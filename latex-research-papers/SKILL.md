---
name: latex-research-papers
description: Writes and finalises compile-ready LaTeX research papers in the best-fit journal's official template, compiled with a local Tectonic until there is no overflow, floats sit beside their first mention, every claim and reference is fact-checked and in order, and links are clickable. Use when the user asks to write, edit, fix, compile, or polish a research paper, manuscript, preprint, thesis chapter, or other academic LaTeX, or its bibliography, figures, tables, overflow, anonymised submission copy, or Turnitin copy without references. Not for resumes (`resume-and-linkedin`).
---

# LaTeX Research Papers

## Overview

Papers go to reviewers who check every claim, so nothing in them is fabricated, assumed, or unverified. Done means every claim and reference is fact-checked, [scripts/check_paper.py](scripts/check_paper.py) prints `RESULT: CLEAN` with its PDF checks run, and every rendered page has been looked at.

## When to Use

- Any academic LaTeX document. Not resumes (`resume-and-linkedin`). Use `internet-research` for every fact check and reference, and `repo-local-workspace` for installs and output.

## Process

1. Read the project's paper README, paper skill, and build command (such as `npm run paper`) and follow them. Numbers come only from the project's result files.
2. Venue: if the user or project already names a target journal, use it. Otherwise, with `internet-research`, shortlist journals whose aims and scope fit the paper's topic, method, and article type, and pick the most suitable one on scope fit, then indexing and reputation, open-access policy and fees, and review time. Confirm on the journal's or publisher's official author guidelines that it offers a downloadable LaTeX template. Drop any journal that does not and take the next best. State the choice, the runner-up, and the sources.
3. Template: download the official template from that page into `.agent-local/downloads/<journal>/` (an untrusted download per `repo-local-workspace`), copy it into the paper folder, and build the paper from its sample `.tex`, class, and bibliography style, following the journal's guidelines (article type, abstract and keyword limits, section order, reference style). If the paper already uses that template, keep it. If it uses another, port the content into the official template.
4. Tectonic: `$TECTONIC`, `PATH`, or `tectonic(.exe)` in or near the paper folder. If missing, ask, then install it per [references/latex-fixes.md](references/latex-fixes.md#install-tectonic).
5. Write per the Rules. Never edit the template's `.cls`, `.sty`, or `.bst`, its geometry or fonts, or source plots. Patch template quirks in the preamble.
6. Fact-check the whole paper, including text you did not write, with `internet-research`: list every factual claim, statistic, date, name, attribution, and citation, and verify each against opened sources or the project's result files per the fact-check and reference Rules. Extract full texts, not snippets: open-access copies, publisher pages, DOI and Crossref metadata, PDFs, and Playwright or other browser automation where pages need it, within legal access. For many references, `subagent-delegation` decides whether batches of per-reference checks go to `research-worker`s: each gets citation keys, the exact claims they support, and the reference Rules, and returns supports, partial, or fails with the quoted passage and URL. Re-check every partial or failing verdict yourself and spot-check supported ones. Fix or remove anything that fails, and keep a claim-to-evidence list for the final reply.
7. Run `python <skill>/scripts/check_paper.py main.tex --render .agent-local/output/paper-pages`. PDF checks need `pypdf`, `pypdfium2`, and `pillow` (for `--render`) in the repo `.venv`. Fix every blocking item and fixable warning with [references/latex-fixes.md](references/latex-fixes.md), view every page, and repeat. `--allow REGEX` only for a template-internal line confirmed harmless in the PDF.
8. Before finishing, rerun with `--check-links`, then build the deliverable with the project's command, else `tectonic --keep-logs --reruns 3 main.tex` in the paper folder. Git-ignore build artefacts.

## Rules

- The paper uses the target journal's official, unmodified LaTeX template, downloaded from its author guidelines. Never use a generic `article` class or a look-alike when an official template exists.
- No overflow anywhere: text, figures, tables, equations, captions, bibliography. Never mask it with `\sloppy`, `\hfuzz`, `\vfuzz`, or a blanket `\resizebox`.
- Every figure and table has a caption and label, is referenced in the text, and is placed right after the paragraph that first mentions it, landing on that page or the next (appendix exempt). Supplements go in the same PDF so references stay links. When a separate supplementary PDF is required, link the two documents with `xr-hyper` (`\externaldocument`, compiled main, supplement, main), which `check_paper.py` resolves.
- Every factual claim is verified, never assumed or written from memory: results, numbers, and figures trace to the project's result files, and every external fact to an opened source weighed by the `internet-research` Source Rules. Each claim states exactly what its evidence supports, with no overstated generality, causality, or novelty. A claim that cannot be verified is removed or reported, never kept.
- Each reference is checked at the source: it exists (DOI resolves or the publisher page is found), is accessible, has correct metadata (authors, title, venue, year, volume, issue, pages, DOI), is not retracted, and genuinely supports the specific claim it is cited for, confirmed by reading the relevant passage, not only the title or abstract. When the full text is not legally accessible, say which claims rest on the abstract alone.
- References are never from memory or invented, and are only peer-reviewed, published journal or conference papers, preferably recent, and never preprints (arXiv, bioRxiv, SSRN), books, or other unreviewed sources. If only a preprint exists, drop the claim or report it. Every citation has an entry and every entry is cited. Each entry has a `doi`, else a verified `url`.
- Numeric citations are numbered in order of first appearance (`unsrtnat`, `IEEEtran`, biblatex `sorting=none`). If the venue mandates another order, follow it and say so.
- No semicolons in the paper's text, captions, or highlights: split the sentence or use a comma and conjunction. Only syntax that needs one (TikZ, the class's author-year multi-citation separator) is exempt.
- Every paper ships four PDFs from one source: `main.tex`, `main-anonymised.tex` (double-anonymised submission copy with no author names, e-mails, affiliations, ORCIDs, `pdfauthor`, or identifying links such as the repository URL, "Anonymous" in the running head), `main-title-page.tex` (separate title page: full title, all authors in order, affiliations, abstract, 3 to 5 keywords, and a "Corresponding author" section with name, institutional e-mail, phone, and postal address, asked from the user, never invented, ending after it with `\expandafter\endinput\fi`, so its wrapper ends with `\end{document}`), and `main-no-references.tex` (Turnitin similarity copy without the reference list, citations still resolved). Each wrapper is `\def\Anonymised{}`, `\def\TitlePage{}`, or `\def\NoReferences{}` then `\input{main}`, and `main.tex` guards those parts with `\ifdefined`. For no references, keep `\bibliography` and redefine `thebibliography` as `{\setbox0=\vbox\bgroup\list{}{\usecounter{enumiv}}}{\endlist\egroup}` (inside `\makeatletter`) so citations keep their numbers. Without the counter `\bibitem` fails with `Undefined control sequence` at `\@listctr`. A separate supplement (when the venue's page limit forces one, see [references/latex-fixes.md](references/latex-fixes.md#links)) gets a matching `supplementary-anonymised.tex`, linked through `\externaldocument{main\Variant}`. Build all of them with the project's command.
- `hyperref` loaded once (many classes load it), citations, cross-references (`\ref`, `\cref`, never typed numbers), URLs (`\url`, `\href`), and DOIs are clickable. The PDF has numbered bookmarks for the title, abstract, every section, and the references.

## Examples

Bad: `Transformers outperform CNNs on all vision tasks [12]; see Figure 3.` (unchecked claim, typed figure number, semicolon)

Good (illustrative, every number verified against the cited paper before use): `On ImageNet-1k, ViT-B/16 reaches 77.9\% top-1 accuracy when pre-trained on ImageNet-1k alone \cite{dosovitskiy2021vit}, below comparable ResNets without larger pre-training data (Fig.~\ref{fig:accuracy}).` (claim narrowed to what the cited table shows, verified at the passage level, clickable reference)

Bad reference: `@misc{vit, title={An Image is Worth 16x16 Words}, note={arXiv:2010.11929}}` (preprint). Good: the peer-reviewed ICLR 2021 entry with its verified `url`.

## Common Rationalisations

| Rationalisation              | Reality                                                       |
| ---------------------------- | ------------------------------------------------------------- |
| "It compiled, so it is done" | Cramped tables, drifting floats, and dead links compile fine. |
| "I know this paper's DOI"    | Remembered metadata is often wrong. Verify it.                |
| "The title fits the claim"   | Titles and abstracts overstate. Read the passage.             |
| "That fact is well known"    | Reviewers check it anyway. Cite or verify it.                 |
| "`article` is close enough"  | Journals desk-reject off-template submissions. Use theirs.    |
| "The arXiv version is fine"  | Preprints are unreviewed. Cite the peer-reviewed version.     |
| "The project build passes"   | It checks the log only, not placement, links, or citations.   |

## Red Flags

- Choosing a journal without checking its scope, or without confirming its LaTeX template download.
- Finishing without viewing rendered pages, or with PDF checks skipped.
- A citation added for a claim without opening the cited work, or a number in the text with no result file or source behind it.
- `--allow`, `[H]`, or `\sloppy` used on body content.

## Verification

- [ ] Journal chosen on scope fit with sources, and its official LaTeX template confirmed downloadable and used.
- [ ] `RESULT: CLEAN` with PDF checks run, and non-200 links from `--check-links` explained.
- [ ] Every page viewed: no overflow, no `??`, figures and tables beside their first mention.
- [ ] Every factual claim traced to a result file or opened source, and unverifiable claims removed or reported.
- [ ] Every reference exists, is accessible, has correct metadata, is not retracted, and supports its claim at the passage level. All are peer-reviewed papers, no preprints or books. Order correct, or the venue's order stated.
- [ ] Deliverable rebuilt, and no template file or plot edited.
- [ ] Anonymised, title-page, and no-references PDFs built and their extracted text checked: no author name, e-mail, or repository URL in the anonymised copy, the title page complete and ending after the corresponding author, no reference list in the no-references copy, and no semicolon in rendered prose outside citations.
- [ ] Final reply: chosen journal with reasons, runner-up, and template source URL, PDF path, page count, commands run, each `--allow` line and remaining warning with its reason, issues in template files or source plots (reported, not fixed), claims removed or changed by fact-checking, claims resting on abstracts only, anything unverified.
