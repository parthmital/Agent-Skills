# Fixes

Read the section for the problem `paper_check.py` or the rendered pages show.

## Install Tectonic

Only after the user agrees. Save `https://drop-ps1.fullyjustified.net` (Windows) or `https://drop-sh.fullyjustified.net` (POSIX) to `.agent-local/downloads/`, read it, and run it from the folder the build expects (else the repo root) with `powershell -ExecutionPolicy Bypass -File <script>` or `sh <script>`, never piped to `iex` or `sh`. It unpacks `tectonic(.exe)` there, overwriting any copy, and pins its own version (0.17.0 in October 2026); report it. Never add it to `PATH`; Git-ignore it and `.cache/`. First runs download packages. Keep `--reruns 3`: Tectonic 0.15 otherwise loops to six passes.

## Overflow

- Figures: `\includegraphics[width=\linewidth,height=0.4\textheight,keepaspectratio]`; `\columnwidth` in two columns. Crop with `trim`, `clip` (`\adjincludegraphics`).
- Tables: `tabularx` with ragged `X` or `p{}` columns, split cells, `\small`, smaller `\tabcolsep`; then `adjustbox` `max width=\linewidth` if still readable. `longtable` beyond a page.
- Equations: `multline`, `split`, `aligned`.
- URLs, paths, identifiers: `xurl`; `\nolinkurl`; `\renewcommand{\_}{\origunderscore\allowbreak}` after `\let\origunderscore\_`; `\detokenize{#1}` in macros, never `\path` in macro arguments or captions. `\setlength{\emergencystretch}{2em}`.
- Template-internal (for example an empty box in a class `\maketitle`): confirm in the PDF, then `--allow`.

## Placement

- Floats: `[htbp]` right after the first-mentioning paragraph; `figure*` just before it. `\usepackage[section]{placeins}` and `\FloatBarrier`; `\topfraction` 0.9, `\textfraction` 0.07, `\floatpagefraction` 0.8.
- If floats still drift: non-floating `minipage` environments that set `\@captype` and keep the class caption style, plus `\raggedbottom`.

## Bibliography

- Metadata: Crossref `https://api.crossref.org/works?query.bibliographic=<title>&rows=2` (space out to avoid 429); arXiv batch `https://export.arxiv.org/api/query?id_list=ID1,ID2`; publisher pages. DBLP, IEEE Xplore, and JSTOR block automation. Full author lists; DOI-version pages.
- DOI returning 403 or 202: fine if `https://doi.org/<doi>` redirects (302) to the right publisher.
- arXiv-only: `howpublished = {\href{https://arxiv.org/abs/ID}{arXiv:ID}}`. Brace acronyms in titles (`{BERT}`).
- `volume and number` (plainnat): drop `number` from `@inproceedings`. `empty pages` for venues without pages: `--allow`, never invent pages.
- Order: `\usepackage[numbers,sort&compress]{natbib}` with `unsrtnat`; `plain` and `plainnat` sort alphabetically.

## Links

- `\usepackage{doi}` with natbib; if a `.bst` calls `\doi` with `dx.doi.org`, define `\newcommand*{\doi}[1]{\href{https://doi.org/#1}{\path{#1}}}`. `unsrt` and `plain` drop `doi` and `url` fields.
- `cleveref` after `hyperref` with `[capitalise,noabbrev]`; `\hypersetup{pdftitle=..., pdfauthor=...}`.
- Duplicate destinations: give the counter a unique `\theH<counter>`, for algorithmicx `\def\theHALG@line{\thealgorithm.\arabic{ALG@line}}`.
- **PDF has no bookmarks; Tectonic notes "Not writing `main.out`: it would be empty"**: the Elsevier sample line `\let\WriteBookmarks\relax` makes hyperref's XeTeX driver skip every outline entry. Delete it. Add `\hypersetup{bookmarksnumbered=true}`, `\pdfbookmark[1]{...}{...}` before `\maketitle` (title) and after each `\section*`, and `\apptocmd{\bibsection}{\pdfbookmark[1]{References}{references}}{}{}`. The CAS abstract is written verbatim to `\jobname.abs`, which drops a leading command (it prints `[1]Abstractabstract`), so put `\pdfbookmark[1]{Abstract}{abstract}` on the line just before `\begin{abstract}`, not inside it. Check: pypdf `reader.outline` titles and `get_destination_page_number`.
- Harmless stderr: Fontconfig errors, invalid UTF-8 notes from upstream packages.
