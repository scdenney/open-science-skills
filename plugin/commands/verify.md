# Verify

Run the `replication-package` skill's **Step 6b only**: the deterministic checks in `scripts/verify_package.py`. Skip scaffold mode, skip the package grade, skip the FAIR block, and skip the audit report. This is the fast "does my analysis still work" pass, not a submission audit.

Resolve the target directory the same way `replication-package` does, defaulting to the current directory. Then:

1. Run the static tier, `python3 "$SKILL/scripts/verify_package.py" --root <dir>`, where `$SKILL` is the installed `replication-package` skill directory. It reads files only. Report its table as-is rather than paraphrasing it.
2. If a master script was found, ask in one line whether to execute it in a temporary copy, naming the script. On an explicit yes, re-run with `--run`. On anything else, leave the clean-room run as NOT CHECKED and say so.
3. Explain any failure in one sentence each and name the skill that owns the fix: citations to `citation-check`, figures and tables to `figure-table-audit`, packaging and FAIR to `replication-package`. Do not fix anything here.

A `crosswalk` failure means the package claims outputs its own code did not produce. Say that plainly; it is the finding this command exists to surface.

$ARGUMENTS
