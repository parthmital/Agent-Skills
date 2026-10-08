---
name: latex-research-papers
description: Writes and finalises compile-ready LaTeX research papers with a local Tectonic, iterating until there is no overflow, figures and tables sit beside their first mention, references are current, verified, and in order of appearance, and citations, cross-references, URLs, and DOIs are clickable. Use when the user asks to write, edit, fix, compile, or polish a research paper, manuscript, preprint, thesis chapter, or other academic LaTeX, or its bibliography, figures, tables, or overflow. Not for resumes (`resume-tailoring`).
---

# LaTeX Research Papers

## Overview

Done means [scripts/paper_check.py](scripts/paper_check.py) prints `RESULT: CLEAN` with its PDF checks run, and every rendered page has been looked at.

## When to Use

- Any academic LaTeX document. Not resumes (`resume-tailoring`). Use `internet-research` for references and `repo-local-workspace` for installs and output.

## Process

1. Read the project's paper README, paper skill, and build command (such as `npm run paper`) and follow them. Numbers come only from the project's result files.
2. Tectonic: `$TECTONIC`, `PATH`, or `tectonic(.exe)` in or near the paper folder. If missing, ask, then install it per [references/fixes.md](references/fixes.md#install-tectonic).
3. Write per the Rules. Never edit the template's `.cls`, `.sty`, or `.bst`, its geometry or fonts, or source plots; patch template quirks in the preamble.
4. Run `python <skill>/scripts/paper_check.py main.tex --render .agent-local/output/paper-pages`; PDF checks need `pypdf` and `pypdfium2` in the repo `.venv`. Fix every blocking item and fixable warning with [references/fixes.md](references/fixes.md), view every page, and repeat. `--allow REGEX` only for a template-internal line confirmed harmless in the PDF.
5. Before finishing, rerun with `--check-links`, then build the deliverable with the project's command, else `tectonic --keep-logs --reruns 3 main.tex` in the paper folder. Git-ignore build artefacts.

## Rules

- No overflow anywhere: text, figures, tables, equations, captions, bibliography. Never mask it with `\sloppy`, `\hfuzz`, `\vfuzz`, or a blanket `\resizebox`.
- Every figure and table has a caption and label, is referenced in the text, and is placed right after the paragraph that first mentions it, landing on that page or the next (appendix exempt). Supplements go in the same PDF so references stay links.
- References are verified at the source, never from memory or invented; prefer peer-reviewed, recent, published versions over preprints. Every citation has an entry and every entry is cited. Each entry has a `doi`, else a verified `url`.
- Numeric citations are numbered in order of first appearance (`unsrtnat`, `IEEEtran`, biblatex `sorting=none`). If the venue mandates another order, follow it and say so.
- `hyperref` loaded once (many classes load it); citations, cross-references (`\ref`, `\cref`, never typed numbers), URLs (`\url`, `\href`), and DOIs are clickable.

## Common Rationalizations

| Rationalization              | Reality                                                       |
| ---------------------------- | ------------------------------------------------------------- |
| "It compiled, so it is done" | Cramped tables, drifting floats, and dead links compile fine. |
| "I know this paper's DOI"    | Remembered metadata is often wrong; verify it.                |
| "The project build passes"   | It checks the log only, not placement, links, or citations.   |

## Red Flags

- Finishing without viewing rendered pages, or with PDF checks skipped.
- `--allow`, `[H]`, or `\sloppy` used on body content.

## Verification

- [ ] `RESULT: CLEAN` with PDF checks run; non-200 links from `--check-links` explained.
- [ ] Every page viewed: no overflow, no `??`, figures and tables beside their first mention.
- [ ] References verified; order correct, or the venue's order stated.
- [ ] Deliverable rebuilt; no template file or plot edited.
- [ ] Final reply: PDF path, page count, commands run, each `--allow` line and remaining warning with its reason, anything unverified.
