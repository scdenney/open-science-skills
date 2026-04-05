---
name: vlm-ocr-pipeline
description: Guide setup and execution of a VLM-based OCR pipeline for scanned historical and multilingual documents. Covers model selection, image handling, prompt engineering, batch processing, and accuracy evaluation. Use when (1) selecting a vision-language model for document OCR, (2) deciding on DPI and image extraction strategy for scanned PDFs, (3) writing language-specific OCR prompts for a VLM, (4) designing a multi-stage OCR pipeline with diagnostics, (5) planning batch OCR on HPC or SLURM infrastructure, (6) estimating GPU-hours and VRAM for a document corpus, (7) evaluating OCR accuracy with CER/WER and dictionary proxies, or (8) documenting an OCR pipeline for reproducibility.
argument-hint: "[describe your document corpus, languages, and compute environment]"
---

# VLM-Based OCR Pipeline for Scanned Document Corpora

## Instructions

### 1. Model Selection

- **Start from OCR benchmarks, not general VLM leaderboards.** OCRBench (Liu et al. 2024) tests across 29 document OCR dimensions; OCRBench v2 (Fu et al. 2025) extends to multilingual scripts and multi-page documents. General vision-language benchmarks (MMMU, VQAv2) do not predict OCR accuracy.
- **Verify language support explicitly.** Confirm the target language appears in the model's training set with per-language accuracy data. Qwen3-VL (Bai et al. 2025) enumerates 39 languages with OCR benchmarks; models that claim "multilingual support" without language-specific evidence may fail on non-Latin scripts.
- **Compare across models for your script family.** E-ARMOR (2025) compares five VLMs and two traditional OCR systems across 54 languages on a hand-annotated dataset. Use this or similar comparative studies rather than relying on a single model's self-reported scores.
- **Assess quantization tradeoffs before committing.** 4-bit NF4 quantization enables single-GPU deployment but degrades OCR accuracy by approximately 2-5%. Vision tokens are more quantization-sensitive than language tokens (Li et al. 2025). Always compare quantized output against a full-precision baseline on a pilot sample.
- **Test the instruct variant against reasoning variants.** For OCR tasks, instruction-following models typically outperform chain-of-thought variants, which may add latency and fabricate content rather than improving transcription fidelity.

### 2. Image Handling and Preprocessing

- **Separate OCR input resolution from archival preservation.** For VLM OCR input, 200 DPI is sufficient for modern print; use 300 DPI for pre-1970s or degraded documents. For archival preservation, FADGI (2016) prescribes 300-400 DPI and Metamorfoze (van Dormolen 2012) applies similar European standards.
- **Prefer native image extraction over rasterization.** Scanned PDFs store each page as an embedded image at the original scan resolution. Extract these byte-for-byte using PDF library methods rather than re-rasterizing, which downsamples and re-encodes (Pitt OCR Best Practices). Reserve rasterization for VLM input when a specific DPI is needed.
- **Test preprocessing on a sample before applying corpus-wide.** Classical image preprocessing (deskewing, binarization, contrast enhancement) can reduce CER by 60-70% on degraded historical documents (Guan et al. 2025) but may hurt clean modern scans. Run with and without preprocessing on a diverse sample and compare.
- **Store archival images separately from OCR derivatives.** Save native-resolution images for preservation and generate OCR-resolution images in memory for the VLM. Do not save OCR-resolution rasterizations as the archival copy.

### 3. Prompt Engineering

- **Build language-specific prompts that enumerate expected characters.** For diacritics-heavy languages (Polish, Czech, Vietnamese, Turkish), list every expected diacritical character explicitly in the prompt. For CJK scripts, instruct the model to handle mixed-script content (e.g., Korean hangul with classical Chinese hanja).
- **Specify structured output format.** Instruct the model to output markdown preserving headings, paragraphs, footnotes, and tables. Structured prompts with explicit output format significantly outperform generic "extract text" instructions.
- **Include negative instructions.** "Do not translate," "do not interpret," "do not add content not present in the image." VLMs will summarize, translate, or describe images unless explicitly constrained.
- **Handle page-type edge cases in the prompt.** Instruct the model on what to return for blank pages, illustration-only pages, and pages with only page numbers. Without this guidance, models may hallucinate content for non-text pages (Gbelidji 2026).

### 4. Pipeline Architecture

- **Separate GPU-intensive OCR from CPU-only post-processing.** The minimum viable pipeline has three stages: (1) VLM OCR producing per-page raw text, (2) quality diagnostics classifying problem pages, (3) assembly into combined document-level output. olmOCR (Poznanski et al. 2025) demonstrates this extract-describe-assemble pattern at scale.
- **Integrate diagnostics as automated gates.** Diagnostics should classify each page into action categories (OK, rule-fixable, LLM-fixable, manual review) using language-aware detection: diacritic-to-Latin ratios for European scripts, CJK character ratios for East Asian scripts, repetition density, symbol density, and page length anomalies.
- **Store all results as structured JSON with full metadata.** Every pipeline stage should output structured data (model name, quantization, DPI, timestamps, per-page results) rather than flat text files. This enables automated aggregation and corpus-level quality dashboards.
- **Design for resumability.** Jobs fail. The pipeline should detect already-processed documents and skip them on re-run. Store a completion marker (e.g., `results_raw.json`) per document so partial runs can resume without re-processing.

### 5. Batch Strategy and Resource Planning

- **Calibrate GPU-hour estimates from a measured run.** Process 10-20 pages, measure per-page time, multiply by corpus page count, and add 30% buffer for variance and failed retries. Do not rely on model documentation or theoretical throughput.
- **Structure batch processing as one job per document.** This minimizes job scheduling overhead, simplifies failure recovery (re-run one document, not one page), and produces self-contained output directories.
- **Use the tranche/gate pattern.** Split the corpus into a small test tranche (3-5 documents per language) and bulk tranches. Complete accuracy evaluation on the test tranche before committing GPU-hours to bulk runs. This is the single most important resource management decision.
- **Handle large documents explicitly.** Books exceeding the job wall-clock limit should be split into page-range chunks submitted as separate jobs writing to the same output directory. The assembly stage must merge chunks.
- **Track all jobs in a manifest.** Maintain a CSV or database mapping each document to its tranche, job ID, status, GPU-hours consumed, and quality metrics. This supports both operational monitoring and post-hoc reporting.

### 6. Accuracy Evaluation

- **Combine ground-truth sampling with automated proxies.** Human-transcribed ground truth with CER/WER computation gives a rigorous accuracy number; dictionary-based hit rates give a scalable quality signal across every page. Neither alone is sufficient.
- **Stratify the ground-truth sample.** Select pages spanning languages, decades (older print is harder), print quality (faded vs. clean), and content type (body text, tables, captions). A sample of 20-30 pages per language is a practical minimum for a reliable CER estimate (Levchenko 2025).
- **Document the evaluation tool.** CER/WER scores differ across evaluation tools due to normalization differences (whitespace handling, Unicode normalization, punctuation treatment). Neudecker et al. (2021) demonstrate that tool choice changes reported accuracy. Specify which tool you used, which normalization was applied, and whether the comparison was case-sensitive.
- **Acknowledge CER/WER limitations.** Character-level edit distance does not capture layout errors, semantic correctness, or structural fidelity. A model can scramble column order while achieving low CER (Beyene & Dancy 2026). Supplement with dictionary hit rates, manual inspection of representative pages, and downstream task performance.
- **Set go/no-go thresholds relative to downstream needs.** A mean CER below 5% is excellent; below 10% is acceptable for most computational text analysis. Calibrate against what your analysis pipeline can tolerate rather than pursuing absolute accuracy.

### 7. Reproducibility and Documentation

- **Record every pipeline parameter in machine-readable format.** Model name and exact version, quantization method, DPI, prompt text, generation parameters (temperature, max tokens, sampling strategy), software versions, and hardware specifications. Store as JSON alongside the output.
- **Produce per-document processing reports.** Each document should have a JSON report recording pipeline stages completed, timestamps, page counts (processed, failed), quality summary, and output file manifest.
- **Aggregate into a corpus-level batch summary.** A single CSV mapping all documents to their quality metrics, processing metadata, and tranche membership supports both quality monitoring and methods reporting.
- **Archive the complete pipeline code and prompts.** The OCR can only be reproduced if the exact code, prompts, and model weights are available. Pin model versions and software dependencies. If using a model from a hub (HuggingFace, etc.), record the commit hash.

## Quality Checks

- [ ] **Model benchmarked for task:** VLM selected based on document-OCR benchmarks (OCRBench or equivalent), not general VLM leaderboards (Liu et al. 2024; Fu et al. 2025)
- [ ] **Language support verified:** Target language confirmed in the model's explicit training set with per-language accuracy data (Bai et al. 2025)
- [ ] **Quantization tradeoff assessed:** If using 4-bit or 8-bit quantization, accuracy impact measured on a pilot sample against full-precision baseline (Li et al. 2025)
- [ ] **DPI justified:** OCR input DPI chosen based on document age and condition, with archival images stored separately at native resolution (FADGI 2016)
- [ ] **Native extraction preferred:** Embedded images extracted byte-for-byte from scanned PDFs rather than re-rasterized, when available
- [ ] **Preprocessing tested on sample:** Any image preprocessing validated on a diverse sample before corpus-wide application (Guan et al. 2025)
- [ ] **Prompts are language-specific:** OCR prompts explicitly name the script system, enumerate expected diacritics or character sets, and include negative instructions
- [ ] **Pipeline stages separated:** GPU-intensive OCR decoupled from CPU-only diagnostics and assembly, with structured JSON output at each stage
- [ ] **Diagnostics integrated:** Automated quality diagnostics classify every page by action category with language-aware character detection
- [ ] **Resource estimate calibrated:** GPU-hours estimated from a measured calibration run, not assumed from model documentation
- [ ] **Test tranche gated:** Accuracy evaluation completed on a test tranche before committing to bulk GPU-hours
- [ ] **Ground truth sampled:** Human-transcribed ground truth created for a stratified sample of pages, with CER/WER computed and reported (Levchenko 2025)
- [ ] **Evaluation tool documented:** CER/WER tool identified and normalization choices recorded, given known tool discrepancies (Neudecker et al. 2021)
- [ ] **Pipeline fully documented:** Model version, quantization, DPI, prompts, generation parameters, and software versions recorded in machine-readable format
- [ ] **Processing reports generated:** Per-document JSON reports and corpus-level batch summary CSV produced and archived
