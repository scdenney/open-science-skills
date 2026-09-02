# VLM-OCR

Run the `vlm-ocr` skill on the task below. It has three phases: `evaluate` (compare candidate OCR systems against stratified human ground truth and pick one on measured CER/WER), `run` (build and execute the production VLM-OCR pipeline — model selection, image handling, prompts, architecture, batching, accuracy evaluation, reproducibility), and `clean` (LLM and rule-based correction, quality diagnostics, multilingual handling, span-level provenance).

Infer the phase from what is supplied — a corpus with no model chosen goes to `evaluate`, a chosen model to `run`, raw OCR output to `clean` — or use the phase named as the first argument. Born-digital documents with a text layer belong to `doc-to-markdown`, not here.

$ARGUMENTS
