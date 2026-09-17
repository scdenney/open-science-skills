# Kind: module

A course, a course module, or a lecture series with a public site or slides and a class calendar.

## Interview
- The class calendar (dates, release dates, deadlines) and where it lives as data (`_data/course.yml`, a syllabus file); the assessment weights.
- The students: level, prior knowledge, language of instruction; what "done" looks like for a student who completes it.
- What is instructor-only (answer keys, rubrics, workbench notes) and how it is kept out of the public build.
- Readings: where the list lives, whether each reading is verified, and what may not be redistributed.

## Manifest defaults
- `sections_from: explicit` (one section per session or lecture, in calendar order)
- `sources_of_truth`: the calendar data file, the course guide, the release checklist
- `checks`: `facts` (session count, dates, deadlines, weights sum), `leaks` (unreleased sessions absent from the public build, instructor material absent, forbidden patterns), `citations` (`reading_lists: true` over the session pages and guide), `prose_tells`, `credentials`
- `build`: the site build with strict front matter, artifacts `[_site/index.html]`

## Lint questions
- Section: does the session state its objective and the deliverable due; are the readings the ones the calendar names; is every term a first-year reader meets defined at first use; does the demo or exercise match the deliverable.
- Global: do the sessions build (each assumes only earlier sessions); do dates, deadlines, and weights agree with the calendar data everywhere they are printed; is anything released early or instructor-only leaking.

## Ship
Release per session: flip `released` in the calendar data, build, `check_deliverable.py ship`, then the deploy step the repo uses (Pages `workflow_dispatch`, Brightspace upload, Teams package).

## Related skills
`research-repo` for a corpus companion; `sci-edit` for handouts and guides; the `hdw-data`-style house rules where a module has them.

## Ship policy
- `ship: {require_lint: false}` is the default for this kind: session pages ship weekly and a full lint each time is ceremony. The agent asks once per release whether to run `deliverable-lint` first; the receipt records the waiver either way.
