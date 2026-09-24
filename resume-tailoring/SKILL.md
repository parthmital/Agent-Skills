---
name: resume-tailoring
description: Write, rewrite, update, or tailor a single-page LaTeX resume from ground-truth documentation, with ATS keyword coverage, strategic bolding, action verb limits, and no invented metrics. Use automatically when the user asks to write, update, rewrite, refresh, tighten, or tailor a resume or CV, rewrite resume bullets, fit a resume on one page, tailor a resume to a job description, or set up a resume workspace. Do not use for cover letters or LinkedIn posts.
---

# Resume Tailoring

Produce or update a single-page LaTeX resume whose every claim traces to the user's ground-truth documentation.

## Workspace

A resume workspace is a folder with this layout:

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

1. Look for this layout in the current directory first. If it is not there, ask the user where their workspace is.
2. If the user has no workspace, scaffold one: create the folders above and copy [assets/Resume.tex](assets/Resume.tex) to `<workspace>/Resume.tex`. Then ask the user to add their documentation before writing any content.
3. If the workspace uses a different `.tex` file name, treat that file as the target. If there are several `.tex` files, ask which one.
4. Read every relevant file in `Education/`, `Experience/`, and `Projects/` before editing. The resume is only as good as this reading.

If the user supplies a job description, use it only to choose and order content and keywords that already exist in the ground truth. Never add a skill, tool, or claim because the job description asks for it. List important job description keywords that the ground truth does not support, so the user can decide whether to document them.

## Hard Constraints

- **Single page.** The compiled resume must fit on one page.
- **Edit only the target `.tex` file.** Do not edit ground-truth files, the template's preamble, or anything else in the workspace.
- **Content only.** Do not change the preamble, packages, geometry, margins, fonts, spacing macros, section order, or macro definitions. Edit text inside the existing macros (`\resumeSubheading`, `\resumeItem`, `\resumeProject`, `\skillCategory`, and the `\Candidate...` placeholders).
- **Never invent.** Every metric, title, date, tool, and claim must trace to a ground-truth file. If a bullet needs a metric that is not documented, write it without one and tell the user.
- **Projects tiers.** Only `Projects/Present/` appears in the Projects section. `Projects/Past/` and `Projects/Future/` feed the Technical Skills section only.

## Writing Rules

1. **Bullet length.** About 200 characters (roughly two printed lines) is a guide, not a cap. Bullet counts per role follow depth and impact, not a fixed number. Split a large achievement into more bullets rather than over-compressing it.
2. **Bullet structure.** In order: what the product or project was and the problem it solved; the specific engineering, analysis, or architecture work; documented metrics; the operational, business, or developer impact.
3. **Action verbs.** Start every bullet with a strong verb. No verb may appear more than 2 times as a bullet opener across the whole resume. Watch generic verbs such as `Built` and `Automated`. Alternatives: `Architected`, `Engineered`, `Implemented`, `Migrated`, `Designed`, `Trained`, `Benchmarked`, `Deployed`, `Quantized`, `Orchestrated`, `Consolidated`, `Streamlined`, `Authored`.
4. **Strategic bolding.** Every bullet has at least one `\textbf{...}`. Bold the single most impactful element: a metric, outcome, measurable improvement, scale, or achievement (for example `\textbf{reducing model latency by 80\%}`). Do not bold bare technology names.
5. **Ampersands.** Use `\&` instead of "and" in every bullet to save space.
6. **Separation of concerns and no redundancy.**
   - Experience and Projects: depth and proof, using the primary technologies from `Experience/` and `Projects/Present/`.
   - Coursework: formal curriculum titles from `Education/` (for example `Data Structures \& Algorithms`, `Operating Systems`, `Database Systems`), not casual abbreviations.
   - Technical Skills: breadth only. Unique, relevant keywords from `Experience/` and all three `Projects/` tiers that are not already shown in Experience, Projects, or Coursework.
7. **Professional competencies.** Where the ground truth supports it, show ownership and technical decision-making, cross-functional communication, and teamwork (reviews, shared delivery, cross-team alignment).
8. **Two audiences.** Engineers need architecture, tooling, and rigour. Recruiters need the problem, quantified outcomes, scale, and ownership. Each bullet should serve both.
9. **Sequencing.** Order bullets within each entry deliberately, most relevant and impactful first, so each leads naturally into the next.
10. **Parseability.** Keep the standard headings (`Education \& Certifications`, `Experience`, `Projects \& Research`, `Technical Skills`), the `Role/Degree`, `Organisation`, `Dates`, `Location` hierarchy, `Month Year -- Month Year` dates, and single-column flow.
11. **Typography.** No em dashes. Use `--` for ranges. Escape `\%`, `\&`, `\_`, `\$`, `\#`. Zero spelling, grammar, or LaTeX syntax errors; check tool and library names against their official spelling.

## Verification

Before finishing, check each item and report the result:

- [ ] Only the target `.tex` file changed, and only its content, not its layout or macros.
- [ ] Single page. If `pdflatex` is available, compile a copy in a temporary directory outside the workspace (for example `pdflatex -interaction=nonstopmode -output-directory <tmp> Resume.tex`), read the page count from the log (`Output written on ... (N page`), then delete the temporary output. Leave no build artefacts in the workspace. If `pdflatex` is not available, say the page count was not verified and flag any section that looks longer than before.
- [ ] Every metric, date, title, and tool traces to a ground-truth file.
- [ ] The Projects section contains only `Projects/Present/` entries.
- [ ] Bullet-opening verbs counted: none used more than 2 times.
- [ ] Every bullet has a strategic `\textbf{...}` on an impact element.
- [ ] `\&` used instead of "and" in bullets.
- [ ] No technology repeated in Technical Skills that Experience, Projects, or Coursework already shows.
- [ ] Coursework uses formal curriculum titles from `Education/`.
- [ ] LaTeX escaping is valid and there are no spelling or grammar errors.
- [ ] Standard headings, metadata hierarchy, and single-column flow are intact.

In the final reply, list any claims written without a metric because none was documented, any unsupported job description keywords, and whether the single-page check was verified by compiling.
