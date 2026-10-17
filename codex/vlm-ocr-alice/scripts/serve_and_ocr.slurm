#!/bin/bash
# Start vLLM on the GPUs SLURM gives this job, run the vlm-ocr client over a
# manifest, stop vLLM. Generalised from a production run on ALICE (Oct 2026:
# 36,600 pages of Korean textbooks with Qwen3.6-35B-A3B-FP8).
#
# A model that fits on one GPU gets one server per GPU (data parallel: the
# client spreads pages over them). A model that does not fit gets one server
# across all GPUs (set TP to the GPU count).
#
# Fill in --mail-user, check the partition lines, mkdir -p ${ROOT}/logs, then from ${ROOT}/code:
#   sbatch --export=ALL,MODEL=Qwen/Qwen3-VL-8B-Instruct,MODEL_REVISION=<commit>,MANIFEST=manifest_gate.csv,RUN=gate serve_and_ocr.slurm
#   sbatch --hold --export=ALL,MODEL=...,MANIFEST=manifest_bulk.csv,RUN=bulk serve_and_ocr.slurm
#   ... score the gate; then `scontrol release <bulk job id>`, or `scancel` it.
# Exit status follows ocr_client.py: 0 all pages accepted, 1 pages missing or
# failed (resubmit), 2 only loop/length/empty pages left (review them).
# Partitions (check `sinfo -s` first):
#   public A100 80 GB:  --partition=gpu-a100-80g --gres=gpu:a100:1   (7 days)
#   public A100 slice:  --partition=gpu-mig-40g  --gres=gpu:4g.40gb:1 (3-8B models, second readers)
#   public L4 24 GB:    --partition=gpu-l4-24g   --gres=gpu:l4:1      (models up to ~8B)
#   LUCDH members:      --account=gpu_lucdh --partition=gpu_lucdh --gres=gpu:a40:2 (14 days)
#   short tests:        --partition=gpu-short --gres=gpu:1 --time=01:00:00
#
#SBATCH --job-name=vlm-ocr
#SBATCH --partition=gpu-a100-80g
#SBATCH --gres=gpu:a100:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=96G
#SBATCH --time=24:00:00
#SBATCH --output=../logs/%j.out
#SBATCH --error=../logs/%j.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=YOUR_EMAIL@leidenuniv.nl

set -uo pipefail

ROOT="${ROOT:-$(cd .. && pwd)}"            # holds code/, pdfs/, output/, logs/
CODE="${ROOT}/code"                       # this script, ocr_client.py, prompt, manifests, GIT_COMMIT
VENV="${VENV:?set VENV to the vLLM virtualenv}"   # built once; do not reinstall into it
MODEL="${MODEL:?set MODEL to a Hugging Face id in the cache}"
MANIFEST="${MANIFEST:?set MANIFEST (doc_id,path[,pages,dpi])}"
PROMPT_FILE="${PROMPT_FILE:-prompt.txt}"
RUN="${RUN:-run}"
OUT="${ROOT}/output/${RUN}"
TP="${TP:-1}"                             # GPUs per server; >1 only when the model does not fit on one
MAX_MODEL_LEN="${MAX_MODEL_LEN:-16384}"
MAX_NUM_SEQS="${MAX_NUM_SEQS:-32}"
CONCURRENCY="${CONCURRENCY:-32}"          # requests in flight per server
MODEL_REVISION="${MODEL_REVISION:-}"      # commit hash of the weights; pin it for a reproducible run
# Extra arguments, one per line in a file (safe for JSON values), or as a simple
# space-separated string for flags without spaces or quotes.
#   vllm_args.txt:  --trust-remote-code
#                   --mm-processor-kwargs
#                   {"max_soft_tokens": 1120}
VLLM_ARGS_FILE="${VLLM_ARGS_FILE:-}"; VLLM_ARGS="${VLLM_ARGS:-}"
CLIENT_ARGS_FILE="${CLIENT_ARGS_FILE:-}"; CLIENT_ARGS="${CLIENT_ARGS:---no-thinking}"
VLLM_EXTRA=(); CLIENT_EXTRA=()
if [ -n "${VLLM_ARGS_FILE}" ]; then mapfile -t VLLM_EXTRA < "${VLLM_ARGS_FILE}"; else read -ra VLLM_EXTRA <<< "${VLLM_ARGS}"; fi
if [ -n "${CLIENT_ARGS_FILE}" ]; then mapfile -t CLIENT_EXTRA < "${CLIENT_ARGS_FILE}"; else read -ra CLIENT_EXTRA <<< "${CLIENT_ARGS}"; fi
if [ -n "${MODEL_REVISION}" ]; then VLLM_EXTRA+=(--revision "${MODEL_REVISION}"); fi
export HF_HOME="${HF_HOME:?set HF_HOME to the shared model cache}"
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1   # weights were downloaded beforehand

# On a MIG node nvidia-smi lists every physical GPU; count this job's devices.
[ -n "${CUDA_VISIBLE_DEVICES:-}" ] || { echo "no GPU allocated (CUDA_VISIBLE_DEVICES unset)"; exit 1; }
NGPU=$(echo "${CUDA_VISIBLE_DEVICES}" | tr ',' '\n' | grep -c .)
if [ "${TP}" -lt 1 ] || [ "${TP}" -gt "${NGPU}" ] || [ $(( NGPU % TP )) -ne 0 ]; then
    echo "TP=${TP} does not divide the ${NGPU} allocated GPU(s)"; exit 1
fi
NSERVERS=$(( NGPU / TP ))
# Two vLLM jobs can land on one node: ask the OS for free ports. Keep compile
# caches in this job's TMPDIR (a cache path left by another job on the node
# raises PermissionError).
free_port() { "${VENV}/bin/python" -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()'; }
export VLLM_CACHE_ROOT="${TMPDIR}/vllm" TORCHINDUCTOR_CACHE_DIR="${TMPDIR}/inductor" TRITON_CACHE_DIR="${TMPDIR}/triton"

mkdir -p "${OUT}" "${ROOT}/logs"
echo "Job ${SLURM_JOB_ID} on ${SLURMD_NODENAME} (${SLURM_JOB_PARTITION}) $(date)"
echo "GPUs: $(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | paste -sd';')"
echo "MODEL=${MODEL} revision=${MODEL_REVISION:-unpinned} servers=${NSERVERS} TP=${TP} manifest=${MANIFEST} out=${OUT} commit=$(cat "${CODE}/GIT_COMMIT" 2>/dev/null)"
"${VENV}/bin/python" -c "import vllm, torch; print('vllm', vllm.__version__, 'torch', torch.__version__)"

PIDS=(); URLS=(); PORTS=()
DEVICES=(${CUDA_VISIBLE_DEVICES//,/ })
for s in $(seq 0 $((NSERVERS - 1))); do
    PORT=$(free_port); PORTS+=("${PORT}")
    if [ "${NSERVERS}" -gt 1 ]; then   # pin each server to its own GPU(s)
        export CUDA_VISIBLE_DEVICES=$(IFS=,; echo "${DEVICES[*]:$((s * TP)):${TP}}")
    fi
    "${VENV}/bin/python" -m vllm.entrypoints.openai.api_server \
        --model "${MODEL}" --tensor-parallel-size "${TP}" \
        --max-model-len "${MAX_MODEL_LEN}" --max-num-seqs "${MAX_NUM_SEQS}" \
        --gpu-memory-utilization 0.92 --limit-mm-per-prompt '{"image": 1}' \
        --host 127.0.0.1 --port "${PORT}" "${VLLM_EXTRA[@]}" \
        > "${ROOT}/logs/vllm_${SLURM_JOB_ID}_${s}.log" 2>&1 &
    PIDS+=($!); URLS+=("http://127.0.0.1:${PORT}/v1")
done
stop_servers() { kill "${PIDS[@]}" 2>/dev/null; wait "${PIDS[@]}" 2>/dev/null; }
trap stop_servers EXIT

# Loading a 35B model from network storage took about 8 minutes; allow 20.
for s in $(seq 0 $((NSERVERS - 1))); do
    PORT=${PORTS[$s]}; READY=0
    for i in $(seq 1 240); do   # 240 x 5 s = 20 min
        kill -0 "${PIDS[$s]}" 2>/dev/null || { echo "server ${s} died:"; tail -40 "${ROOT}/logs/vllm_${SLURM_JOB_ID}_${s}.log"; exit 1; }
        if curl -sf -m 5 "http://127.0.0.1:${PORT}/health" >/dev/null 2>&1; then
            echo "server ${s} ready after about $((i * 5))s on port ${PORT}"; READY=1; break
        fi
        sleep 5
    done
    [ "${READY}" -eq 1 ] || { echo "server ${s} not ready after 20 min"; exit 1; }
done
nvidia-smi --query-gpu=index,memory.used,memory.total --format=csv,noheader

cd "${CODE}"
"${VENV}/bin/python" ocr_client.py --manifest "${MANIFEST}" --root "${ROOT}/pdfs" \
    --output "${OUT}" --prompt-file "${PROMPT_FILE}" --model "${MODEL}" \
    --api-url "${URLS[@]}" --concurrency "${CONCURRENCY}" "${CLIENT_EXTRA[@]}"
EXIT_CODE=$?
echo "Finished $(date) exit ${EXIT_CODE} output ${OUT}"
exit ${EXIT_CODE}
