---
name: vlm-ocr
description: "OCR scanned or image-only corpora with vision-language models in four phases: `triage` inventories the scans, identifies script and language, and shortlists models by script, hardware, and data constraints; `evaluate` picks a system by measured CER/WER against ground truth, using born-digital twins, a second reader, and decision rules set in advance; `run` builds the production pipeline; and `clean` removes model artifacts, audits what every cleaning rule deletes, corrects with rule-based and LLM passes, and records provenance. Born-digital documents with a text layer go to $doc-to-markdown; runs on Leiden's ALICE cluster add $vlm-ocr-alice."
---

# VLM-OCR: Scanned Corpora from Page Images to Research-Usable Text

## Instructions

This skill covers the whole path from a corpus of page images to text an analysis can consume: knowing what the scans are and which models can read them (`triage`), choosing an OCR system by measurement (`evaluate`), running the chosen model across the corpus (`run`), and correcting and documenting its output (`clean`).

**Use this skill only for scanned or image-only documents.** Born-digital PDFs, Word files, and anything carrying an embedded text layer belong to `$doc-to-markdown`, which extracts the text directly and needs no model at all. A PDF yielding under ~300 extractable characters per page is a scan. So is a PDF whose text is an invisible layer over page-sized images: that is an earlier OCR, usually worse than a current model, and `triage` detects it.

Two bundled scripts carry the mechanics: `scripts/triage.py` (inventory, contact sheets, script and language profile) and `scripts/ocr_client.py` (resumable page OCR against any OpenAI-compatible endpoint: vLLM, SGLang, llama.cpp, Ollama, LM Studio, or a hosted API). The dated model shortlist is `references/model-routing.md`; it goes stale within months, so check its date and refresh it before relying on it.

### Phase selection

Infer the phase from what the user brings:

| What you are given | Phase |
|---|---|
| A folder of scans not yet characterized, or the question of which models or hardware a corpus needs | `triage` |
| A triaged corpus with a shortlist, or the question of which OCR system to use or how accurate one is on these pages | `evaluate` |
| A chosen model and a corpus to transcribe at scale | `run` |
| Raw OCR output needing correction, quality diagnostics, or a provenance record | `clean` |

Invoking `$vlm-ocr triage`, `$vlm-ocr evaluate`, `$vlm-ocr run`, or `$vlm-ocr clean` forces a phase. Otherwise infer it, and state which phase you are working in before you start.

### Phase order and handoff

`triage` → `evaluate` → `run` → `clean`. Each phase produces exactly what the next one consumes:

- `triage` emits an inventory (`triage.csv`), the scripts and languages per document, layout risks for the prompt, a model shortlist per script with the hardware route, and the ground truth that already exists. `evaluate` scores the shortlist.
- `evaluate` emits a model registry, a declared normalization recipe, per-stratum CER/WER, and a documented model choice — possibly one model per script or era. `run` takes the chosen model and the registry.
- `run` emits per-page structured records: the raw response, the transcription, page type, finish reason and loop flag, and the pipeline settings (`ocr_client.py` writes these; the richer schema with uncertain spans and layout markers is in `references/prompt-and-schema.md` (b)). `clean` uses these to route pages to a correction strategy and to anchor its own edit log.
- `clean` emits corrected text plus a span-level provenance log anchored to the raw OCR revision, with the raw text preserved alongside every corrected variant.

Moving backwards is legitimate and expected: a `run` whose diagnostics fail returns to `evaluate` for a different model, and a `clean` pass that finds systematic transcription failure returns to `run` at higher DPI or without quantization.

### Provenance rules that hold in every phase

- **Pin and date every model.** Exact identifier plus revision or commit hash for open-weight models; the dated identifier for hosted APIs. Family-name reporting ("we used Qwen and Gemma") is not reproducible, and neither is an undated proprietary model name.
- **Record every parameter in machine-readable form** alongside the output, not in prose notes: quantization, DPI, prompt text or prompt id, generation parameters (temperature, max tokens, sampling strategy, seed), software versions, and hardware.
- **Never overwrite the previous stage's text.** Raw OCR survives every correction pass; each stage writes a new artifact and leaves its input intact, so a downstream researcher can choose a different normalization. Keep the per-page model output as the raw layer: every cleaning bug found later is then fixed by re-running CPU post-processing, not the OCR.
- **Declare normalization once and reuse it.** The recipe declared in `evaluate` §4 is the same one `run` §6 reports against and `clean` §5 scores with. Two different recipes across phases make the numbers incomparable.
- **Prefer locally-hosted open-weight models pinned to a revision** when publication-grade reproducibility is required; hosted APIs change underneath you (Barrie, Palmer & Spirling 2025).
- For the methods-section disclosure of any phase, compose with `$methods-reporting`. For the hardest pages, where no single model is reliable, transcribe with several independent models and route disagreements to a human; agreement between models is not ground truth, since models trained on similar data fail on the same pages.

---

## Phase `triage`: Know the Scans Before Choosing a Model

Triage answers four questions before any model is compared: what the files are, which scripts and languages they hold, which models and hardware can read them, and what ground truth already exists. It costs minutes of CPU and prevents the expensive surprises: a model that cannot read the script, a layout the prompt does not handle, or a corpus that cannot leave the machine.

### 1. Inventory

- Run `python scripts/triage.py scan <corpus> --out triage/`. Per document it records page count, a content hash, the kind of text layer (none, born-digital, or an invisible earlier OCR over page images), `/Rotate` flags, landscape pages, page size, scan resolution, and the script mix of any text layer. It renders sample body pages from the middle 60 % of each book (covers, front matter and indexes are sparse or in another language) and draws contact sheets of twelve documents each.
- **Landscape pages in a book are usually two-page spreads.** Split them before OCR, or the model reads across the gutter. In one 229-book collection, 4 files were spreads and the rest single pages, so check per file.
- **`/Rotate` flags are common in older scans.** Rendering with PyMuPDF's `get_pixmap` applies them; extracting the embedded image directly does not.
- **Reconcile files with the catalogue now.** Look for exact duplicate scans (same hash), two files that map to one catalogue id, reprints of an edition you already hold, and catalogued books with no scan. Before declaring a scan missing or mislabelled, open its title page. Fixing ids after the corpus is built costs a re-merge.

### 2. Recognize script and language

Script and language decide the model shortlist and the prompt, so establish them from evidence, not from the collection's label.

- **Look at the contact sheets.** You can read the PNGs in `triage/sheets/`; a person can too. Name, per document, the scripts (including secondary ones: hanja inside Korean, Latin or German quotations inside Polish), the language, the approximate print era, and the layout risks: columns, vertical text, spreads, margin headings, tables, maps, picture-heavy pages, handwriting, blackletter. This is the most reliable check for a corpus of tens to hundreds of books.
- **Count characters by Unicode script on any text you have** (`triage.py profile`). It is the only reliable measure of mixed-script ratios such as hangul to hanja, which no language identifier reports. Where a text layer exists, run language identification on it (`--lid`: GlotLID v3, 2,102 language-script labels, Apache-2.0; lingua as fallback). Expect it to degrade on noisy text: in DIVERS-Bench (arXiv 2509.17768), GlotLID's macro-F1 is 93 on FLORES (clean, edited sentences) and 65 on SMOL, its noisiest set; no benchmark tests OCR output directly.
- **For scans without a text layer, pilot-read the sample pages** with a small multilingual model from the shortlist, then profile and identify the language of its output. Do not use Tesseract's script detection: in a test it read Polish print as Cyrillic at 100 dpi and Korean as Japanese at 300 dpi, and it weights every Han character toward Korean or Japanese by a fixed ratio.
- **A vision model's own guess of the script is reliable only for about ten major scripts.** In GlotOCR Bench (158 scripts; arXiv 2604.12978), averaged across scripts, 68 % of model outputs were in the wrong script, mostly on low-resource scripts. That measures transcription, not a direct question about the script, but the failure is the same. For anything beyond Latin, Cyrillic, Greek, Han, Hangul, Japanese, and Devanagari, confirm the script by eye.
- **Route mixed documents by the dominant script of each page, and name the secondary scripts in the prompt.** Telling a model the script raised its accuracy on Han characters by more than 20 points in the same benchmark.

### 3. Route by script, hardware, and data constraints

- **Shortlist two to four models per script family** from `references/model-routing.md`: at least two general vision-language models from different families and one small document-OCR specialist. Specialists top the layout leaderboards (OmniDocBench, olmOCR-Bench), but those are English and Chinese only. On real Korean pages (MDPBench, arXiv 2603.28130), GLM-OCR, MinerU and DeepSeek-OCR scored 15–61 against 86 for PaddleOCR-VL. In this author's runs, DeepSeek-OCR left repetition-loop junk in up to 14.6 % of a Korean book, and GLM-OCR differed from a 35B general model by 14–15 % of characters on 1960s–70s print. Choose specialists from per-language evidence, never from the headline board.
- **Read each model's license, not its tag.** HunyuanOCR's territory excludes the EU, the UK and South Korea. dots.mocr is tagged MIT, but its bundled agreement forbids "unauthorized digitization of publications/document scanning". Llama 4's multimodal models exclude EU-based users, and Chandra and Surya need a paid license above a revenue threshold.
- **Hardware decides which shortlisted models are feasible and how long the run takes.** Measure pages per hour on the pilot pages, divide the corpus page count by it, and add about 30 % for retries and re-runs. If the result exceeds what the machine can run unattended, or the best model does not fit in memory, move to a cluster or a hosted API. Reference points from this author's runs: a 35B mixture-of-experts model in FP8 read 2,000–2,700 dense book pages an hour on one 48 GB A40. One 80 GB A100 read 4,300 pages an hour of dense 1950s print and 7,500 of sparse elementary pages. On a 24 GB Apple M4 Pro laptop through Ollama, Qwen3-VL-8B took 11–33 seconds a page, one request at a time, or 110–330 pages an hour (`references/model-routing.md`).
- **Data terms can rule out hosted APIs.** Scans held under a library agreement, archival records with personal data, and anything under GDPR may not be sent to a commercial API. Check before the shortlist includes one: use paid tiers only, and note that batch endpoints are often excluded from zero-data-retention terms. Published books also meet content filters: Gemini's RECITATION block returns empty output for transcribed published text, at rates one user put at 1 in 50 pages. Hosted models also change underneath you (see `run` §7), so a publication corpus favours pinned open weights.

### 4. Find ground truth that already exists

- **Look for born-digital twins: the same edition already available as typeset text.** National digital libraries, publisher files, Wikisource, and earlier hand-corrected transcriptions all qualify. For South Korean state textbooks, the national history institute's typeset editions matched 19 scanned books from 1961 to 2007, which became the benchmark pairs for every decision in that pipeline.
- **Check that the twin is the same edition.** Compare the title page and colophon, then align OCR paragraphs to the twin (see `evaluate` §4). When over 0.9 of the OCR text aligns and over 0.9 of the twin's text is matched, it is the same text; below 0.5 on either side, a different edition or printing. Alignment alone cannot prove edition identity.
- **Split twins into development and test pairs** before tuning anything, and report only the test pairs.
- Where no twin exists for a stratum (here, the 1957–61 world-history books), plan hand transcription for it and a second reader (`evaluate` §6).

### 5. Output

`triage.csv`; the contact sheets; per document, the scripts, language, era and layout risks; a shortlist per script family with the hardware route and an estimate of hours; the data constraints; and the ground-truth plan. `evaluate` starts from these.

---

## Phase `evaluate`: Comparing OCR Systems Before You Commit

Before running any OCR model across a whole corpus, run a controlled comparison on a small, human-transcribed sample and let the measured error rates pick the model. This is the **selection gate**: choose a model and document why, then move to `run`.

### 1. Run a Comparison Before You Commit

- Treat model choice as an empirical question. A model that tops a general vision-language leaderboard, or reads one language well, can still fail on your script, era, or page layout; its error rate on pages like yours is the only trustworthy signal. A 50–100 page comparison is cheap next to discovering, after a 50,000-page run, that the model dropped every table or collapsed on degraded scans.
- Scope the comparison to the decision. The concrete figures throughout this phase come from one 9-system, 64-page comparison across two languages and seven decades, and from the gate of a 2026 production run on about 36,600 pages of Korean textbooks — enough to rank candidates on the strata that matter, not a full corpus. Treat them as evidence from two corpora, not as general findings.
- The output is a go/no-go gate: keep the model whose accuracy clears your threshold on the strata you care about, or conclude that no single model does and split the corpus by script or era (§7).

### 2. Assemble the Candidate Set

- Include three kinds of system: several **open-weight VLMs** from different families, one or two **proprietary APIs** where the data terms allow (`triage` §3), and a **small document-OCR specialist** as the cheap baseline. The reference comparison held six open-weight VLMs spanning two size tiers and three families, a traditional OCR engine, and two proprietary APIs — nine systems total. Start from the `triage` shortlist and `references/model-routing.md` rather than copying a fixed list; what transfers is the shape of the candidate set, not its membership.
- Pick the VLM candidates from **OCR benchmarks with per-language results** (MDPBench, GlotOCR Bench), then the English and Chinese document boards, never from general multimodal leaderboards. General vision-language ability does not predict transcription fidelity on dense historical print; the `run` phase §1 covers benchmark-grounded model selection in detail.
- Keep a **cheap baseline**: a sub-2B document-OCR specialist shows what a fast model already gets right and where a large VLM earns its cost and latency. Do not use Tesseract as the baseline; it fails on non-Latin and degraded print, so it no longer marks what current tools can do.
- Record an exact registry entry per system — `name` / `hf_id` (or dated API identifier) / `type` / `quantization` / `loader`, one row per model — so the run is reconstructible from the registry alone.

### 3. Build a Stratified Ground-Truth Set

- Human-transcribe a **stratified** sample, not a convenience sample. Stratify on the dimensions that actually drive OCR difficulty: language/script, era (a decade bracket), and content type — running body text, multi-column tables, illustrated or captioned pages, degraded or water-damaged print, and front matter / title pages. Build a page manifest tagging each page with `language`, `year`, `decade`, `subject`, and `content_type`, and sample across all of them.
- Size: roughly **50–100 pages** is a workable default for a handful of candidate systems (a house default that balances transcription effort against per-stratum cell sizes, not a cited figure). More strata require more pages so that each cell holds enough pages to mean something.
- Store ground truth as **one UTF-8 `.txt` per page**, keyed by a stable page id (`ground_truth/<page_id>.txt`), so scoring joins on the id rather than on file order. Transcribe faithfully — preserve the characters actually on the page (hanja alongside hangul, diacritics) — and decide up front how to render non-text regions (tables, figures) so the reference and the OCR output are scored on the same basis.
- Transcribe **before** looking at any model output, so the reference is not anchored to a model's guesses. Two independent transcribers on a subset, with disagreements reconciled, guard against a single transcriber's systematic errors (the inter-coder logic in the `$text-classification` skill applies here too).
- **Born-digital twins (`triage` §4) are ground truth for the strata they cover**, often whole books rather than sampled pages. Hand-transcribe only the strata they miss. A twin is usually a modern typeset edition, so it cannot reveal errors that turn old spellings into modern ones; the spelling check in §6 covers that gap.

### 4. Character and Word Error Rate

- CER and WER are **edit-distance** metrics. CER = Levenshtein(reference, hypothesis) ÷ length(reference); WER is the same at the word level (a word-level dynamic-programming edit distance ÷ reference word count). Implement both directly — a character Levenshtein distance for CER and a word-level DP for WER (Levenshtein 1966) — rather than trusting an unaudited helper, and report which implementation was used.
- **When the reference is a twin rather than a transcription of the exact page, score aligned spans and report both directions of coverage.** Locate each OCR paragraph in the reference with a partial alignment and keep it when the aligned span is similar enough. Then report three numbers: CER over the kept spans (a conditional CER, which excludes the hardest misreads); the share of OCR text that aligned (unaligned OCR text is captions the twin lacks, revisions, or invention); and the share of the twin's text that the aligned OCR covers (reference-side recall). Only recall detects deleted text: dropping half a book leaves the OCR-side share and the CER unchanged. A cleaning change that lowers recall has removed text (`clean` §2).
- **Reduce both texts to the characters that carry content before computing CER** (for Korean, hangul, hanja and digits), and score spacing and punctuation separately, so a spacing convention does not swamp character errors.
- **Declare normalization before scoring; it changes the numbers.** A workable default: apply Unicode **NFC**, strip markdown artifacts (headers, bold/italic, links — VLMs routinely emit markdown), collapse whitespace, and stay deliberately **case-sensitive** (no lowercasing) to preserve OCR fidelity. State each choice (NFC vs NFKC, case sensitivity, punctuation and markdown handling) and apply it identically to every system. Comparing a markdown-emitting VLM against a plain-text baseline without stripping markup unfairly penalizes the VLM.
- **Report both CER and WER, and report the distribution, not a single mean.** Give mean *and* median with the page count (`n`) per cell. The median resists the blank-page and repetition-loop outliers that wreck a mean, while the mean exposes how bad the tail gets.
- **Interpretation bands** (house defaults, consistent with the `run` phase §6): CER below ~5% is excellent, below ~10% is usable with cleanup, and above that the text needs heavy correction or a different model. These are planning guides, not cited cutoffs — set the operative threshold from what your downstream analysis tolerates.
- **Score every stratum, not just the overall mean.** Aggregate CER/WER by model, by language × model, by decade bracket × model, and by content type × model — because a model can win overall and still fail on tables, on one script, or on the oldest decade.

### 5. Run the Comparison Efficiently

- **Load and unload models sequentially to fit one GPU.** Import torch lazily and release each model (a `gc` pass) before loading the next, so several large VLMs are scored on a single card without holding them all in memory at once. State the exact quantization per model (GPTQ-Int4, NF4, BF16) — it affects both fit and accuracy.
- **Serve via vLLM or Ollama** for batched throughput where the model supports it — a vLLM OpenAI-compatible server in front of the largest open-weight candidate is the usual arrangement; run proprietary APIs through their own rate-limited scripts.
- **Measure speed (pages per hour at the concurrency you will run in production) alongside accuracy**, as context for cost, never as a quality signal. A small specialist is fast partly because it does less: no page-type tags, no rules for boxes or reading order.
- **Make the run resumable and idempotent:** write one output file per page per model and skip pages already done, so a crash partway through the comparison does not restart everything.

### 6. Gate the Bulk Run with Rules Set in Advance

The comparison picks a model; the gate decides the prompt and resolution for it and says go or no-go. In the 2026 production run, the gate found the error that mattered most, and no CER figure showed it.

- **Write the decision rules before the results exist.** Name the pairs and their thresholds (there: CER ≤ 2 % at coverage ≥ 0.75 on 2007 print, ≤ 5 % on 1961 print). Fix a rule for choosing a prompt (the new prompt unless it is worse by more than 0.3 pp on any pair) and a rule for resolution (higher dpi only if it gains at least 0.5 pp). Cap flagged pages at 1 %. Rules written afterwards tend to fit whatever came out.
- **Run a prompt × dpi grid on one server in one job.** Two prompts at two resolutions over 358 pages took under an hour on two A40s. 300 dpi gained less than 0.1 pp CER over 200 dpi at about twice the GPU time, so 200 dpi went to production. Measure this on your own print before paying for 300.
- **Use a second reader from another model family on pages without a twin.** Report per-book disagreement over the content characters. It points to pages; it is not an error rate, because either reader can be wrong. On the highest-disagreement page the difference was where a box went, not which characters were read.
- **Read the highest-disagreement pages against the scans.** That is where the gate found that two prompts rewrote 1957 loanword spellings in their modern form (폴투갈 → 포르투갈, 이태리 → 이탈리아). The twins were elementary books with few loanwords, so their CER could not show it, and it cannot be undone after OCR. Expect the same anywhere a language's spelling changed after the print date. In 18th-century Russian the error ran the other way, adding archaic letters (`run` §3).
- **Turn an eyeball finding into a count you can gate on.** List printed forms and their modern forms from the sample pages and count both in each run. The fixed prompt (spell as printed, with real examples from the pages; `references/prompt-and-schema.md` §d) moved the count from 69 modern / 27 printed to 42 / 45, and most of the remaining "modern" hits were what the books actually print.
- **Fix the prompt once and rerun the gate; stop and report after a second failure.**
- **Keep the gate as the monitoring baseline.** Re-score the twins from the bulk output. They should match the gate within about 0.1 pp; vLLM batching is not fully deterministic even at temperature 0, and a larger gap means the pipeline changed.

### 7. Interpret: There Is No Single Best Model

- **Expect no universal winner.** The lesson of the reference comparison is fit-to-script-and-corpus: on the Latin-script language most models clustered within a couple of percent CER, while on the Korean pages the field split by roughly 25% even among the best. One comparison on one corpus, but the pattern is the reason to run your own. When that happens, pick per script or per era rather than forcing one model.
- **Skill does not transfer across scripts.** A model that reads Polish beautifully can collapse on Korean hanja–hangul. A single-language result says nothing about a script the model was not measured on.
- **The "OCR specialist" is not guaranteed to win.** In that same comparison a document-only OCR model produced the most blank pages and repetition loops, and general-purpose VLMs beat it. Judge on measured CER for *your* pages, not on a system's category label.
- **Open can rival proprietary and also reproduce.** The best open-weight models matched the proprietary APIs while remaining pinnable and re-runnable; the proprietary APIs are fast and capable but change underneath you between versions (the reproducibility argument in the `run` phase §7). Weigh accuracy against reproducibility, not accuracy alone.
- **Decide and document:** the chosen model(s), the threshold they cleared, the strata where they win and lose, and any split (e.g., model A for Polish, model B for Korean).

### 8. Reproducibility and Reporting

- **Publish the model registry** — exact ids, quantization, loaders or dated API identifiers, decoding settings, and seeds — and the ground-truth set (or a precise description of how it was built and transcribed).
- **Report the full results table:** CER and WER, mean and median, `n`, broken down by model and by stratum (language, era, content type), with the normalization recipe stated alongside.
- **Report speed per system** for cost context, with the pages-per-hour basis stated.
- **Report per-model failure modes** — blank pages, repetition loops, garbled or hallucinated script. These are decision-relevant and invisible in an averaged CER.
- Carry the chosen model, the registry, and the normalization recipe forward into the `run` phase; for the methods-section disclosure of the comparison, compose with `$methods-reporting`.

---

## Phase `run`: The Production VLM-OCR Pipeline

For a worked language-specific transcription prompt (pre-reform Cyrillic), a per-page JSON output schema with `uncertain_spans`, `layout_markers`, and `flags`, and the production book-page prompt with a page-type tag and box delimiter, see `references/prompt-and-schema.md`. `scripts/ocr_client.py` is a client for this phase.

### 1. Model Selection

- **The `evaluate` comparison is the selection gate.** Benchmarks and published studies narrow the shortlist (`triage` §3, `references/model-routing.md`); measured error on your own pages decides. Everything below narrows the shortlist that comparison scores.
- **Start from OCR benchmarks, not general VLM leaderboards.** OCRBench (Liu et al. 2024) is saturated, with vendors reporting 900+ of 1,000. OCRBench v2 (Fu et al. 2025), OmniDocBench and olmOCR-Bench cover English and Chinese only. For other languages, MDPBench (real pages, 17 languages) and GlotOCR Bench (100+ scripts, synthetic) are the per-language evidence. General vision-language benchmarks (MMMU, VQAv2) do not predict OCR accuracy.
- **Verify language support explicitly.** Confirm the target language appears in the model's training set with per-language accuracy data. Qwen3-VL (Bai et al. 2025) enumerates 39 languages with OCR benchmarks; models that claim "multilingual support" without language-specific evidence may fail on non-Latin scripts.
- **Compare across models for your script family.** E-ARMOR (2025) compares five VLMs and two traditional OCR systems across 54 languages on a hand-annotated dataset. Use this or similar comparative studies rather than relying on a single model's self-reported scores.
- **Assess quantization tradeoffs before committing.** Low-bit quantization (e.g., W3A16, W4A8) enables single-GPU deployment but can degrade VLM accuracy non-uniformly across modalities. Li et al. (2025) show that **language tokens are an order of magnitude more sensitive to quantization than vision tokens**; treating them equally during calibration over-weights the insensitive modality and hurts performance. Compare quantized output against a full-precision baseline on a pilot sample before a bulk run. Prefer the publisher's own quantized weights (FP8, AWQ, GPTQ): bitsandbytes 4-bit loading failed on a mixture-of-experts VLM in transformers v5, whose fused expert weights it does not quantize (bitsandbytes issue #1849). FP8 weights ran on Ampere GPUs (A40, A100) in vLLM through weight-only kernels.
- **Test the instruct variant against reasoning variants, and turn thinking off in hybrid models.** For OCR tasks, instruction-following models typically outperform chain-of-thought variants, which may add latency and fabricate content rather than improving transcription fidelity. Reasoning models also exhaust the token budget and return empty pages (vertical-Japanese study, arXiv 2511.15059). For hybrid models such as Qwen3.x, disable thinking per request (`chat_template_kwargs: {"enable_thinking": false}`; `ocr_client.py --no-thinking`). Local runtimes can default to the thinking build: Ollama's plain `qwen3-vl:8b` tag is `8b-thinking`, which ignored a request to skip reasoning, spent a 4,096-token budget, and returned an empty page; pull the `-instruct` tag.

### 2. Image Handling and Preprocessing

- **Separate OCR input resolution from archival preservation.** For archival capture, FADGI (2016) prescribes 300-400 ppi across books, journals, and manuscripts (with 400+ ppi for 4-star compliance), and Metamorfoze (van Dormolen 2012) applies similar European standards. For VLM OCR input, resolution requirements are lower but not well-pinned by the KB: calibrate on a pilot, do not drop below ~150-200 ppi, and raise DPI for small type, faded ink, or pre-industrial typography.
- **Prefer native image extraction over rasterization.** Scanned PDFs store each page as an embedded image at the original scan resolution. Extract these byte-for-byte using PDF library methods rather than re-rasterizing, which downsamples and re-encodes (Pitt OCR Best Practices). Reserve rasterization for VLM input when a specific DPI is needed. When rasterizing, use a library that applies the page's `/Rotate` flag and crop box (PyMuPDF's `get_pixmap` does); an extracted image comes as stored, which for some older scans is sideways.
- **Split two-page spreads before OCR** (`triage` §1). A model given a spread may read across the gutter.
- **Start at 200 dpi for print and raise it only on measured gain.** In the 2026 gate, 300 dpi improved CER by less than 0.1 pp on 1950s–60s small type at about twice the GPU time per page.
- **Check what resolution the model actually receives.** Servers resize images to the model's token budget. Gemma 4 in vLLM defaults to 280 image tokens; raising it to 1,120 cut OmniDocBench edit distance from 0.201 to 0.131. Set the budget explicitly per model (`max_pixels` for Qwen, `max_soft_tokens` for Gemma).
- **Test preprocessing on a sample before applying corpus-wide.** Learned image restoration combined with neural post-correction can yield large CER reductions on degraded historical documents — Guan et al. (2025) report 63.9-70.3% CER reduction for the full PreP-OCR pipeline (ResShift image restoration + ByT5 post-correction), not for classical deskew/binarization/contrast alone. Classical preprocessing alone may not help and can actively hurt: Machidon & Machidon (2025) find that grayscale conversion, binarization, and dilation did not improve OCR on degraded folkloristic scans and in some cases introduced artifacts that worsened recognition. Run with and without preprocessing on a diverse sample and compare.
- **Store archival images separately from OCR derivatives.** Save native-resolution images for preservation and generate OCR-resolution images in memory for the VLM. Do not save OCR-resolution rasterizations as the archival copy.

### 3. Prompt Engineering

- **Build language-specific prompts that enumerate expected characters.** For diacritics-heavy languages (Polish, Czech, Vietnamese, Turkish), list every expected diacritical character explicitly in the prompt. For CJK scripts, instruct the model to handle mixed-script content (e.g., Korean hangul with classical Chinese hanja).
- **Specify structured output format.** Instruct the model to output markdown preserving headings, paragraphs, footnotes, and tables. Structured prompts with explicit output format significantly outperform generic "extract text" instructions.
- **Include negative instructions.** "Do not translate," "do not interpret," "do not add content not present in the image." VLMs will summarize, translate, or describe images unless explicitly constrained.
- **Handle page-type edge cases in the prompt.** Instruct the model on what to return for blank pages, illustration-only pages, and pages with only page numbers. Without this guidance, models may hallucinate content for non-text pages (Gbelidji 2026).
- **Tag each page's type on the first line and separate main text from boxes.** A first-line tag (`[PAGE_TYPE: body|toc|front|back|blank]`) lets assembly keep body pages only and gives blank pages a correct answer, where an untagged blank page invites invented text. Main text first, then a delimiter line, then sidebars and captions, keeps a caption from landing inside a sentence. Worked prompt and the residue each rule leaves: `references/prompt-and-schema.md` §d.
- **Guard against modernization on period documents.** A model's language prior can override the image: on 1950s Korean print the model wrote old loanword spellings in their modern form until the prompt said "reproduce the spelling character for character as printed" and gave real examples from the pages (`evaluate` §6). Tell the model to ignore letters from the facing page at the image edge, and to give only the title and caption of maps and figures.
- **Guard against over-historicization on period documents.** VLMs trained with broad historical exposure may project archaic orthography anachronistically. Levchenko (2025) documents GPT-4o inserting historical characters in 59% of 18th-century Russian files regardless of prompt. Validate on the target period and stratify ground-truth sampling by decade (see §6) to detect this failure mode; no prompt will fully suppress it.

### 4. Pipeline Architecture

- **Separate GPU-intensive OCR from CPU-only post-processing.** The minimum viable pipeline has three stages: (1) VLM OCR producing per-page raw text, (2) quality diagnostics classifying problem pages, (3) assembly into combined document-level output. olmOCR (Poznanski et al. 2025) demonstrates this extract-describe-assemble pattern at scale.
- **Integrate diagnostics as automated gates.** Diagnostics should classify each page into action categories (OK, rule-fixable, LLM-fixable, manual review) using language-aware detection: diacritic-to-Latin ratios for European scripts, CJK character ratios for East Asian scripts, repetition density, symbol density, and page length anomalies. These categories are exactly the routing input the `clean` phase consumes.
- **Store all results as structured JSON with full metadata.** Every pipeline stage should output structured data (model name, quantization, DPI, timestamps, per-page results) rather than flat text files. This enables automated aggregation and corpus-level quality dashboards.
- **Design for resumability at the page level.** Append one JSON record per page to one file per document as each page finishes; on restart, skip pages that have a record and let the last record for a page win, so a retry overrides its first attempt. A job killed at hour 20 then loses minutes, not books, and a resubmitted job needs no bookkeeping.
- **Serve the model and send pages concurrently.** A vLLM (or SGLang) server batches concurrent requests; a client with 16–32 requests in flight per server keeps the GPU busy. When the model fits on one GPU, run one server per GPU and spread pages across them; that roughly halves wall-clock time on two GPUs. Use tensor parallelism only for a model that does not fit.

### 5. Batch Strategy and Resource Planning

- **Calibrate GPU-hour estimates from a measured run.** Process 10-20 pages, measure per-page time, multiply by corpus page count, and add 30% buffer for variance and failed retries. Do not rely on model documentation or theoretical throughput.
- **With a served model, run one job per server session over a manifest, not one job per document.** Loading a 35B model from network storage took 3–8 minutes, longer than many books take to read. Order the manifest by priority (benchmark pairs, then in-scope books, then the rest) so a job that dies has finished the books that matter; page-level resume handles the rest.
- **Decode deterministically and budget for the densest page.** Temperature 0, a fixed seed, and a `max_tokens` budget that fits the densest page (8,192 tokens for dense textbook pages). Re-run pages that end in a repetition loop or hit the limit once with a mild repetition penalty (1.05), then trim loops that remain. Keep the penalty mild and confined to the retry: strong penalties corrupt tables and legitimately repeated characters. In the main 2026 run, 76 of 25,043 pages needed the retry and 45 still looped or truncated and were trimmed. An earlier DeepSeek-OCR run of the same books, without such a pass, left loop junk in up to 14.6 % of a book.
- **Check completeness, not exit codes.** Per document: pages with a record equal the pages requested, zero error records, the retry count, the flagged-page share, and the page-type distribution. Books with more than 5 % flagged pages or a body-page share well under 80 % go on a re-run list; read a few of their pages before re-running.
- **Use the tranche/gate pattern.** Split the corpus into a small test tranche (3-5 documents per language) and bulk tranches. Complete accuracy evaluation on the test tranche before committing GPU-hours to bulk runs. This is the single most important resource management decision.
- **Handle large documents explicitly.** With page-level resume, a book that outlasts the wall-clock limit continues in the next job. Without it, split the book into page-range chunks that write to the same output directory, and merge the chunks at assembly.
- **Track all jobs in a manifest.** Maintain a CSV or database mapping each document to its tranche, job ID, status, GPU-hours consumed, and quality metrics. This supports both operational monitoring and post-hoc reporting.

### 6. Accuracy Evaluation

- **Combine ground-truth sampling with automated proxies.** Human-transcribed ground truth with CER/WER computation gives a rigorous accuracy number; dictionary-based hit rates give a scalable quality signal across every page. Neither alone is sufficient.
- **Re-score the twins from the bulk output** and compare with the gate (`evaluate` §6).
- **Monitor with a stratified sample, reusing the `evaluate` design.** The stratification scheme, normalization recipe, and CER/WER implementation from `evaluate` §3-4 carry over unchanged. For ongoing monitoring of a pipeline in production, 20-30 pages per language is a practical minimum for a reliable CER estimate (Levchenko 2025); that is separate from the up-front selection sample.
- **Document the evaluation tool.** CER/WER scores differ across evaluation tools due to normalization differences (whitespace handling, Unicode normalization, punctuation treatment). Neudecker et al. (2021) demonstrate that tool choice changes reported accuracy. Specify which tool you used, which normalization was applied, and whether the comparison was case-sensitive.
- **Acknowledge CER/WER limitations.** Character-level edit distance does not capture layout errors, semantic correctness, or structural fidelity. A model can scramble column order while achieving low CER (Beyene & Dancy 2026). Supplement with dictionary hit rates, manual inspection of representative pages, and downstream task performance.
- **Set go/no-go thresholds relative to downstream needs**, using the interpretation bands from `evaluate` §4 as a starting point. van Strien et al. (2020) show that the impact of OCR quality on downstream NLP tasks is task-specific (topic modeling, NER, dependency parsing, and retrieval degrade at different thresholds), so the right threshold depends on which downstream task consumes the text.

### 7. Reproducibility and Documentation

- **Record every pipeline parameter as JSON alongside the output**, per the provenance rules above.
- **Produce per-document processing reports.** Each document should have a JSON report recording pipeline stages completed, timestamps, page counts (processed, failed), quality summary, and output file manifest.
- **Aggregate into a corpus-level batch summary.** A single CSV mapping all documents to their quality metrics, processing metadata, and tranche membership supports both quality monitoring and methods reporting.
- **Archive the complete pipeline code and prompts**, with pinned dependencies and the hub commit hash for each model.
- **Treat hosted-API non-determinism as a reproducibility hazard.** Levchenko (2025) measured coefficient-of-variation (CV) of daily word-accuracy over seven days and found roughly a 10x spread across models (e.g., CV=0.307 vs. 0.037). Commercial hosted APIs can silently change underneath you. Barrie, Palmer & Spirling (2025) generalize the point for political-science LM work: temperature=0 does not fix it, many LM-based pipelines fail the re-runnable and repeatable sub-standards of replication, and the disciplinary recommendation is locally-hosted, versioned open-weight models. Prefer local open-weight models pinned to a specific revision when publication-grade reproducibility is required; otherwise, report the evaluation window and replicate the pilot run before and after any bulk campaign.
- **Hand off.** Pass raw per-page output to the `clean` phase (LLM-based correction, constrained decoding, Unicode normalization, provenance). Before publication, audit the pipeline documentation with the `$methods-reporting` skill (APSA/JARS/DA-RT standards for methods sections).

---

## Phase `clean`: Post-OCR Text Cleanup for Research Corpora

### 1. Cleanup Strategy Selection

- **Characterize the error-generating DGP before selecting a method.** Document source language(s), era, typeface family (Fraktur, Antiqua, typewritten, handwritten), scan DPI, OCR engine, and domain jargon. Each parameter constrains which corrections are plausible and which risk introducing semantic drift. When the text came from the `run` phase, most of this is already in the per-page `pipeline` record.
- **Choose between LLM correction, rule-based fixes, or a hybrid pipeline based on error type.** LLM correction excels at context-dependent errors (wrong but plausible characters, broken words, missing diacritics). Rule-based fixes handle deterministic patterns (control characters, Unicode normalization, repetition artifacts, whitespace) with zero risk of content alteration. Use rule-based fixes unconditionally for these categories.
- **Default to the hybrid approach for research corpora.** Run LLM correction first on all pages, then apply deterministic rule fixes on top. This order matters: LLM correction may introduce formatting artifacts that rule fixes clean up, while the reverse order wastes rule-fix effort on text the LLM will rewrite (Machidon & Machidon 2025).
- **Pilot-test LLM correction per language before corpus-wide deployment.** LLM post-correction effectiveness is highly language-dependent: English achieves 7-58% CER reduction across open models, while Finnish shows negative or near-zero improvement across the same model set (Kanerva et al. 2025). Validate each language separately.
- **Keep a stage only if it measurably helps.** Score raw, rules, spacing and LLM-corrected text against the twins, stage by stage, and keep a stage only when it lowers CER without lowering coverage. On modern print read at 1–3 % CER, the 2026 pipeline needed no LLM pass.
- **Consider whether correction is needed at all.** Define the quality threshold before choosing a strategy. The Hill & Hengchen 70-80% quality band (reported in van Strien et al. 2020) marks the critical threshold below which most downstream NLP tasks perform poorly; above 80% quality many tasks (e.g., topic modeling) tolerate residual noise. If the downstream analysis sits comfortably above this band, the risk of correction-introduced errors may outweigh the benefit.

### 2. Remove Model Artifacts, and Audit Every Rule That Deletes Text

Post-processing is where a good OCR run loses text without anyone noticing. In the 2026 Korean pipeline, three cleaning rules each passed review and each deleted real text across the corpus. No summary statistic showed it; checking deletions against the scans did.

- **Strip markup by a whitelist of tag names, never by a generic pattern.** A `<[^>]+>` stripper removed every angle-bracketed span. Korean books print titles, citations and dates in angle brackets (`<삼국사기>`, `<1960. 4. 19.>`), so about 4,500 of them were gone from every book, and an unmatched `<` swallowed text up to the next `>` across lines: 37,000 characters of one book.
- **Positional heuristics need evidence from repetition.** A rule that treated a short, unpunctuated line next to a page number as a running head deleted the last line of most pages in books set at about 25 characters a line (315 lines in one book). Count a line as a running head only when it recurs next to the page number on three or more pages of the same book.
- **Junk filters must spare unusual layouts that are real.** A filter for stray letters bleeding in from the facing page dropped classical Chinese quotations printed vertically, one character per line (a 131-character passage). Join such runs instead of dropping them.
- **Cross-page joins are an error source.** Joining a paragraph that ends mid-sentence to the next page's first paragraph misfired on box-heavy pages and cost 0.5–1.1 pp CER, the whole gap between raw and cleaned text on those books.
- **Audit each rule.** Log the characters each rule removes per book and read the largest removals against the scans. Diff raw against cleaned text on a random sample of pages. Re-score the twins after every change to post-processing: CER, the aligned share of OCR text, and reference-side recall together (`evaluate` §4). Fixing the tag stripper and the running-head rule raised one pair's aligned share from 0.95 to 0.97 and cut its CER from 3.32 % to 3.05 %.
- **Remove model artifacts from a list, then scan the final corpus until the scan finds none.** Models emit placeholders the prompt never asked for. Examples: `[Figure caption]`, `[Image 1]`, `<그림>`, `(No text found on the page)`, a second delimiter, an echoed page-type tag, and captions wrapped in English (`[Figure: Soldiers marching]`). In a non-English book, a box paragraph with six or more Latin-script words and no target-script characters was an invented English description of a figure.
- **Treat text on picture pages as low-trust.** In a check of 16 picture pages, the model gave one wordless page invented captions and misread the text of one poster. Check a sample of picture-heavy pages against the scans and state the limitation with the corpus.
- **Fix in post-processing, not by re-OCR.** Every fix above was applied by re-running CPU post-processing on the stored page records; the affected books were rebuilt without new OCR.
- **Recompute derived text only for changed documents, with pinned tokenizer versions.** Re-running a newer Kiwi over the whole corpus tokenised unchanged books differently from the published version (중고사 → 고사), which would have shifted every analysis input.

### 3. LLM-Based Correction

- **For most pages, use a small text-only model.** The correction input is already text; image understanding is not needed for well-OCR'd pages. A 7-13B parameter model with 4-bit quantization fits in ~4-20GB VRAM and runs on a single GPU. Larger fp16 models (e.g., Llama-3.1-70B at fp16 yielding ~42% CER reduction vs ~39% at 4-bit) gain 2.5-4.7pp but require roughly 3x the memory (132GB vs 43GB) and often a second GPU (Kanerva et al. 2025).
- **For severely degraded pages, use multimodal correction.** Feeding both the original page image and the OCR text to a correction model can achieve below 1% CER on degraded documents, but doubles GPU cost (Greif et al. 2025). Reserve this for flagged pages, not routine processing.
- **Write tight correction prompts.** Instruct the model to "fix clear OCR mistakes only: wrong characters, broken words, garbled punctuation, repetition artifacts. Do not translate, modernize, or add anything. Output the corrected text only." Loose prompts invite hallucination.
- **Supply socio-cultural context in the prompt.** Including document era, publication type, language register, and genre (e.g., "The text is from an English newspaper in the 1800s") meaningfully reduces CER beyond generic correction prompts — the top-performing CLOCR-C configuration achieved over 60% CER reduction on the NCSE dataset using a modular prompt that combines expert framing, recovery instructions, publication context, text-type context, and anti-overgeneration instructions (Bourne 2024). Misleading or mismatched context degrades performance, so use the real document metadata.
- **Add language-specific instructions.** For Polish, explicitly mention diacritics restoration (ą, ć, ę, ł, ń, ó, ś, ź, ż). For Korean, mention hangul integrity and hanja preservation. The correction model needs to know which character set to favor.
- **Mitigate hallucination with constrained decoding.** Constrained decoding techniques — beam search with CER-based re-ranking, sequence-level similarity re-ranking, and token-level Constrained Beam Search that interpolates the model's distribution with a character-similarity distribution — enforce fidelity between input and output and prevent plausible-but-fabricated substitutions (Sastre et al. 2025). Prefer token-level CBS with dynamic α if model logits are accessible; otherwise fall back to beam search with CER re-selection. This matters because WER can worsen even when CER improves: fine-tuning alone in Sastre et al. left CER roughly flat (0.314→0.321) while WER jumped from 0.633 to 0.821, a failure mode constrained decoding directly addresses.
- **Use worked prompt templates and a provenance schema.** See `references/prompt-templates-and-schema.md` for a minimal constrained-decoding-friendly baseline prompt, a Bourne-style socio-cultural-context prompt, and a span-level JSONL provenance schema (per Guo & Wei 2026 §3.2/§3.3).
- **Strip LLM overgeneration with alignment-based post-processing.** Llama-family models routinely prepend "Here is the corrected text:" or append error-by-error explanations. Without post-hoc trimming (character-level local alignment of output against input, keeping only the aligned region), Llama-3-8B scored -74.1% CER; with trimming, +7.3% (Kanerva et al. 2025). Gemma and GPT-4o are largely unaffected, but the step is cheap; apply it to every model.
- **Disable chain-of-thought for correction tasks.** Reasoning modes add latency without improving transcription fidelity. Use low-temperature sampling or greedy decoding for deterministic output.
- **Tune segment length for corpus-scale processing.** Short segments (50-100 words) score notably worse CER% across models; 200-300 words appears optimal for page-level correction (Kanerva et al. 2025). When splitting long documents, use a stride that preserves left context (left-uncorrected-concatenate parallelizes cleanly; left-corrected-concatenate is sequential but slightly better at segment boundaries).
- **Track all changes with edit-distance metrics.** Compute Levenshtein distance and change ratio (edit distance / original length) per page. Flag pages where the correction model altered more than 10% of characters for manual review — high change ratios may indicate hallucination rather than correction. This 10% threshold is an operational heuristic; calibrate against your pilot evaluation.

### 4. Rule-Based Fixes

- **Apply deterministic fixes in a fixed order, and audit each one (§2).** (1) Control character removal; (2) zero-width and invisible character removal, keeping the joiners (U+200C, U+200D) that Persian, Arabic and Indic scripts use; (3) NFC Unicode normalization; (4) loop trimming, applied only to runs the loop detector flagged, never to digits (10000) or leaders; (5) standalone symbol line removal; (6) whitespace normalization. This ordering prevents interactions between fixes.
- **Store NFC, never NFKC.** NFKC turns ① into 1, ſ into s, ﬅ into st and ㈜ into (주), which is wrong for a stored corpus. Even NFC merges CJK compatibility ideographs (U+F900–FAFF, U+2F800–2FA1F) into their unified forms, and Korean uses them to mark readings of the same hanja; exclude those ranges or keep the raw string alongside (UAX #15). Score with the recipe declared in `evaluate` §4; if you also report a score after NFKC folding, label it separately, since folding hides long-s, ligature and compatibility-character errors.
- **Never collapse repeated characters blindly.** Collapsing runs of 4+ identical characters to 3 turns 10000 into 1000 and damages leaders, tables, and scripts with legitimate long runs. Trim only what the loop detector flagged, and check the trims against the scans.
- **Rule-based diacritics restoration is viable for some languages.** For Polish, rule-based approaches (removing word breaks, rejecting case-changing corrections, restoring diacritical characters replaced with visually similar ASCII) are competitive with LLM-based correction and more predictable (Ogrodniczuk 2022).
- **Generate synthetic OCR errors for training when ground truth is scarce.** Glyph-similarity-based synthetic corruption (feature-matched character confusions) produces more realistic training data than random-injection baselines, and outperforms in low-resource languages (Guan & Greene 2024).

### 5. Quality Diagnostics and Metrics

- **Move beyond CER/WER as the sole quality measure** (limitations in `run` §6; normalization choices such as ligature, Unicode-compatibility, and PUA handling also shift the numbers — Beyene & Dancy 2026; Neudecker et al. 2021).
- **Use precision as a primary metric for historical and archival corpora.** CER and WER emerged from speech recognition, where insertions and deletions are symmetric. Historical and archival research is asymmetric: false positives (hallucinated tokens, invented entities) are more costly than false negatives (missed content), because historians already expect absence. Precision on downstream tasks (e.g., NER precision, entity similarity) often aligns better with analytic needs than CER/WER and can show improvement even when CER/WER indicate regression (Backer & Hyman 2025).
- **Build a multi-signal diagnostic profile per page.** Character composition ratios (diacritics-to-Latin for European scripts, CJK character ratios for East Asian), repetition artifact density, symbol density, and page length anomalies (empty, suspiciously short, suspiciously long) each capture different failure modes.
- **Use dictionary hit rates as an automated quality proxy.** Tokenize OCR output and check against morphological dictionaries or analyzers. Compute per-page and per-document valid-token rates. This scales to every page in the corpus without human effort.
- **Classify pages by recommended action.** Map diagnostic signals to action categories: OK (no intervention), rule-fixable (deterministic cleanup sufficient), LLM-fixable (context-dependent errors), manual review (critical failures). This prioritizes human attention on the pages that need it most, and it matches the routing categories the `run` phase §4 already assigns.

### 6. Multilingual Considerations

- **Check diacritic ratios for Latin-script languages.** For Polish, a page of body text with zero diacritical characters almost certainly has OCR errors. Flag pages where the diacritic-to-alphabetic ratio drops below a language-calibrated threshold (Ogrodniczuk 2022).
- **Treat Korean spacing as a distinct post-OCR task.** Korean uses space-delimited eojeol units, and OCR frequently merges or splits them incorrectly. Dedicated syllable-and-morpheme spacing models (Choi & Kim 2021) address this error type specifically and may outperform general-purpose LLM correction, though direct LLM benchmarks on this task are not well-established. Kiwi (`kiwipiepy`, `space()`) is the practical tool; score spacing separately from characters (`evaluate` §4) to see whether it helps on your print, and keep historical spacing where the print predates the current rules.
- **Use morphological analyzers as correction validators.** Morfeusz for Polish, Mecab-ko for Korean — tokens that parse successfully are likely correct; tokens that fail to parse are OCR error candidates. This provides both a diagnostic signal and a correction filter.
- **Protect dialectal and archaic text from normalization.** Correction models trained on standard modern language may silently replace historical or dialectal tokens with modern near-neighbors, introducing semantic drift (e.g., Machidon & Machidon 2025 document *žlahnega* → *glavnega* in Slovene folkloristic text; Kanerva et al. 2025 document historical long-s and v/w substitutions). Test on a sample of the oldest and most linguistically distinctive documents before corpus-wide deployment, and disable normalization flags that modernize orthography.

### 7. Corpus-Level Quality Assurance

- **Implement a three-tier review workflow.** (1) Automated pass/fail based on diagnostic thresholds applied to all documents, (2) spot-check review of flagged documents (10-15% of corpus), (3) deep review of a random sample of passing documents (2-5% of corpus) to catch false negatives.
- **Define specific flagging thresholds.** Mean quality score below 0.80, LLM correction change ratio above 10%, dictionary hit rate below 80%, or more than 5% empty pages. These are operational defaults, not empirically derived cutoffs — calibrate against your pilot evaluation and pre-register the final values.
- **Route flagged documents to specific remediation actions.** Re-run LLM cleanup with a different prompt, re-OCR at higher DPI or without quantization (back to the `run` phase), or escalate to manual transcription. Each action has different cost and quality implications.
- **Produce a corpus-level quality dashboard.** Aggregate per-document metrics into a summary CSV or report: document ID, language, page count, mean quality score, dictionary hit rate, correction change ratio, flag status, review outcome. This supports both operational monitoring and methods reporting.

### 8. Provenance and Documentation

- **Maintain a complete audit trail of all corrections.** Each correction should be attributed to its source (LLM model version, rule name) with before/after text preserved at the page level (Guo & Wei 2026). Correction pathways can substantially alter extracted entities and downstream interpretations.
- **Log model details for the LLM correction stage.** Model name, quantization method, prompt text, generation parameters (temperature, max tokens, sampling), and per-page edit-distance metrics. This is the minimum required to reproduce or audit the correction.
- **Log rule-fix details.** Which rules fired and how many characters each rule changed per page. This enables downstream researchers to assess whether rule fixes were aggressive or conservative for a given document.
- **Produce a cleanup comparison artifact.** A CSV or JSON with page-level before/after text pairs and metrics (edit distance, change ratio, flagged status) enables downstream researchers to assess correction quality and choose their preferred text version.
- **Record all thresholds and human review outcomes.** Sampling decisions, flagging thresholds, remediation actions, and human review results should be documented in a methods section alongside the corpus, not just in internal notes.
- **Pre-register the correction strategy when downstream inference depends on cleaned text.** Correction pathways can substantially alter extracted entities — Guo & Wei 2026 show that raw, fully-corrected, and provenance-filtered variants of the same corpus yield materially different NER inventories (176 volatile entities in their pilot). Correction-stack flexibility (prompt wording, trust-policy threshold, model version) is a researcher-degrees-of-freedom problem in the Simmons et al. 2011 sense: each un-documented choice is a forking path that can shift downstream inferences. Pre-registration is the standard remedy (Nosek et al. 2018). When cleaned text feeds named-entity-based, topic-based, or embedding-based inferential analyses, pre-register the correction model, prompt, decoding configuration, and provenance-filter trust policy alongside the analysis plan (cross-reference the `$pre-registration-writing` skill).

---

## Quality Checks

### `triage`

- [ ] Every document inventoried (`triage.csv`): kind of text layer (including invisible earlier OCR), duplicates, `/Rotate` flags, landscape spreads, scan resolution
- [ ] Files reconciled with the catalogue (duplicate scans, reprints, missing scans checked against title pages)
- [ ] Script and language established per document from the contact sheets plus a script count and language ID on text (text layer or pilot read); no Tesseract script detection
- [ ] Secondary scripts and layout risks (columns, vertical text, margin headings, tables, maps, picture pages) listed for the prompt
- [ ] Shortlist per script family from the dated `references/model-routing.md`, at least two VLM families plus a small specialist
- [ ] Hardware route chosen from corpus pages ÷ measured pages per hour, plus about 30 % for retries
- [ ] Data terms checked before any hosted API is shortlisted
- [ ] Born-digital twins searched for, edition match checked by title page and alignment in both directions, and split into dev and test pairs

### `evaluate`

- [ ] Comparison run on a human-transcribed sample before any bulk OCR; model choice treated as empirical, not as a default
- [ ] Candidate set spans open-weight VLMs from different families + a proprietary API where data terms allow + a small document-OCR specialist as the cheap baseline; VLM candidates chosen from OCR benchmarks, not general leaderboards
- [ ] Twin pairs scored on aligned spans: conditional CER, aligned OCR share, and reference-side recall reported; CER on content characters, spacing scored separately
- [ ] Ground truth stratified on script/language, era, and content type (body, tables, illustrations, degraded, front matter)
- [ ] ~50–100 pages (house default) with enough pages per stratum cell to be informative; one UTF-8 `.txt` per page id
- [ ] Ground truth transcribed faithfully (scripts and diacritics preserved) and before viewing any model output
- [ ] Normalization recipe declared before scoring (NFC, case sensitivity, markdown/whitespace handling) and applied identically to every system
- [ ] CER and WER computed as edit-distance ratios (Levenshtein 1966); mean and median reported with `n`
- [ ] Accuracy reported per stratum (model × language, × era, × content type), not just an overall mean
- [ ] Interpretation thresholds stated as house defaults tied to downstream tolerance, not as cited cutoffs
- [ ] Models loaded/unloaded sequentially (or served) to fit hardware, with quantization recorded; run resumable, one file per page per model
- [ ] Speed reported as pages per hour at production concurrency, as cost context only
- [ ] Gate decision rules (pair thresholds, prompt rule, dpi rule, flag cap) written before the results
- [ ] Second reader from another family run on pages without a twin; highest-disagreement pages read against the scans
- [ ] Spelling modernization counted with printed/modern pairs from the sample pages for any print older than the current orthography
- [ ] Per-model failure modes (blank pages, repetition loops, garbled script) reported alongside CER
- [ ] No single-best model assumed: fit-to-script documented and any per-script/era model split stated
- [ ] Model registry, ground-truth set, normalization recipe, and seeds archived for reproducibility (compose with `$methods-reporting`)

### `run`

- [ ] Model benchmarked for task: VLM selected based on document-OCR benchmarks (OCRBench or equivalent), not general VLM leaderboards (Liu et al. 2024; Fu et al. 2025)
- [ ] Language support verified: Target language confirmed in the model's explicit training set with per-language accuracy data (Bai et al. 2025)
- [ ] Quantization tradeoff assessed: If using 4-bit or 8-bit quantization, accuracy impact measured on a pilot sample against full-precision baseline (Li et al. 2025)
- [ ] DPI justified: OCR input DPI calibrated on a pilot (not dropped below ~150-200 ppi without evidence), with archival images stored separately at FADGI/Metamorfoze targets (FADGI 2016; van Dormolen 2012)
- [ ] Native extraction preferred: Embedded images extracted byte-for-byte from scanned PDFs rather than re-rasterized, when available
- [ ] Rendering applies `/Rotate`; two-page spreads split before OCR
- [ ] Prompt tags page type, separates main text from boxes, and tells the model to spell as printed with real examples from the pages; thinking disabled in hybrid models
- [ ] Page-level resume: one append-only record per page; served model with concurrent requests, one server per GPU when the model fits
- [ ] Deterministic decoding (temperature 0, seed), a token budget for the densest page, one retry with a repetition penalty for loops and truncations
- [ ] Completeness checked per document (records = pages requested, zero errors, flagged share, page-type distribution); twins re-scored from the bulk output and compared with the gate
- [ ] Preprocessing tested on sample: Any image preprocessing (classical or learned restoration) validated on a diverse sample before corpus-wide application; headline CER reductions from PreP-OCR-style pipelines reflect combined restoration + post-correction, not classical preprocessing alone (Guan et al. 2025; Machidon & Machidon 2025)
- [ ] Prompts are language-specific: OCR prompts explicitly name the script system, enumerate expected diacritics or character sets, and include negative instructions
- [ ] Pipeline stages separated: GPU-intensive OCR decoupled from CPU-only diagnostics and assembly, with structured JSON output at each stage
- [ ] Diagnostics integrated: Automated quality diagnostics classify every page by action category with language-aware character detection
- [ ] Resource estimate calibrated: GPU-hours estimated from a measured calibration run, not assumed from model documentation
- [ ] Test tranche gated: Accuracy evaluation completed on a test tranche before committing to bulk GPU-hours
- [ ] Ground truth sampled: Human-transcribed ground truth created for a stratified sample of pages, with CER/WER computed and reported (Levchenko 2025)
- [ ] Evaluation tool documented: CER/WER tool identified and normalization choices recorded, given known tool discrepancies (Neudecker et al. 2021)
- [ ] Pipeline fully documented: Model version, quantization, DPI, prompts, generation parameters, and software versions recorded in machine-readable format
- [ ] Model stability acknowledged: If using a hosted API, evaluation window recorded and pilot re-run before and after the bulk campaign; publication-grade corpora use pinned open-weight models (Levchenko 2025; Barrie, Palmer & Spirling 2025)
- [ ] Processing reports generated: Per-document JSON reports and corpus-level batch summary CSV produced and archived

### `clean`

- [ ] DGP characterized: Source language(s), era, typeface, scan DPI, OCR engine, and domain documented before method selection
- [ ] Strategy justified: Cleanup approach (LLM, rule-based, or hybrid) chosen based on error types, corpus size, and resource constraints
- [ ] LLM correction pilot-tested per language: Cleanup validated on a sample from each language before corpus-wide application (Kanerva et al. 2025)
- [ ] Socio-cultural context supplied in prompts: Document era, publication type, and genre included; misleading context avoided (Bourne 2024)
- [ ] Segment length tuned: Input segments of 200-300 words used; boundary concatenation strategy chosen (Kanerva et al. 2025)
- [ ] Overgeneration stripped: Alignment-based trimming applied to LLM outputs to remove "Here is the corrected text:" preambles and trailing commentary (Kanerva et al. 2025)
- [ ] Hallucination risk mitigated: Constrained decoding (token-level CBS preferred; beam + CER re-rank as fallback) applied to prevent fabricated content (Sastre et al. 2025)
- [ ] Change ratio tracked: Per-page edit distance and change ratio computed and stored; pages exceeding the flagging threshold (default 10%) reviewed
- [ ] Rule-based fixes ordered correctly: Deterministic fixes applied in the prescribed sequence (control chars, zero-width, NFKC, repetitions, symbols, whitespace)
- [ ] Every deleting rule audited: characters removed per rule per book, raw-vs-cleaned diffs on sampled pages, twins re-scored (CER and reference-side recall) after each post-processing change
- [ ] Markup stripped by whitelist; running heads removed only when they recur across pages; unusual real layouts (vertical quotations) kept
- [ ] Model placeholders and invented captions removed and the final corpus scanned until it shows none; picture-page text flagged as low-trust
- [ ] Corpus stored in NFC with CJK compatibility ideographs protected; one declared scoring recipe across phases, with any NFKC-folded score labelled separately
- [ ] Derived text (tokenized, lemmatized) recomputed only for changed documents, with the tokenizer version pinned
- [ ] Metrics go beyond CER/WER: Quality assessed using multiple signals (precision for historical corpora, character composition, dictionary hit rates, diagnostic flags), not CER/WER alone (Backer & Hyman 2025; Beyene & Dancy 2026; Neudecker et al. 2021)
- [ ] Downstream impact considered: Quality thresholds set relative to the intended analysis and the 70-80% critical quality band (van Strien et al. 2020), not abstract accuracy targets
- [ ] Language-specific patterns addressed: Diacritics ratios, morphological parsing, and spacing rules checked for each language in the corpus
- [ ] Dialectal and archaic text protected: Correction models tested for damage to non-standard language varieties; modernization flags disabled where relevant (Machidon & Machidon 2025)
- [ ] Flagging thresholds defined and calibrated: Numeric thresholds (quality score, change ratio, dictionary hit rate, empty page rate) set and calibrated against pilot evaluation
- [ ] Stratified human review conducted: Review sample stratified by language, document age, print quality, and flag category; sampling fraction justified
- [ ] Both raw and cleaned text preserved: Original OCR output retained alongside every cleanup stage for auditability
- [ ] Correction provenance logged: Each correction attributed to its source (LLM model, rule name) with before/after text, edit type, confidence, and review status (Guo & Wei 2026)
- [ ] Correction strategy pre-registered: When cleaned text feeds inferential analyses, the correction model, prompt, decoding configuration, and trust policy are pre-registered alongside the analysis plan
- [ ] Cleanup comparison artifact produced: Page-level CSV or JSON with raw text, cleaned text, and per-page metrics archived
- [ ] Methods documented: All thresholds, sampling decisions, model versions, prompts, and human review outcomes recorded
