# Kind profiles

One file per deliverable kind. `deliverable-open` reads the profile to run its interview and write the manifest; `lint_prepare.py` appends the profile's lint questions to every section input; the ship step follows the profile. Vendor-neutral: Claude and Codex read the same files. Sections: `## Interview` (questions beyond the common five), `## Manifest defaults`, `## Lint questions` (added to the section finders and the global pass), `## Ship`, `## Related skills`.
