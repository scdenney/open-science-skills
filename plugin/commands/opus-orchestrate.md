# Orchestrate (Opus lead)

Run the `orchestrate` skill with `--lead opus`, forcing **Opus-lead mode** rather than detecting the lead from the session's model. Claude Opus 5 leads at medium reasoning effort by default (high only if the session will be dominated by direct hard reasoning). You are the same model as the `deep-reasoner`, so reason compact hard problems in place and delegate only to fan out, keep context lean, or get a blind independent line; structured phases run as parallel `Agent` fan-outs, upgrading to a dynamic `Workflow` only where the session actually has that tool.

Still read the model line in your own context first. If the session is not actually running Opus 5, say so plainly, ask for `/model` (and `/effort` per the skill's calibration table), and do not label the output as Opus's.

$ARGUMENTS
