---
name: resume-tailoring
description: Write, rewrite, update, or tailor a single-page LaTeX resume from ground-truth documentation, with ATS keyword coverage, strategic bolding, action verb limits, and no invented metrics. Use when the user asks to write, update, rewrite, refresh, tighten, or tailor a resume or CV, rewrite resume bullets, fit a resume on one page, tailor a resume to a job description, or set up a resume workspace. Not for cover letters or LinkedIn posts.
---

# Resume Tailoring

Produce or update a single-page LaTeX resume in which every claim traces to the user's ground-truth documentation.

## Workspace

```text
<workspace>/
|-- Resume.tex          the resume source; the only file this skill edits
|-- Education/          transcripts, grades, official coursework lists, certifications
|-- Experience/         one Markdown file or subfolder per role
`-- Projects/
    |-- Present/        completed flagship projects; the only source for the Projects section
    |-- Past/           completed older projects; Technical Skills keywords only
    `-- Future/         in-progress projects; Technical Skills keywords only
```

1. Look for this layout in the current directory; if it is absent, ask where the workspace is.
2. If the user has none, create the folders, copy [assets/Resume.tex](assets/Resume.tex) to `<workspace>/Resume.tex`, and ask them to add their documentation before writing content.
3. If the `.tex` file has another name, it is the target. If there are several, ask which one.
4. Read every relevant file in `Education/`, `Experience/`, and `Projects/` before editing. The resume can only be as good as this reading.

A job description only guides which existing ground-truth content and keywords to choose and how to order them. Never add a skill, tool, or claim because the job description asks for it. List important job description keywords the ground truth does not support, so the user can decide whether to document them.

## Hard Constraints

- The compiled resume fits on one page.
- Edit only the target `.tex` file, and only its content: text inside the existing macros (`\resumeSubheading`, `\resumeItem`, `\resumeProject`, `\skillCategory`, and the `\Candidate...` placeholders). Never change the preamble, packages, geometry, margins, fonts, spacing macros, section order, or macro definitions, and never edit ground-truth files.
- Never invent. Every metric, title, date, tool, and claim traces to a ground-truth file. If a bullet needs an undocumented metric, write it without one and tell the user.
- Only `Projects/Present/` appears in the Projects section. `Projects/Past/` and `Projects/Future/` feed Technical Skills only.

## Writing Rules

1. Length: about 200 characters (two printed lines) per bullet is a guide, not a cap. Bullet counts follow depth and impact; split a large achievement rather than over-compressing it.
2. Structure, in order: what the product or project was and the problem it solved; the specific engineering, analysis, or architecture work; documented metrics; the operational, business, or developer impact.
3. Verbs: start every bullet with a strong verb, and use no verb as an opener more than 2 times across the resume. Watch generic ones like `Built` and `Automated`. Alternatives: `Architected`, `Engineered`, `Implemented`, `Migrated`, `Designed`, `Trained`, `Benchmarked`, `Deployed`, `Quantised`, `Orchestrated`, `Consolidated`, `Streamlined`, `Authored`.
4. Bolding: every bullet has at least one `\textbf{...}` on its single most impactful element (metric, outcome, improvement, scale, or achievement), such as `\textbf{reducing model latency by 80\%}`. Never bold bare technology names.
5. Use `\&` instead of "and" in bullets to save space.
6. No redundancy between sections:
   - Experience and Projects show depth and proof with the primary technologies from `Experience/` and `Projects/Present/`.
   - Coursework uses formal curriculum titles from `Education/`, such as `Data Structures \& Algorithms`, not casual abbreviations.
   - Technical Skills shows breadth only: unique, relevant keywords from `Experience/` and all three `Projects/` tiers that Experience, Projects, or Coursework do not already show.
7. Where the ground truth supports it, show ownership, technical decision-making, cross-functional communication, and teamwork.
8. Write each bullet for two audiences: engineers want architecture, tooling, and rigour; recruiters want the problem, quantified outcomes, scale, and ownership.
9. Order bullets within each entry most relevant and impactful first, so each leads into the next.
10. Keep it parseable: standard headings (`Education \& Certifications`, `Experience`, `Projects \& Research`, `Technical Skills`), the `Role/Degree`, `Organisation`, `Dates`, `Location` hierarchy, `Month Year -- Month Year` dates, and single-column flow.
11. Typography: no em dashes; `--` for ranges; escape `\%`, `\&`, `\_`, `\$`, `\#`. Zero spelling, grammar, or LaTeX errors, with tool and library names in their official spelling.

## Verification

Check and report each item:

- [ ] Only the target `.tex` file changed, in content only, apart from the Git-ignored `.agent-local/` work area.
- [ ] Single page. If `pdflatex` is available, compile inside the workspace (`pdflatex -interaction=nonstopmode -output-directory .agent-local/tmp/resume-build Resume.tex`), read the page count from the log line `Output written on ... (N page`, and delete `.agent-local/tmp/resume-build/` so no build artefacts remain. Otherwise say the page count is unverified and flag sections that look longer than before.
- [ ] Every metric, date, title, and tool traces to ground truth, and Projects contains only `Projects/Present/` entries.
- [ ] No bullet-opening verb used more than 2 times.
- [ ] Every bullet has a strategic `\textbf{...}` and uses `\&` instead of "and".
- [ ] Technical Skills repeats nothing shown in Experience, Projects, or Coursework, and Coursework uses formal titles.
- [ ] LaTeX escaping, spelling, and grammar are correct, and headings, hierarchy, and single-column flow are intact.

In the final reply, list claims written without a metric because none was documented, unsupported job description keywords, and whether the single-page check was verified by compiling.
