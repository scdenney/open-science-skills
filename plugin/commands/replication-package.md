# Replication Package Scaffold

Scaffold or audit a social-science replication package at a target directory. Generates folder structure, `README.md`, `master.R`, figure/table crosswalk, codebook template, `LICENSE` placeholder, `.gitignore`, and a pre-release checklist. Platform-neutral (Harvard Dataverse, OSF, Zenodo, GitHub releases, institutional archives) — this skill builds the local package; uploading is left to the destination repository's tools.

Methodology adapted from Yusaku Horiuchi's [replication-package-guide](https://github.com/yhoriuchi/replication-package-guide), with FAIR-principle integration. Pair with `/oss:fair-check` afterwards to audit the finished package against FAIR before submission.

Pass a target directory as an argument. The skill defaults to `./replication` if no path is given.

$ARGUMENTS
