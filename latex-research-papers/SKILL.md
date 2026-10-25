---
name: latex-research-papers
description: Writes and finalises compile-ready LaTeX research papers in the best-fit journal's official template, compiled with a local Tectonic until there is no overflow, floats sit beside their first mention, references are verified and in order, and links are clickable. Use when the user asks to write, edit, fix, compile, or polish a research paper, manuscript, preprint, thesis chapter, or other academic LaTeX, or its bibliography, figures, tables, overflow, anonymised submission copy, or Turnitin copy without references. Not for resumes (`resume-tailoring`).
---

# LaTeX Research Papers

## Overview

Done means [scripts/paper_check.py](scripts/paper_check.py) prints `RESULT: CLEAN` with its PDF checks run, and every rendered page has been looked at.

## When to Use

- Any academic LaTeX document. Not resumes (`resume-tailoring`). Use `internet-research` for references and `repo-local-workspace` for installs and output.

## Process

1. Read the project's paper README, paper skill, and build command (such as `npm run paper`) and follow them. Numbers come only from the project's result files.
2. Venue: if the user or project already names a target journal, use it. Otherwise, with `internet-research`, shortlist journals whose aims and scope fit the paper's topic, method, and article type, and pick the most suitable one on scope fit, then indexing and reputation, open-access policy and fees, and review time. Confirm on the journal's or publisher's official author guidelines that it offers a downloadable LaTeX template; drop any journal that does not and take the next best. State the choice, the runner-up, and the sources.
3. Template: download the official template from that page into `.agent-local/downloads/<journal>/` (an untrusted download per `repo-local-workspace`), copy it into the paper folder, and build the paper from its sample `.tex`, class, and bibliography style, following the journal's guidelines (article type, abstract and keyword limits, section order, reference style). If the paper already uses that template, keep it; if it uses another, port the content into the official template.
4. Tectonic: `$TECTONIC`, `PATH`, or `tectonic(.exe)` in or near the paper folder. If missing, ask, then install it per [references/fixes.md](references/fixes.md#install-tectonic).
5. Write per the Rules. Never edit the template's `.cls`, `.sty`, or `.bst`, its geometry or fonts, or source plots; patch template quirks in the preamble.
6. Run `python <skill>/scripts/paper_check.py main.tex --render .agent-local/output/paper-pages`; PDF checks need `pypdf` and `pypdfium2` in the repo `.venv`. Fix every blocking item and fixable warning with [references/fixes.md](references/fixes.md), view every page, and repeat. `--allow REGEX` only for a template-internal line confirmed harmless in the PDF.
7. Before finishing, rerun with `--check-links`, then build the deliverable with the project's command, else `tectonic --keep-logs --reruns 3 main.tex` in the paper folder. Git-ignore build artefacts.

## Rules

- The paper uses the target journal's official, unmodified LaTeX template, downloaded from its author guidelines; never a generic `article` class or a look-alike when an official template exists.
- No overflow anywhere: text, figures, tables, equations, captions, bibliography. Never mask it with `\sloppy`, `\hfuzz`, `\vfuzz`, or a blanket `\resizebox`.
- Every figure and table has a caption and label, is referenced in the text, and is placed right after the paragraph that first mentions it, landing on that page or the next (appendix exempt). Supplements go in the same PDF so references stay links; when a separate supplementary PDF is required, link the two documents with `xr-hyper` (`\externaldocument`, compiled main, supplement, main), which `paper_check.py` resolves.
- References are verified at the source, never from memory or invented, and are only peer-reviewed, published journal or conference papers, preferably recent; never preprints (arXiv, bioRxiv, SSRN), books, or other unreviewed sources. If only a preprint exists, drop the claim or report it. Every citation has an entry and every entry is cited. Each entry has a `doi`, else a verified `url`.
- Numeric citations are numbered in order of first appearance (`unsrtnat`, `IEEEtran`, biblatex `sorting=none`). If the venue mandates another order, follow it and say so.
- No semicolons in the paper's text, captions, or highlights: split the sentence or use a comma and conjunction. Only syntax that needs one (TikZ, the class's author-year multi-citation separator) is exempt.
- Every paper ships four PDFs from one source: `main.tex`, `main-anonymised.tex` (double-anonymised submission copy with no author names, e-mails, affiliations, ORCIDs, `pdfauthor`, or identifying links such as the repository URL, "Anonymous" in the running head), `main-title-page.tex` (separate title page: full title, all authors in order, affiliations, abstract, 3 to 5 keywords, and a "Corresponding author" section with name, institutional e-mail, phone, and postal address, asked from the user, never invented, ending after it with `\expandafter\endinput\fi`), and `main-no-references.tex` (Turnitin similarity copy without the reference list, citations still resolved). Each wrapper is `\def\Anonymised{}`, `\def\TitlePage{}`, or `\def\NoReferences{}` then `\input{main}`, and `main.tex` guards those parts with `\ifdefined`. For no references, keep `\bibliography` and redefine `thebibliography` as `{\setbox0=\vbox\bgroup\list{}{}}{\endlist\egroup}` so citations keep their text. A separate supplement gets a matching `supplementary-anonymised.tex`, linked through `\externaldocument{main\Variant}`. Build all of them with the project's command.
- `hyperref` loaded once (many classes load it); citations, cross-references (`\ref`, `\cref`, never typed numbers), URLs (`\url`, `\href`), and DOIs are clickable. The PDF has numbered bookmarks for the title, abstract, every section, and the references.

## Common Rationalizations

| Rationalization              | Reality                                                       |
| ---------------------------- | ------------------------------------------------------------- |
| "It compiled, so it is done" | Cramped tables, drifting floats, and dead links compile fine. |
| "I know this paper's DOI"    | Remembered metadata is often wrong; verify it.                |
| "`article` is close enough"  | Journals desk-reject off-template submissions; use theirs.    |
| "The arXiv version is fine"  | Preprints are unreviewed; cite the peer-reviewed version.     |
| "The project build passes"   | It checks the log only, not placement, links, or citations.   |

## Red Flags

- Choosing a journal without checking its scope, or without confirming its LaTeX template download.
- Finishing without viewing rendered pages, or with PDF checks skipped.
- `--allow`, `[H]`, or `\sloppy` used on body content.

## Verification

- [ ] Journal chosen on scope fit with sources; its official LaTeX template confirmed downloadable and used.
- [ ] `RESULT: CLEAN` with PDF checks run; non-200 links from `--check-links` explained.
- [ ] Every page viewed: no overflow, no `??`, figures and tables beside their first mention.
- [ ] References verified and all peer-reviewed papers, no preprints or books; order correct, or the venue's order stated.
- [ ] Deliverable rebuilt; no template file or plot edited.
- [ ] Anonymised, title-page, and no-references PDFs built and their extracted text checked: no author name, e-mail, or repository URL in the first, no reference list in the second, no semicolon in rendered prose outside citations.
- [ ] Final reply: chosen journal with reasons, runner-up, and template source URL, PDF path, page count, commands run, each `--allow` line and remaining warning with its reason, issues in template files or source plots (reported, not fixed), anything unverified.
