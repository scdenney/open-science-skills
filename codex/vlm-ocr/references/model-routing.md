# VLM-OCR Model Routing (checked 17 October 2026)

A dated shortlist for `triage` §3. This field changes monthly: if this file is more than about three months old, refresh it with the recipe at the end before relying on it. Every shortlist here is a starting point for `evaluate`, never a substitute for it. No public benchmark measures mixed hangul–hanja print or historical print in most non-Latin scripts, so the gate on your own pages decides.

Sources: model cards and licenses on Hugging Face; MDPBench (real pages, 17 languages; arXiv 2603.28130); GlotOCR Bench (synthetic sentences, 100+ scripts; arXiv 2604.12978); OCRBench v2 board (99franklin.github.io/ocrbench_v2); OmniDocBench board (github.com/opendatalab/OmniDocBench); CHURRO (historical; stanford-oval.github.io/Churro); vLLM recipes (recipes.vllm.ai); provider pricing and data-terms pages. "Measured" means this author's own runs (below); everything else is published, and vendor-reported figures are marked.

## What the benchmarks can and cannot tell you

- **OmniDocBench and olmOCR-Bench are English and Chinese only**, weighted toward tables, formulas and layout, and mostly self-reported. Small specialists (about 1B parameters) top them. A 1–2 point difference carries no information, and scores are not comparable across benchmark versions.
- **MDPBench and GlotOCR are the only broad per-language evidence.** On real Korean pages, GLM-OCR scored 61, MinerU-2.5 15 and DeepSeek-OCR 28, against 86 for PaddleOCR-VL-1.5 and 85.5 for Gemini-3-pro-preview. Open models lose about 14 % on non-Latin scripts. Users report OvisOCR2 writing Chinese characters in place of hangul.
- **A leaderboard leader can be wrong for your script.** In this author's runs, DeepSeek-OCR left repetition junk in up to 14.6 % of a Korean book, and GLM-OCR differed from a 35B general model by 14–15 % of characters on 1960s–70s Korean print.

## Measured reference points

| Setup | Pages | Result |
|---|---|---|
| `Qwen/Qwen3.6-35B-A3B-FP8`, vLLM 0.19, one server per A40 48 GB, 32 requests in flight | 36,600 Korean textbook pages, 1950s–2010s | 2,000–2,700 dense pages/h per A40; CER 1–2 % (1990s–2000s print), about 3 % (1961 print) against born-digital twins |
| Same model, one A100 80 GB | 10,194 elementary pages; 1,369 dense 1950s pages | 7,500 and 4,300 pages/h |
| Apple M4 Pro, 24 GB, Ollama 0.40.6, one request at a time | 4 Korean pages (1961, 1975), 2 Polish pages | Character distance from the Qwen3.6 text, Korean / seconds per page Korean, Polish: `qwen3-vl:8b-instruct` (Q4_K_M) 1.4–2.6 % on 1975 print, 7.1 % on 1961 / 11–18 s, 33 s. `gemma4:e4b` 3.4–4.0 % / 14–24 s, 44 s. `glm-ocr` 14–15 % / 5–8 s, 12 s. `qwen3-vl:8b` (the thinking build) returned empty pages after spending its token budget |
| Polish gate, 48 pages of history textbooks 1948–2003, against a blind model read checked on the scan (vLLM, 200 dpi) | 46 scored pages | Median / mean CER after Polish post-processing: `google/gemma-4-31B-it` 0.09 % / 0.19 % (diacritic recall 99.65 %); `Qwen/Qwen3.6-35B-A3B-FP8` 0.27 % / 0.45 %; `Qwen/Qwen3.6-27B-FP8` 0.23 % / 1.47 % (listed a map's labels); `datalab-to/chandra-ocr-2` 0.70 % / 6.67 % (raw). Gemma 4 FP8 = BF16; 300 dpi no gain. Qwen keeps line-end hyphens; Gemma joins them but twice repeated a whole box |

Distances against another model's output are not error rates, but a gap of 14 % against 2 % is not noise.

## Shortlist by hardware tier and script

Script groups: (a) Latin with diacritics, including Polish, Czech, German and older Latin type; (b) CJK, including Korean with hanja; (c) Cyrillic, Arabic, Devanagari. VRAM figures are weights only; add 20–40 % for batch serving.

| Tier | (a) Latin | (b) CJK / Korean | (c) Cyrillic / Arabic / Devanagari |
|---|---|---|---|
| **CPU only** | A hosted API in batch mode if the data terms allow; otherwise a ≤1B specialist through llama.cpp on a small corpus (no published CPU throughput; expect minutes per page) | `PaddlePaddle/PaddleOCR-VL-1.6` official GGUF through llama.cpp (about 1 GB); or a hosted API | Hosted API (Gemini has the best independent evidence); Surya OCR 2 (vendor figures; license threshold) |
| **Apple Silicon 16–24 GB** (Ollama, mlx-vlm, llama.cpp) | `qwen3-vl:8b-instruct` or `Qwen3.5-9B` 8-bit; `PaddleOCR-VL-1.6` 4-bit | `qwen3-vl:8b-instruct` (measured above); `PaddleOCR-VL-1.6`; `Qwen3.5-9B` 8-bit | `Qwen3.5-9B` 8-bit; `qwen3-vl:8b-instruct` |
| **Apple Silicon 32–64 GB** | `mlx-community/Qwen3.6-35B-A3B-4bit` (about 20 GB) or `-8bit` (about 37 GB, 48 GB+ machines); `Qwen3.6-27B` 8-bit | same as the production model at 4- or 8-bit; quantization effect on Korean untested | same |
| **NVIDIA 12–24 GB (32 GB RTX 5090)** | `Qwen3.5-9B` (vLLM, BF16 on 24 GB); `lightonai/LightOnOCR-3-4B` or `-1B` (Latin focus; vendor 3.4 pages/s on H100); `datalab-to/chandra-ocr-2` (license threshold) | `PaddleOCR-VL-1.6` (vLLM, about 2 GB; 1.35–1.6 pages/s on A100); `Qwen3.5-9B`; on 24–32 GB, a community AWQ 4-bit of `Qwen3.6-35B-A3B` (about 20 GB) | `Qwen3.5-9B`; `dots.mocr` (best open MDPBench Arabic and Hindi; see licenses) |
| **48 GB (A40, L40S, RTX 6000 Ada)** | `google/gemma-4-31B-it` with online FP8 (measured best on Polish, above); `Qwen/Qwen3.6-35B-A3B-FP8` (about 2.5× faster); `Qwen/Qwen3.6-27B-FP8` | `Qwen3.6-35B-A3B-FP8` (production, measured above); `Qwen3.6-27B-FP8` as the A/B candidate; `PaddleOCR-VL-1.6` as a cheap cross-check | `Qwen3.6-35B-A3B-FP8`; compare Gemini on a sample for Arabic, where every open model trails it |
| **80 GB+ or several GPUs** | One copy of the 48 GB-tier model per GPU (data parallel), not a bigger model: Qwen's own document-OCR scores rise only from 89.9 (35B-A3B) to 90.8 (397B) | same; escalate failed pages to `Qwen3.5-122B-A10B-FP8` or `Qwen3-VL-235B-A22B` | same |
| **Hosted API** | Mistral OCR 4.1 ($2 per 1,000 pages in batch); Gemini flash-class in batch (about $1.4–2.3 per 1,000, estimated) | Gemini (MDPBench Korean 85.5); hanja: no evidence | Gemini; Mistral OCR 4.1 (claimed, unbenchmarked) |

To test before adopting, not yet shortlist material: `Qwen/Qwen3.8-27B` (higher on Qwen's own document benchmark, lower on the independent OCRBench v2 board than Qwen3.6); `openbmb/MiniCPM-V-4.7-35B-A3B` (vendor claims only; no released vLLM supports it as of this date); `zenosai/MonkeyOCRv2-B-Parsing` (highest MDPBench scores, but self-reported); `ATH-MaaS/Ovis2.6-30B-A3B` (top general model on OmniDocBench; no per-language evidence).

## Licenses and data terms that rule models out

- **`tencent/HunyuanOCR`**: the license territory excludes the European Union, the United Kingdom and South Korea.
- **`dots-studio/dots.mocr`** (formerly `rednote-hilab/dots.mocr`): tagged MIT, but the bundled agreement says licensees "shall not use the tool for unauthorized digitization of publications/document scanning" and restricts GDPR-sensitive data. Get it reviewed before using it on published books, even as a second reader.
- **Chandra OCR 2 and Surya OCR 2**: modified OpenRAIL-M; a commercial license is needed above $2M (Chandra) or $5M (Surya) in revenue or funding; research and personal use are exempt for both.
- **Llama 4 multimodal**: the use policy withholds the multimodal rights from individuals and companies domiciled in the EU (end users of a product built on it are exempt), so an EU-based researcher or institution has no license to run it. **`tencent/Youtu-Parsing`**: "not intended for use within the European Union". **EXAONE 4.5, VARCO-VISION 2.0, jina-ocr-v1**: non-commercial.
- **Hosted APIs**: read the data-use terms for your region and tier. Gemini's unpaid tier may use inputs for training outside the EEA, Switzerland and the UK, where Google applies its paid-service data terms; a paid tier is the safe default. Batch endpoints at OpenAI, Anthropic and Mistral are not zero-data-retention eligible. Anthropic's first-party API offers no EU processing; Vertex AI and Azure do. **Gemini's RECITATION filter blocks transcription of published text**, and one user saw the block rate on public-domain books rise to 1 in 50 pages. Expect it to be worst on copyrighted textbooks. Parse the finish reason and route blocked pages to a local model.

## Failure modes by family

| Failure | Where it shows | Mitigation |
|---|---|---|
| Repetition loops to the token limit | Qwen2.5/3-VL (worse at 4-bit), DeepSeek-OCR, dots.ocr, MinerU, GLM-OCR under GGUF, Gemma 4 long outputs | Cap `max_tokens`; detect loops; retry once with a mild repetition penalty (1.05), then trim. Strong penalties corrupt tables and legitimately repeated syllables, so test on gold pages |
| Thinking spends the budget and returns nothing | Qwen3.5/3.6/3.8 think by default; Ollama's plain `qwen3-vl` tags are the thinking builds; GLM-4.5V/4.6V | Disable thinking server-wide (vLLM `--default-chat-template-kwargs '{"enable_thinking": false}'`) or per request; pull `-instruct` tags. Qwen3.6 does not support `/nothink` |
| Wrong-script output | Most specialists on non-Latin scripts; general models on low-resource scripts | Per-page script-ratio checks (`triage.py profile`); name the scripts in the prompt |
| Invented text on blank and picture pages | olmOCR (older versions), PaddleOCR-VL without its layout stage, HunyuanOCR, small general models | Page-type tag in the prompt; drop non-body pages; spot-check picture pages |
| Image downscaled before the model sees it | Gemma 4 in vLLM defaults to 280 image tokens (raising it to 1,120 cut OmniDocBench edit distance from 0.201 to 0.131); Mistral models cap images at 1,540 px | Set the image token budget per model explicitly |
| Quantization damage | bitsandbytes 4-bit leaves fused MoE expert weights unquantized in transformers v5 implementations (bitsandbytes #1849, open) | Use the publisher's FP8, or AWQ/GPTQ; keep the vision projector (`mmproj`) at 16-bit in GGUF builds |
| Runtime-specific bugs | Ollama ignores repetition and presence penalties for Qwen3.5-family models (ollama #14493); a maintainer reports OCR accuracy problems with MiniCPM-V under Ollama; results differ between transformers and vLLM for some parsers | Pin runtime versions; re-score the gold set after every runtime upgrade |

FP8 on Ampere GPUs (A40, A100, RTX 30xx) runs as weight-only W8A16 in vLLM: it saves memory, not compute. Ada, Hopper and Blackwell GPUs run FP8 natively.

## Serving tools on the check date

vLLM 0.31.0 (2026-10-05), SGLang 0.5.22, transformers 5.20.1, mlx-vlm 0.7.8, Ollama 0.40.6, PaddleOCR 3.7.0, mineru 4.0.12. Newer models often need a recent vLLM; a pinned production environment (vLLM 0.19 in the measured run) cannot serve them without a second environment.

## Refreshing this file

1. List new releases: the Hugging Face API (`huggingface.co/api/models?author=<org>&sort=createdAt`) for Qwen, PaddlePaddle, google, openbmb, allenai, lightonai, datalab-to, zai-org, deepseek-ai, opendatalab, plus a search for "OCR" sorted by creation date.
2. For each candidate: license text (not just the tag), languages with per-language OCR evidence, vLLM or llama.cpp support and the minimum version, official quantizations.
3. Check the per-language boards first (MDPBench, GlotOCR, CHURRO), then the English/Chinese ones.
4. Re-check hosted prices and data terms on the providers' own pages.
5. Change the date in the title, and keep the measured rows: they are the only figures on real pages of the author's corpora.
