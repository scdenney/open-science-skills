# Verify

Run the `replication-package` skill's **Step 6b only**: the deterministic checks in `scripts/verify_package.py`. Skip scaffold mode, skip the package grade, skip the FAIR block, and skip the audit report. This is the fast "does my analysis still work" pass, not a submission audit.

Resolve the target directory the same way `replication-package` does, defaulting to the current directory. Then:

1. Run the static tier, `python3 "$SKILL/scripts/verify_package.py" --root <dir>`, where `$SKILL` is the installed `replication-package` skill directory. It reads files only. Report its table as-is rather than paraphrasing it.
2. If a master script was found, ask whether to execute it in a temporary copy. Use the `AskUserQuestion` tool, not a line of prose, so the choice is a real prompt. One question headed `Clean-room run`, naming the script, offering `Run it now` and `Skip, record NOT CHECKED`. Re-run with `--run` only on an explicit choice to run; otherwise leave the clean-room run as NOT CHECKED and say so.
3. Explain any failure in one sentence each and name the skill that owns the fix: citations to `citation-check`, figures and tables to `figure-table-audit`, packaging and FAIR to `replication-package`. Do not fix anything here.

A `crosswalk` failure means the package claims outputs its own code did not produce. Say that plainly; it is the finding this command exists to surface.

$ARGUMENTS
