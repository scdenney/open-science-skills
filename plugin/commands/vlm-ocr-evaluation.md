# VLM-OCR Evaluation

Compare multiple OCR systems against human ground truth to select a model before a bulk run. Assemble a candidate set (open-weight VLMs, one or two proprietary APIs, and a traditional Tesseract baseline), build a stratified ground-truth sample (language/script, era, content type), compute CER and WER with an explicitly declared normalization recipe, report mean and median per stratum rather than a single overall mean, run models sequentially to fit hardware, and interpret fit-to-script instead of assuming a single best model. This is the selection gate that precedes the vlm-ocr-pipeline skill.

$ARGUMENTS
