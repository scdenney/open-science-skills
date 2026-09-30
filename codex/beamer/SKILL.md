---
name: beamer
description: House rules and craft for LaTeX Beamer slide decks (lectures, seminars, talks), built from the author's own Overleaf edits and published slide-design guidance. Covers storyboarding before LaTeX, frame titles, slide prose, word and frame budgets, layout that avoids overfull boxes, XeLaTeX fonts and Korean (xeCJK), color, figures and screenshots, Overleaf source hygiene, speaker notes, and the build and QA loop with a contact sheet. Use whenever a .tex deck, a beamer theme (.sty), a storyboard, slides, frames, overfull boxes in a deck, or an Overleaf slide repo is being written, edited, reviewed, or built, even without the word Beamer. A course skill (for example ba3-skills) supplies that course's facts, schedule and frame skeleton, and this skill supplies the craft alongside it. Not for HTML or PowerPoint decks, posters, or papers.
license: CC-BY-NC-4.0
metadata:
  author: Steven Denney
  version: 1.0.0
---

# Beamer decks

A deck is read from the back of a room, then posted as a PDF. Every rule below serves one of those two readings. Many rules come from edits the author made to drafts on Overleaf. Where an older skill or template disagrees with those edits, the edits win.

## Division of labor

- A **course or project skill** owns facts and structure: dates, deadlines, objectives, checklists, the frame skeleton, the corpus, release rules. Read it first when one applies, and never type a fact it generates.
- **This skill** owns craft: wording, density, layout, type, figures, source hygiene, and QA.
- Prose beyond slide text (handouts, READMEs, site pages) goes to the house editing skill (`$sci-edit` where installed).

## Workflow

1. **Pull first.** The author edits on Overleaf between sessions. `git pull --rebase` before touching a deck, and treat every wording change they made as a decision. Keep their text verbatim unless asked to change it. Never re-apply a rule from this file to wording they wrote.
2. **Storyboard before LaTeX.** One file with the teaching claim (two to four sentences), a minute budget that sums to the slot, one running example, and a frame table listing each frame's number, title, and evidence (the figure, output, excerpt, or table that makes the frame's point). Read the titles top to bottom. If the story does not hold, fix the storyboard.
3. **Get the numbers from the data.** Every count, score, or example in a deck comes from the dataset the audience will use, computed by a script kept next to the deck. Numbers from older decks built on other corpora are recomputed, never carried over.
4. **Write** one frame per storyboard row.
5. **Build twice** with XeLaTeX (references, page totals, and the progress bar settle on the second pass). Build every variant the repo produces (main, handout, notes). A bug once shipped because only the main build was checked.
6. **Check**, then look. Run the repo's checker if it has one, then render a contact sheet and read it, naming what you saw (overflow, contrast, Korean glyphs, cropped images, crowded frames). Render single pages at 110–150 dpi for a close look.
7. **Report** the page count, overfull count, checker result, and what the contact sheet showed.

## Titles

- Short labels and questions are fine and often better: "Review", "Roadmap for today", "A token and a type", "What is preprocessing?", "Demo 1 checklist". The author shortened many sentence titles to labels like these.
- A sentence title is useful when the claim is the point of the frame ("Three features of Korean make it hard to use the same splitting tools"). Keep it under about 12 words.
- No "(cont'd)". A continued idea gets its own title.
- Vary the title shapes. A run of aphorisms with the same cadence ("X secretly does Y") reads as generated.

## Slide prose

- Plain words a first-year student understands. Shorter definitions beat complete ones ("clean units for analysis").
- Use fewer words, 20–40 per frame and 80 at most (Beamer user guide). Cut the frame back to its title's point and move the rest to what you say aloud, the notes, or the course site.
- Bullets are phrases or short sentences, at most two levels, 45–75 characters per line.
- Bold a key phrase inline rather than adding a block. No bold pseudo-headings inside running text ("**The task.** …").
- Punctuation:
  - no em dashes
  - no semicolons
  - a colon only before a list (clock times are fine)
  - straight TeX quotes ``like this''
- Sentences:
  - no "not X but Y"
  - no trailing "-ing" clauses ("highlighting…", "reflecting…")
  - no "reveal", "move", or "sharpen" as analytic verbs
  - is/are/has rather than "serves as" or "represents"
  - three items only when there are three things
- Digits for numbers. One term per concept across the deck. American spelling unless the course uses British.
- Direct address and first person are fine where the author uses them ("Ask me for a piece of paper", "the script I wrote for you. You can tinker!"). Some courses forbid "I", and the course skill says so.
- Nothing internal on a student slide: no planning-file names, no "from our module plan", no codewords, no survey IDs.
- A short aside in the audience's language is fine as emphasis ("Let op!").

## Density and pacing

- About one frame per minute of talk at most (Beamer user guide). For 105 minutes with a survey and a live demonstration, 20–30 frames. A live demonstration needs one frame (the exported workflow), not a screenshot per click.
- One idea per frame. When a frame is crowded, split it. Never shrink the font to make it fit. `\small` is the floor, and only for code, trees, or tables.
- When content overflows, fix the layout (wider or equal columns, a smaller image, a table with `p{}` columns). Do not reword the author's text to fit.
- Cut decoration. Every block, rule, and color has a meaning or goes (Mayer's coherence principle).
- On-screen text does not repeat the narration word for word (Mayer's redundancy principle).

## Structure

- **Title page:** only the title, name, institution, and occasion. The session objective goes on its own frame after it.
- **Open with the real thing:** a real output, excerpt, or result, before administration where the format allows.
- **One running example** (a sentence, a dataset, a case) threads through the whole deck.
- **Roadmap times must add up.**
  - Each row's start time equals the previous start plus its minutes.
  - The last row ends at the slot's end.
  - Use round or five-minute blocks.
  - Check the arithmetic before every build. A row reading "10:" once shipped to Overleaf.
- **Cue, break, and transition frames** are unnumbered standout frames with one short line ("Screens away · No computers or phones", "Laptops open", "Break").
- **Before a hands-on block:** recap on one frame.
- **The close** ends on the next concrete task (the checklist and next week), not on a list of what was not covered. Limitation and "not covered" frames are optional. The author cut them when they weakened the close.
- **The appendix:**
  - `\appendix` and an "Appendix" cue frame
  - unnumbered `[noframenumbering]` frames titled "Appendix · …"
  - a glossary covering every term the deck uses: two fixed-width, left-aligned columns, no rules
- **Backup frames:** detail that does not fit goes to the appendix, reached by `\hyperlink`, not squeezed in.

## Layout

- `\raggedright` in columns and blocks. Justified text in narrow columns leaves gaps.
- Tables:
  - booktabs, no vertical rules
  - `p{}` columns with `\raggedright\arraybackslash` and `\tabularnewline`. A wide `l` column overflows at 16:9.
  - reveal rows with overlays only when the reveal is the point
- Image frames: prompt text in a left column of about `.32\textwidth`, the image in the right column at `height=.92\textheight, keepaspectratio`. The title can be empty when the image is the whole point.
- Side-by-side comparison: two equal columns, each with a short label on top.
- No `allowframebreaks`, no navigation symbols, no section title frames unless the author asks for them. A progress bar under the frame title is enough.
- Overlays only when the step-by-step build is the idea. The handout build collapses overlays, so the final state of every frame must read correctly on its own.

## Type and color

- **XeLaTeX** (or LuaLaTeX when the theme needs it), 16:9, 11pt.
- **Fonts** are loaded by filename through fontspec, so the build does not depend on the system font cache:
  - use static font files (Regular, SemiBold, Bold). XeTeX cannot embolden a variable font.
  - a deck never sets its own fonts over the theme's. A deck-level `\setsansfont` silently replaces the theme and is the usual cause of Latin Modern or missing Hangul.
  - never switch to another font to get a build through. Install the missing font instead.
- **Korean:**
  - load xeCJK after the Latin fonts with Noto Sans CJK KR (fall back to NanumGothic) and `CJKspace=true`
  - type Hangul directly, with no wrapper macro
  - declare the middle dot (U+00B7) and box-drawing characters (U+2500–257F) as `Default` class so they stay in the Latin font
  - a "Missing character" warning in the log means Korean text reached a Latin font
  - xeCJK may break a line between two Hangul syllables, splitting a word such as 국민 across lines. Wrap a word that must stay whole in `\mbox{}`.
- **Color:**
  - 2–3 colors in regular use, colorblind-safe (Okabe–Ito or Paul Tol)
  - never red against green, or color as the only cue
  - a muted palette: saturated full-width title bars and bright accents made decks feel busy and were replaced
  - use the deep brand color for cue frames only
  - blocks use dark text on a pale fill, never white on a mid-tone fill
  - check contrast. Ink on paper should be above 7:1, and anything under 4.5:1 fails.

## Figures and screenshots

- Crop a screenshot to the decision being shown, use the current app version, keep each file under 1 MB, and give it alt text (printed under the image or in the notes).
- Replace blurry or cluttered browser captures with clean exports.
- Generated figures come from a script in the repo with a fixed seed, plus a small JSON of method metadata next to the output. Render at the size shown on the slide, so no text inside the figure falls below about 8 pt after scaling.
- Use the deck's fonts in figures (matplotlib `FontProperties` from the same font file, or ggplot `family=`).
- Don't invent glyphs or icons. Render candidates and show them before adopting one across a deck.
- Credit third-party images and documentation screenshots in the repo README or the notes.
- Live-demo placeholders: when a screenshot must come from the author's own machine, leave a labeled slot (`\imgslot{name}{what to capture}`) rather than an approximation.

## Overleaf source hygiene

- One paragraph or bullet per source line, so Overleaf soft-wraps and diffs stay readable.
- The theme `.sty` holds formatting only, with no student-visible wording and no whole frames. Wording lives in the deck file, where the author can edit it on Overleaf. Generated fact macros (dates, deadlines) are the exception and come from a script.
- Do not edit the theme to fix one deck's problem. Fix the frame.
- Speaker notes do not go in `\note{}` by default. Frame-by-frame note blocks make the source hard to navigate. Keep notes in a companion `<deck>-notes.md`, unless the repo already builds a notes PDF the author uses. Notes over about 120 words overflow a notes page silently.
- Overleaf strips the executable bit. Call repo tools as `bash tools/build.sh`, not `./tools/build.sh`.
- After a bulk reformat (line wrapping, macro inlining), prove the output did not change: `pdftotext` both PDFs and diff them.
- Commit messages follow the repo's git conventions. Overleaf pushes go to `main` with `git pull --rebase` first, never force.

## QA checklist

- [ ] Two XeLaTeX passes. Zero errors, zero `Overfull` boxes (compare the count against the pre-edit baseline), zero `Missing character`.
- [ ] `pdffonts` shows every font embedded, and no Latin Modern where the theme sets another font.
- [ ] Word count per frame: 40 or under, except table, code and figure frames. None over 80.
- [ ] Frame count against the minute budget. Roadmap arithmetic checked.
- [ ] Every number traces to the script and dataset. Every date comes from generated meta if the course has it.
- [ ] Contact sheet read, with what was seen named. Handout and notes variants built and glanced at.
- [ ] Nothing private or unreleased on a frame.

## Snippets

Preamble, with fonts by filename and Korean:

```latex
\documentclass[11pt,aspectratio=169]{beamer}
\usetheme{metropolis}
\metroset{progressbar=frametitle, numbering=fraction, sectionpage=none}
\usepackage{fontspec}
\setsansfont{FiraSans}[Extension=.otf, UprightFont=*-Regular, BoldFont=*-SemiBold,
  ItalicFont=*-Italic, BoldItalicFont=*-SemiBoldItalic]
\setmonofont{FiraMono}[Extension=.otf, UprightFont=*-Regular, BoldFont=*-Bold, Scale=MatchLowercase]
\usepackage{xeCJK}
\IfFontExistsTF{Noto Sans CJK KR}{\setCJKsansfont{Noto Sans CJK KR}}{\setCJKsansfont{NanumGothic}}
\xeCJKsetup{CJKspace=true}
\xeCJKDeclareCharClass{Default}{"00B7}
\usepackage{booktabs}
```

Table that fits at 16:9:

```latex
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{.28\textwidth}
                   >{\raggedright\arraybackslash}p{.62\textwidth}@{}}
\toprule
Term & What it means \tabularnewline
\midrule
TF-IDF & A count weighted by how rare the word is across documents \tabularnewline
\bottomrule
\end{tabular}
```

Image on the right, prompt on the left:

```latex
\begin{frame}{}
  \begin{columns}[T,onlytextwidth]
    \begin{column}{.32\textwidth}\raggedright
      Which words rise when we weight by rarity?
    \end{column}
    \begin{column}{.64\textwidth}
      \includegraphics[height=.92\textheight,width=\linewidth,keepaspectratio]{shots/cloud-tfidf}
    \end{column}
  \end{columns}
\end{frame}
```

Roadmap with times that add up (09:15 + 10 = 09:25, and so on, ending at 11:00):

```latex
\begin{tabular}{@{}l>{\raggedright\arraybackslash}p{.62\textwidth}r@{}}
09:15 & Opening survey and review & 10 \tabularnewline
09:25 & Lecture & 45 \tabularnewline
10:10 & Orange demonstration & 35 \tabularnewline
10:45 & Checklist and next week & 15 \tabularnewline
\end{tabular}
```

Unnumbered appendix frame:

```latex
\appendix
\begin{frame}[standout]Appendix\end{frame}
\begin{frame}[noframenumbering]{Appendix · Glossary}
  ...
\end{frame}
```

## Troubleshooting

- **The deck looks like Latin Modern.** A deck-level font command overrode the theme. Remove it.
- **Blank or boxed Hangul.** The CJK font is not set for the family in use (`\setCJKsansfont` for metropolis), or a deck redefined the sans font.
- **Overfull hbox on a table.** Switch the wide `l` column to `p{}` with `\raggedright\arraybackslash`.
- **Overfull vbox.** The frame has too much content. Split it, or move detail to the appendix.
- **The title page overfills at 16:9.** Build it inside a `\textheight` minipage.
- **The notes PDF renders near-white text.** pgfpages broke the color stack. Interleave note pages instead of using `show notes on second screen`.
- **Overleaf rejects the push.** `git pull --rebase origin main`, then push again.

## Sources

The rules above come from:
- the Beamer user guide's chapter on creating presentations (frames per minute, words per frame, fonts, color, overlays)
- Alley's assertion–evidence design
- Goldsmith-Pinkham's Beamer tips (colorblind palettes, tables, backup slides)
- Keith Head on navigation symbols and continuation titles
- Brown University's Sheridan Center on lecture slides (minimum sizes, contrast, describing visuals)
- Mayer's multimedia-learning principles (coherence, signaling, redundancy)
- the metropolis manual
- the author's own edits
