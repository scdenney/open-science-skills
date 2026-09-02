# Replication Package

Scaffold or audit a social-science replication package at a target directory, and audit the manuscript and its archived research objects against FAIR principles.

Scaffold mode generates folder structure, `README.md`, `master.R`, figure/table crosswalk, codebook template, `LICENSE` placeholder, `.gitignore`, and a pre-release checklist. Audit mode grades an existing package against that checklist and the paper-consistency check, then runs the FAIR block — Findable, Accessible, Interoperable, Reusable — over data, code, materials, prompts, preregistrations, repository links, persistent identifiers, metadata, licenses, access restrictions, and availability statements, prompting the author for anything missing.

Platform-neutral (Harvard Dataverse, OSF, Zenodo, GitHub releases, institutional archives) — this skill builds and audits the local package; uploading is left to the destination repository's tools.

Methodology adapted from Yusaku Horiuchi's [replication-package-guide](https://github.com/yhoriuchi/replication-package-guide), with FAIR-principle integration.

Pass a target directory as an argument, plus a manuscript path or pasted availability statements when auditing. The skill defaults to `./replication` if no path is given.

$ARGUMENTS
