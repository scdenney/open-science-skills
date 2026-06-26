# LLM Calibration via Token Logprobs

Read a single model's own uncertainty from token log-probabilities and check whether that confidence is calibrated. Collect logprobs (OpenAI/vLLM/Ollama) at temperature 0 with a fixed seed, aggregate multi-token labels into one per-item confidence, map confidence (and the margin to the runner-up) onto triage tiers, then assess calibration with a reliability diagram, Expected Calibration Error, and Brier score against human-adjudicated ground truth before letting the thresholds drive human review. Distinct from cross-model agreement: this is within-model confidence, the complement to model-council-voting.

$ARGUMENTS