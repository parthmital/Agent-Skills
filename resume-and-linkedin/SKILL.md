---
name: resume-and-linkedin
description: Writes, updates, or tailors a single-page LaTeX resume from ground-truth documentation with ATS keyword coverage, and turns a project README or write-up into a LinkedIn project description of at most 500 characters, both with no invented claims. Use when the user asks to write, update, rewrite, tighten, or tailor a resume or CV, rewrite resume bullets, fit a resume on one page, tailor it to a job description, set up a resume workspace, or write a LinkedIn project description, summary, or post about a project. Not for cover letters.
---

# Resume and LinkedIn

## Overview

Career writing where every claim traces to a source the user owns. Two outputs share one discipline: a single-page LaTeX resume built from ground-truth documentation, and a LinkedIn project description of at most 500 characters built from a project write-up. Both compress wording, never drop listed items, and never invent a number.

## When to Use

- Output **Resume**: writing, tailoring, or tightening a resume or its bullets.
- Output **LinkedIn**: converting a README or project write-up into a LinkedIn project description.
- Not for cover letters, or for READMEs (`project-docs`).

## Shared Rules

1. Every metric, title, date, tool, and claim traces to the source. Metrics and units exactly as written there. Never invent, estimate, round, or infer one. A bullet that needs an undocumented metric is written without it, and the reply says so.
2. Before writing, silently list everything that must appear: every role and project in scope, each one's key achievements and documented metrics, and the technologies. The final text contains every listed item or the reply names what the user must decide to cut.
3. Bullet shape: what was built and the problem, how (engineering, analysis, architecture), documented result, then impact. Lead with a strong, specific verb (`Architected`, `Engineered`, `Implemented`, `Migrated`, `Trained`, `Benchmarked`, `Deployed`, `Quantised`, `Orchestrated`, `Consolidated`, `Automated`), no opener more than twice per document.
4. No buzzwords (innovative, cutting-edge, seamless, revolutionary, passionate, scalable without a number), no bare technology lists, no em dashes or semicolons.
5. A job description only guides which documented content and keywords to choose and order. Never add a skill because it asks for it. List unsupported important keywords for the user instead.
6. If sources contradict each other, use the most specific or recent one and mention the contradiction.

## Process

### Resume

Workspace (create it if missing, copy [assets/resume-template.tex](assets/resume-template.tex) to `Resume.tex`, and ask the user to add documentation first):

```text
<workspace>/
|-- Resume.tex          the only file this output edits (whatever its name; ask if several)
|-- Education/          transcripts, grades, coursework, certifications
|-- Experience/         one file or folder per role
`-- Projects/
    |-- Present/        flagship projects, the only Projects section source
    |-- Past/           older projects, Technical Skills keywords only
    `-- Future/         in-progress projects, Technical Skills keywords only
```

1. Read every relevant file in `Education/`, `Experience/`, and `Projects/` before editing. With a job description, extract its required and preferred skills, then rank documented content by match.
2. Write per Shared Rules and these resume rules:
   - Edit only content inside existing macros (`\resumeSubheading`, `\resumeItem`, `\resumeProject`, `\skillCategory`, `\Candidate...`). Never change the preamble, packages, geometry, margins, fonts, spacing, section order, macro definitions, or any ground-truth file.
   - About 200 characters (two printed lines) per bullet as a guide. Bullet counts follow depth and impact, most relevant first.
   - Each bullet bolds its single most impactful element with `\textbf{...}` (metric, outcome, or scale), never a bare technology name. `\&` instead of "and".
   - No redundancy: Experience and Projects show depth, Coursework uses formal curriculum titles from `Education/`, and Technical Skills holds only keywords not shown elsewhere, job description matches first.
   - ATS-parseable: standard headings (`Education \& Certifications`, `Experience`, `Projects \& Research`, `Technical Skills`), `Month Year -- Month Year` dates, single column. Escape `\%`, `\&`, `\_`, `\$`, `\#`, official tool spellings.
3. Fit to one page, recompiling after each step, compressing and never dropping an item: cut filler and articles, shorten phrasing (`using` to `with`), merge related bullets of one role, trim bullets that spill a few words onto a new line, move secondary tools to Technical Skills and merge its categories. If it still does not fit, stop and ask what to cut, listing candidates.
4. Compile: with `pdflatex` available, run `pdflatex -interaction=nonstopmode -output-directory .agent-local/tmp/resume-build Resume.tex` in the workspace, read `Output written on ... (N page` from the log, then delete the build folder.

### LinkedIn

1. Get the source, asking if none is given. For a repository, read `README.md` and any linked docs holding metrics.
2. Write one plain sentence on what was built and why, then 3 to 6 bullets starting with `•`, ordered what, how, then measurable impact. A bullet may carry several related items.
3. Count characters including spaces. Over 500: compress, never drop a listed item. In order: cut filler and adjectives, shorten phrasing, merge related bullets, fold technologies into the clause they serve, use `&`, `~`, `→`, `+`, and common abbreviations. Recount after each pass.
4. Reply with only the description in one code block. Add one short line after it only when something needs attention: a contradiction, an unsupported claim left out, or an item that could not fit.

## Examples

Resume, bad: `\resumeItem{Worked on a machine learning model using Python and TensorFlow and improved it.}`

Resume, good, when ground truth documents the numbers: `\resumeItem{Engineered a TensorFlow defect classifier for 40k PCB images \& deployed it on an edge GPU, \textbf{cutting inspection time by 62\%}}`

LinkedIn, bad: `Built an innovative, cutting-edge AI platform using Python, React, Docker, AWS, and more.`

LinkedIn, good, from a README stating these facts:

```text
Built a retrieval-augmented assistant that answers support questions over 12k past tickets.
• Engineered hybrid BM25 & embedding retrieval with re-ranking behind a FastAPI service
• Cut median answer time from 9 min to 40 s in a 3-week pilot with 25 agents
```

## Common Rationalisations

| Rationalisation                                                   | Reality                                                      |
| ----------------------------------------------------------------- | ------------------------------------------------------------ |
| "The job description wants Kubernetes, and they probably used it" | Undocumented claims fail interviews. List it as unsupported. |
| "An estimated or rounded metric reads better"                     | Changed numbers are invented numbers.                        |
| "A small preamble tweak will fit one page"                        | Layout is fixed. Tighten wording instead.                    |
| "Space is tight, drop the weakest project"                        | Compress. Only the user decides what to cut.                 |
| "Listing every tool shows breadth"                                | Tech lists bury the impact.                                  |

## Red Flags

- A metric or claim not found in the source.
- Any resume diff outside macro content.
- A verb opening more than two bullets.
- A listed role, project, metric, or keyword missing from the final text.
- LinkedIn text outside the code block beyond one attention line.

## Verification

- [ ] Every claim and metric traces to the source, and every listed item appears or the user agreed to cut it.
- [ ] Resume: only the target `.tex` changed, content only. One page verified by compiling, or reported unverified with the sections that grew. Projects only from `Projects/Present/`. Verb limit, one `\textbf{...}` per bullet, escaping, headings, and single column intact.
- [ ] LinkedIn: at most 500 characters, counted. One opening sentence plus 3 to 6 `•` bullets.
- [ ] Final reply lists claims left without metrics, unsupported job description keywords, and anything outside editable content (reported, not fixed).
