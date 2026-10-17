---
disable-model-invocation: true
name: vlm-ocr-alice
description: Runs the GPU part of a vlm-ocr pipeline on Leiden University's ALICE cluster. Decides whether a corpus needs ALICE, picks a GPU partition for the model, sets up storage, a pinned vLLM environment and offline weights, ships code and scans, runs a gate job and chained bulk jobs with the bundled SLURM template, and brings the page records home for post-processing. Use with vlm-ocr when OCRing scans on ALICE or deciding whether to.
argument-hint: '[corpus size in pages, chosen or candidate models, your ALICE accounts and storage]'
---

# VLM-OCR on ALICE

## Instructions

This skill pairs with `vlm-ocr`, which holds the method: `triage`, `evaluate`, `run`, `clean`. This skill covers where and how the GPU work runs on ALICE, Leiden University's SLURM cluster, and the failure modes met in a production run there (October 2026: about 36,600 pages of Korean textbooks with Qwen3.6-35B-A3B-FP8 on vLLM 0.19). Partition names, limits and paths below were checked on 17 Oct 2026; confirm them live before submitting (`sinfo -s`), and use the ALICE wiki and helpdesk (helpdesk@alice.leidenuniv.nl) for anything account-related.

The bundled `scripts/serve_and_ocr.slurm` starts vLLM on the job's GPUs, runs `vlm-ocr`'s `scripts/ocr_client.py` over a manifest, and stops vLLM. Copy both into the deployment's `code/` directory.

### 1. Decide whether the corpus needs ALICE

- **Measure first.** `vlm-ocr` `triage` §3 gives pages per hour for the shortlisted models on the machine you have. Divide the corpus page count by it and add about 30 % for retries.
- **Go to ALICE when** the run would take more than a night on local hardware, or the model that won the comparison does not fit in local memory. A 35B mixture-of-experts model in FP8 needs about 35 GB for weights plus the KV cache; a 24 GB laptop runs 4–8B models only, one page at a time.
- **Stay local** for triage, contact sheets, pilot reads with small models, and all post-processing. These are CPU or small-GPU work.
- **Data:** ALICE is university infrastructure, so scans that may not go to a commercial API can usually go there. Personal data still needs to fit your data management plan; ask the data steward when unsure.

### 2. Pick the partition for the model

| Model footprint | Partition and GRES | Measured or expected |
|---|---|---|
| Up to ~8B parameters (small VLMs, OCR specialists, second readers) | `gpu-l4-24g` `--gres=gpu:l4:1`, or an A100 slice on `gpu-mig-40g` `--gres=gpu:4g.40gb:1` | A 3B second reader (dots.mocr) read the 48 gate sample pages on one MIG slice |
| 30–35B MoE in FP8 (fits one 48 GB GPU) | LUCDH members: `--account=gpu_lucdh --partition=gpu_lucdh --gres=gpu:a40:2`, one server per GPU. Others: `gpu-a100-80g` `--gres=gpu:a100:1` | 2,000–2,700 dense pages/h per A40; 4,300 (dense 1950s print) to 7,500 (sparse elementary pages) pages/h on one A100 |
| Larger than one GPU | `gpu-a100-80g` with several GPUs and tensor parallelism (`TP=` in the template) | Public and scarce; ask before planning on it |
| Tests under 4 h | `gpu-short` `--gres=gpu:1` | Startup and smoke tests |

Time limits: 7 days on the public GPU partitions, 14 days on `gpu_lucdh`, 4 hours on `gpu-short`. `gpu_lucdh` (two A40s on one node) is restricted to its groups; the public partitions are open to every account. When the preferred partition is busy, split the manifest: in the 2026 run, the main books ran on `gpu_lucdh` while the elementary books ran on a public A100 at the same time.

### 3. Set up storage, environment and weights once

- **Keep the deployment on group or project storage, not in `$HOME`:** `ROOT/{code,pdfs,output,logs}`. On ALICE that is `/zfsstore/user/$USER` where your group has it, or your group's directory on `/data1` (shared BeeGFS, 81 % full in October 2026). Check `quota -s` and `df -h` before copying gigabytes of scans.
- **Download weights once, in a CPU job, into a shared cache, at a pinned revision** (`HF_HOME` on the same storage; `hf download <model id> --revision <commit>` in a `cpu-short` job). Serve the same revision (`MODEL_REVISION=<commit>` in the template) and record it; an offline run otherwise loads whatever the shared cache holds. Run every GPU job offline (`HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`; the template sets them), so a missing file fails at once instead of downloading on a compute node.
- **Build the vLLM virtualenv once, in a job, with pinned versions, and never install into it again.** In the production run, reinstalling into a working environment broke its torch build. Record the versions in the job log (the template prints them). The 2026 run used vLLM 0.19.0 with torch 2.10.0.
- **A newer model can need a second environment; build it beside the pinned one.** Gemma 4 needs transformers 5, which vLLM 0.19 excludes, so the 2026 Polish run built vLLM 0.31.0 separately. Its wheels are CUDA 13 builds: with `uv` 0.8 name the index (`--extra-index-url https://download.pytorch.org/whl/cu130 --index-strategy unsafe-best-match`), because `--torch-backend=auto` on a `gpu-short` node picked CUDA 12.6 for an RTX 2080 Ti and the import failed. The node drivers (580–610) support CUDA 13. Install `pymupdf` into any environment the client runs in; the template runs the client with the server's Python.
- **Prefer the model publisher's FP8 or AWQ/GPTQ weights.** FP8 ran on the A40s and A100s through vLLM's weight-only kernels. bitsandbytes 4-bit failed on the MoE model.

### 4. Ship code and scans

- **Build the manifest locally** from `triage.csv`: `doc_id,path[,pages,dpi]`, with the most important documents first (benchmark pairs, then in-scope books), so a job that dies has finished them.
- **Stage scans under ASCII file names** (symlinks are enough) and keep the original names in the manifest. Catalogue names with commas, spaces and parentheses break shell and SLURM quoting.
- **Record the code version:** `git rev-parse HEAD > code/GIT_COMMIT`. The template prints it into every job log.
- **Copy both directories in one transfer:** `rsync -avL code pdfs <login node>:ROOT/` (no trailing slashes, so `code/` and `pdfs/` arrive as directories; `-L` copies symlink targets).

### 5. Run the gate, then chained bulk jobs

- **Submit the gate** (`vlm-ocr` `evaluate` §6) as its own job: `sbatch --export=ALL,MODEL=...,MANIFEST=manifest_gate.csv,RUN=gate serve_and_ocr.slurm`. For a prompt × dpi grid, submit one job per combination, or loop over combinations in one job so the server loads once.
- **Queue the bulk jobs on hold, and release them only after the gate is scored.** `afterok` only means the gate job finished; it knows nothing about CER thresholds or spelling counts. Submit bulk jobs with `--hold` and the settings the gate is expected to confirm, score the gate (`vlm-ocr` `evaluate` §6), then `scontrol release <job id>`, or `scancel` if it failed. In 2026 the bulk jobs were queued behind the final gate and would have been cancelled had it failed; two were later moved to a free public A100 so they ran in parallel with the first.
- **Resubmit the same command after a crash or a timeout.** Page-level resume skips finished pages made with the same model, prompt, dpi and decoding settings. The job exits 1 while pages are missing, failed or refused (resubmit), and 2 when only looping, truncated or empty pages remain (review them).

### 6. Watch without loading the login node

- **Let SLURM email you** (`--mail-type=END,FAIL` in the template; fill in `--mail-user`). If you must look, run `squeue -u $USER` and `sacct -j <id>` in one SSH call, at most once a minute. Never loop `watch` against a login node.
- **Run nothing heavy on a login node:** no Python over the corpus, no model downloads, no post-processing. ALICE's rules require SLURM for compute.
- **If a login node hangs after authentication, use the other one** (login3 and login4 share home directories and the scheduler).
- **Read the job log for:** server ready time, the `nvidia-smi` memory line, pages-per-second lines, the retry-pass count, and the client's final completeness line and exit code.

### 7. Bring the records home

- **`rsync` `output/<run>/` back** and post-process locally or in a `cpu-short` job (`vlm-ocr` `clean`). Post-processing is CPU work and is re-run whenever a rule changes, so it belongs where you iterate.
- **Keep the per-page JSONL** on ALICE and locally; it is the raw layer every later fix is rebuilt from.
- **Leave nothing running:** `squeue -u $USER` is empty, and no `sleep infinity` or interactive jobs are holding GPUs.

### Gotchas from the production run

- **Two vLLM jobs on one node collide on port 8000.** The template asks the operating system for free ports and checks that its own server answers.
- **A compile-cache path left by another user's job raises PermissionError.** The template puts vLLM, Triton and Inductor caches in the job's `$TMPDIR`.
- **On a MIG node, `nvidia-smi` lists every physical GPU,** not the job's slice. The template counts `CUDA_VISIBLE_DEVICES` instead.
- **Loading a 35B model from network storage took about 8 minutes.** The template waits up to 20 minutes for the health check and prints the server log tail if the server dies.
- **Temperature 0 is not bit-identical across batch compositions in vLLM.** Twin scores from the bulk run differed from the gate by up to 0.12 pp raw, within 0.1 pp after cleaning. Treat a larger gap as a pipeline change.
- **vLLM 0.2x and later compile FlashInfer's sampling kernels at start-up, which needs `nvcc`.** ALICE's CUDA modules stop at 12.9 and a CUDA 13 environment ships no compiler, so the server died during warm-up ("Could not find nvcc"). Greedy decoding does not need that sampler: export `VLLM_USE_FLASHINFER_SAMPLER=0`.
- **The client exits 2 when only review pages remain (loops, truncations, empty pages), and SLURM then reports the job as FAILED.** Read the client's last "Done:" line before resubmitting.
- **Online FP8 lets a dense 30B model use the A40s.** Gemma 4 31B in vLLM's `--quantization fp8` matched BF16 on the Polish gate and read about 430 dense pages an hour per A40 (16 in flight) and about 1,700 on an A100 (32 in flight); in BF16 it fills an 80 GB A100 and cannot run on an A40.
- **Some OCR specialists need extra server flags,** for example `--trust-remote-code` and a string chat-template content format for dots.mocr, and the image before the prompt (`CLIENT_ARGS="--image-first --retry-penalty 0"`). Put arguments that carry JSON, such as an image-token budget, one per line in a file passed as `VLLM_ARGS_FILE`. Check the model card's vLLM section and license.

## Quality Checks

- [ ] Need for ALICE decided from corpus pages ÷ measured pages per hour, not assumed
- [ ] Partition matches the model's memory footprint; `gpu-a100-80g` used only when smaller GPUs cannot hold the model or the preferred partition is busy
- [ ] Deployment on group storage with quota checked; weights downloaded in a CPU job at a pinned revision and served at that revision; GPU jobs run offline
- [ ] vLLM environment built once with pinned versions and not modified afterwards; versions and `GIT_COMMIT` printed in every job log
- [ ] Scans staged under ASCII names with a manifest ordered by priority
- [ ] Gate job run and scored first; bulk jobs held (`--hold`) and released only after the gate passed
- [ ] Monitoring by SLURM email; no polling loops or compute on a login node
- [ ] Client's completeness line checked (records = pages, zero errors) and the twins re-scored against the gate
- [ ] Page records copied home and kept; post-processing run off the login node; no jobs left in the queue
