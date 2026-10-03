---
name: resume-tailoring
description: Writes, updates, or tailors a single-page LaTeX resume from ground-truth documentation, with ATS keyword coverage, strategic bolding, action verb limits, and no invented metrics. Use when the user asks to write, update, rewrite, refresh, tighten, or tailor a resume or CV, rewrite resume bullets, fit a resume on one page, tailor a resume to a job description, or set up a resume workspace. Not for cover letters or LinkedIn posts.
---

# Resume Tailoring

## Overview

A single-page LaTeX resume in which every claim traces to the user's ground-truth documentation.

## When to Use

- Writing, tailoring, or tightening a resume or its bullets.
- Not for cover letters or LinkedIn (`linkedin-project-description`).

## Workspace

```text
<workspace>/
|-- Resume.tex          the only file this skill edits
|-- Education/          transcripts, grades, coursework, certifications
|-- Experience/         one file or folder per role
`-- Projects/
    |-- Present/        flagship projects; the only Projects section source
    |-- Past/           older projects; Technical Skills keywords only
    `-- Future/         in-progress projects; Technical Skills keywords only
```

## Process

1. Find this layout in the current directory, else ask where it is. If none exists, create it, copy [assets/Resume.tex](assets/Resume.tex) to `<workspace>/Resume.tex`, and ask the user to add documentation first.
2. The target is the `.tex` file, whatever its name; if there are several, ask.
3. Read every relevant file in `Education/`, `Experience/`, and `Projects/` before editing.
4. A job description only guides which ground-truth content and keywords to choose and order. Never add a skill or claim because it asks for it; list unsupported important keywords for the user.
5. Write per the rules below, then run Verification.

## Hard Constraints

- Compiles to one page.
- Edit only content inside existing macros (`\resumeSubheading`, `\resumeItem`, `\resumeProject`, `\skillCategory`, `\Candidate...`). Never change the preamble, packages, geometry, margins, fonts, spacing, section order, or macro definitions, or any ground-truth file.
- Every metric, title, date, tool, and claim traces to ground truth. If a bullet needs an undocumented metric, write it without one and tell the user.
- Projects section uses only `Projects/Present/`.

## Writing Rules

1. About 200 characters (two printed lines) per bullet as a guide, not a cap. Bullet counts follow depth and impact; split large achievements rather than over-compress.
2. Bullet order of ideas: the product and problem; the engineering, analysis, or architecture work; documented metrics; operational, business, or developer impact.
3. Start every bullet with a strong verb, no opener used more than 2 times across the resume. Watch `Built` and `Automated`; alternatives include `Architected`, `Engineered`, `Implemented`, `Migrated`, `Designed`, `Trained`, `Benchmarked`, `Deployed`, `Quantised`, `Orchestrated`, `Consolidated`, `Streamlined`, `Authored`.
4. Each bullet bolds its single most impactful element (metric, outcome, scale) with `\textbf{...}`, such as `\textbf{reducing model latency by 80\%}`. Never bold bare technology names.
5. `\&` instead of "and" in bullets.
6. No redundancy: Experience and Projects show depth with primary technologies; Coursework uses formal curriculum titles from `Education/` (`Data Structures \& Algorithms`); Technical Skills shows only unique keywords from `Experience/` and all `Projects/` tiers not already shown elsewhere.
7. Where supported, show ownership, technical decisions, cross-functional communication, and teamwork.
8. Write for engineers (architecture, tooling, rigour) and recruiters (problem, quantified outcome, scale, ownership). Order bullets most relevant first.
9. ATS-parseable: standard headings (`Education \& Certifications`, `Experience`, `Projects \& Research`, `Technical Skills`), `Role/Degree`, `Organisation`, `Dates`, `Location` hierarchy, `Month Year -- Month Year` dates, single column.
10. No em dashes; `--` for ranges; escape `\%`, `\&`, `\_`, `\$`, `\#`; official spelling of tool names; zero spelling, grammar, or LaTeX errors.

## Common Rationalizations

| Rationalization                                                   | Reality                                                              |
| ----------------------------------------------------------------- | -------------------------------------------------------------------- |
| "The job description wants Kubernetes, and they probably used it" | Undocumented claims fail interviews. List it as unsupported instead. |
| "An estimated metric is better than none"                         | Invented numbers are fabrication.                                    |
| "A small preamble tweak will fit one page"                        | Layout is fixed; cut or tighten content instead.                     |

## Red Flags

- Any diff outside macro content.
- A metric not found in ground truth.
- A verb opening more than 2 bullets.

## Verification

- [ ] Only the target `.tex` changed, content only (Git-ignored `.agent-local/` aside).
- [ ] One page: if `pdflatex` exists, run `pdflatex -interaction=nonstopmode -output-directory .agent-local/tmp/resume-build Resume.tex` in the workspace, read `Output written on ... (N page` from the log, then delete `.agent-local/tmp/resume-build/`. Otherwise report the page count unverified and flag sections that grew.
- [ ] All claims trace to ground truth; Projects only from `Projects/Present/`.
- [ ] Verb limit, one `\textbf{...}` per bullet, `\&` used.
- [ ] Technical Skills repeats nothing; Coursework uses formal titles.
- [ ] Escaping, spelling, grammar, headings, hierarchy, single column intact.
- [ ] Final reply lists claims left without metrics, unsupported job description keywords, and whether one page was verified by compiling.
