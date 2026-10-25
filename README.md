# Agent Skills

Reusable, model- and harness-neutral agent skills. Each skill is a folder with a `SKILL.md` whose front matter `description` tells the agent when to use it, and whose body tells it how. This is not an application or package: there is nothing to build or deploy.

## Table Of Contents

1. [Skills](#skills)
2. [Installation](#installation)
3. [Repository Structure](#repository-structure)
4. [Notebook Helper](#notebook-helper)
5. [Paper Checker](#paper-checker)
6. [Writing And Maintaining Skills](#writing-and-maintaining-skills)
7. [Troubleshooting](#troubleshooting)
8. [Known Limitations](#known-limitations)

## Skills

| Skill                          | Purpose                                                                                                                                                                                                                                   |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frontend-design`              | Clean, intuitive, fully responsive frontend UI in light and dark modes, built on proven patterns and libraries, with custom components and no browser-native UI.                                                                          |
| `git-commit-and-push`          | Docs check and full local CI until green, then factual commits, `.gitignore` upkeep, strict message format, and push.                                                                                                                     |
| `internet-research`            | Current, source-based research, comparison, validation, and recommendations.                                                                                                                                                              |
| `kaggle-jupyter-notebooks`     | Safe notebook editing for Kaggle GPU T4 x2, with full hardware use, per-cell explanations, progress, metrics, and an output zip.                                                                                                          |
| `latex-research-papers`        | Picks the best-fit journal and uses its official LaTeX template; compiles via local Tectonic: no overflow, well-placed floats, peer-reviewed in-order references, clickable links, no semicolons, plus anonymised and no-references PDFs. |
| `linkedin-project-description` | Turns a project README into a LinkedIn description of at most 1000 characters, using only supported claims.                                                                                                                               |
| `production-architecture`      | Whole-repo re-architecture for production readiness, scalability, modularity, zero redundancy, and a one-command `npm run dev`.                                                                                                           |
| `readme-generator`             | Verified README generation; notebook repositories get a cell-by-cell walkthrough with every metric and output image.                                                                                                                      |
| `repo-local-workspace`         | Keeps tools, caches, helper scripts, logs, outputs, and temp files in a Git-ignored folder inside the repository.                                                                                                                         |
| `research-driven-development`  | Decides whether a task needs research; if so, finds existing libraries, projects, datasets, models, skills, and MCP servers to adopt or adapt before building.                                                                            |
| `resume-tailoring`             | Writes or tailors a single-page LaTeX resume from ground-truth Education, Experience, and Projects documentation.                                                                                                                         |
| `security-hardening`           | Scans the whole repository and its history for every class of vulnerability, then fixes and verifies them.                                                                                                                                |
| `skill-improvement`            | Records each solved hard problem in the skill that loads when it recurs, merging rather than appending, so every problem is solved once.                                                                                                  |

`research-driven-development` is the entry point for new work. `AGENTS.md` routes non-trivial tasks to it, and `frontend-design`, `production-architecture`, and `kaggle-jupyter-notebooks` use it for library, architecture, model, and dataset choices. It picks a tier from the task's complexity, scope, and novelty: Skip (small, well-understood changes), Quick (one bounded choice), or Full (new project, unfamiliar domain, or stack choice). It judges sources by the `internet-research` rules and records lasting decisions in a `RESEARCH.md` at the target repository's root. The prior art behind this design is in this repository's [RESEARCH.md](RESEARCH.md).

`skill-improvement` closes the loop. `AGENTS.md` tells the agent to search the skills for an error's text before debugging it, and to record every hard problem it solves in the skill that loads when the problem recurs. Fixes with no owning skill go in `skill-improvement/references/fixes.md`.

## Installation

There is no install script. Link each skill folder into the skills directory of your agent or harness (for Claude Code, `~/.claude/skills/`), keeping the folder name. A link keeps one source of truth: edits made by `skill-improvement` from any project land in this repository. On Windows a directory junction needs no administrator rights:

```powershell
foreach ($d in Get-ChildItem -Directory | Where-Object { Test-Path "$($_.FullName)\SKILL.md" }) {
  New-Item -ItemType Junction -Path "$HOME\.claude\skills\$($d.Name)" -Target $d.FullName
}
```

On POSIX use `ln -s "$PWD/<skill>" ~/.claude/skills/<skill>`. A harness that does not follow links needs a copy of the whole folder (`SKILL.md`, `agents/`, `references/`, `scripts/`, `assets/`); recopy it after every change.

`agents/openai.yaml` in each skill is optional metadata (`display_name`, `short_description`, `default_prompt`, `allow_implicit_invocation`) for harnesses that read it. Others ignore it.

## Repository Structure

```text
.
|-- AGENTS.md                         agent rules: skills, communication, implementation, verification
|-- README.md
|-- RESEARCH.md                       dated research behind this repository's design decisions
|-- .gitattributes                    text normalisation; fonts, images, PDFs, zips as binary
|-- .gitignore                        local folders, Python and Node artefacts, secrets, logs, editor files
|-- .prettierrc.json                  Prettier: tabs, tab width 2
|-- .prettierignore                   skips .agent-local/, .venv/, .cache/
|-- <skill>/
|   |-- SKILL.md                      skill instructions
|   `-- agents/openai.yaml            optional harness metadata
|-- frontend-design/
|   `-- references/custom-controls.md  browser-native UI to replace with custom components
|-- kaggle-jupyter-notebooks/
|   |-- references/kaggle-authoring.md  hardware, progress, metrics, output layout, zip cell
|   `-- scripts/notebook_doctor.py    notebook maintenance CLI
|-- latex-research-papers/
|   |-- references/fixes.md           overflow, placement, bibliography, link fixes; Tectonic install
|   `-- scripts/paper_check.py        Tectonic compile plus layout, reference, and citation checks
|-- production-architecture/
|   `-- references/local-launch.md    one-command npm run dev launcher rules
|-- readme-generator/
|   `-- references/notebook-walkthrough.md  cell-by-cell README rules for notebook repositories
|-- resume-tailoring/
|   `-- assets/Resume.tex             single-page LaTeX resume template
`-- skill-improvement/
    `-- references/fixes.md           tool and environment fixes no other skill owns
```

`<skill>` stands for each of the 13 skill folders listed above.

## Notebook Helper

[kaggle-jupyter-notebooks/scripts/notebook_doctor.py](kaggle-jupyter-notebooks/scripts/notebook_doctor.py) needs Python 3 and `nbformat`. Install `nbformat` into a repository-local virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install nbformat --cache-dir .cache\pip
.\.venv\Scripts\python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py --help
```

On POSIX shells use `./.venv/bin/python` and forward slashes.

| Subcommand     | Purpose                                                                                                                                                                       |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `inspect`      | Metadata, cell counts, output size (warns above 5 MiB), cell ID and execution count health, hidden-state warnings.                                                            |
| `validate`     | `nbformat` validation plus duplicate cell ID check.                                                                                                                           |
| `repair`       | Converts to format 4, normalises, and fixes missing or duplicate cell IDs.                                                                                                    |
| `clean`        | Clears outputs and execution counts; `--drop-widgets` also removes widget state.                                                                                              |
| `export-code`  | Writes code cells to a Python file with cell index and ID markers (`--output`).                                                                                               |
| `check-kaggle` | Static checks: markdown overview first, markdown before every code cell, code syntax, tqdm used, `/kaggle/working` outputs, no machine paths, final zip cell with `FileLink`. |
| `diff`         | Semantic diff of two notebooks by cell source, type, outputs, and execution counts.                                                                                           |

`repair` and `clean` accept `--backup`. Inside a Git repository, backups go to `<repo>/.agent-local/backups/`; outside one, next to the notebook. The helper never executes notebooks; runtime behaviour is verified only by running on Kaggle.

## Paper Checker

[latex-research-papers/scripts/paper_check.py](latex-research-papers/scripts/paper_check.py) needs Python 3 and a Tectonic binary. It uses `--tectonic <path>`, else `$TECTONIC`, else `tectonic` on `PATH`, else `tectonic.exe` in the paper folder, its parents, and their direct subfolders. The PDF checks need `pypdf`, and `--render` also needs `pypdfium2`; without them those checks are skipped. Install both into a repository-local virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install pypdf pypdfium2 --cache-dir .cache\pip
.\.venv\Scripts\python .\latex-research-papers\scripts\paper_check.py <paper>\main.tex --render .agent-local\output\paper-pages
```

| Option              | Purpose                                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------------------- |
| `--tectonic <path>` | Tectonic binary to use.                                                                              |
| `--outdir <dir>`    | Build directory; default `<repo>/.agent-local/tmp/latex-build/`.                                     |
| `--allow <regex>`   | Accept a log or BibTeX line confirmed harmless in the PDF, such as a template-internal overfull box. |
| `--render <dir>`    | Render every page to `page-NN.png` for visual inspection.                                            |
| `--check-links`     | Request every external link in the PDF and print its HTTP status.                                    |

It compiles with `--keep-logs --keep-intermediates --reruns 3` (Tectonic 0.15 otherwise loops to six passes) and `TECTONIC_CACHE_DIR=<repo>/.cache/tectonic`. It exits 1 on TeX errors, overfull boxes, missing glyphs, undefined or duplicate labels, BibTeX warnings, broken references, missing or uncited bibliography entries, book or preprint entries (book types, arXiv, bioRxiv, medRxiv, SSRN, `eprint`), unreferenced or unlabelled figures and tables, numeric citations out of order of first appearance, or no `hyperref`; and, with `pypdf`, on `??` in the PDF, cited DOIs or URLs that are not links, and body figures or tables more than one page after their first mention. Labels of a document named by `\externaldocument` (`xr` or `xr-hyper`, such as a separate supplementary PDF) count as valid references, read from its `.aux` next to the main file, and entries cited only by that document are not reported as uncited. Underfull boxes, other warnings, bare URLs, and entries without a DOI or URL are listed without failing. Visual overflow still needs a look at the rendered pages.

## Writing And Maintaining Skills

Skills follow the [addyosmani/agent-skills skill anatomy](https://github.com/addyosmani/agent-skills/blob/main/docs/skill-anatomy.md) and load in three levels ([Anthropic skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)):

1. `name` and `description` of every skill: loaded in every session, so this is the most expensive text in the repository.
2. `SKILL.md` body: loaded only when the skill triggers.
3. `references/`, `scripts/`, `assets/`: read or run only when the body points to them for the current task.

Keep each level as small as it can be without the agent making mistakes:

- One skill per workflow. Split a skill that mixes unrelated workflows; reference other skills by name instead of repeating them.
- Front matter has only `name` (matching the folder) and `description`: what the skill does in third person, then a `Use when` clause with every trigger, at most 1024 characters. Rules and details belong in the body, not the description.
- Body sections: `## Overview`, `## When to Use` (including exclusions and the skill to use instead), the process and its rules, `## Common Rationalizations` (excuses for skipping steps, with rebuttals), `## Red Flags`, and `## Verification` (an evidence-based checklist). Keep the body well under 500 lines.
- Never contradict `AGENTS.md`. Where a skill's hard constraint blocks a fix, the skill says to report the issue instead.
- Say each rule once, in imperative form, and give the reason when it is not obvious.
- Cut anything the agent already does by default or that does not change behaviour.
- Move material needed only for some tasks (a sub-workflow, a long checklist, platform-specific detail) into `references/`, linked directly from `SKILL.md` (one level deep) with a pointer saying when to read it. Keep material every run needs inline.
- Record each solved hard problem with `skill-improvement`: search existing entries first, merge instead of appending, and place it where it loads when the problem recurs.
- Update `SKILL.md`, `agents/openai.yaml`, and this README together when a skill is added, renamed, or changes behaviour.
- Never commit `.venv/`, `.cache/`, or `.agent-local/`.

Check formatting with a repository-local npm cache:

```powershell
$env:npm_config_cache = "$PWD\.cache\npm"
npx --yes prettier@3 --check "**/*.{md,json,yaml}"
```

## Troubleshooting

| Problem                                          | Likely cause                                 | Resolution                                                                          |
| ------------------------------------------------ | -------------------------------------------- | ----------------------------------------------------------------------------------- |
| `python` is not recognised.                      | Python is not installed or not on `PATH`.    | Install Python 3 or use the Python launcher on the machine.                         |
| `notebook_doctor.py` reports `nbformat` missing. | The active environment lacks `nbformat`.     | Install it into `.venv` as shown above and run the script with that interpreter.    |
| A notebook is reported as invalid.               | Invalid JSON, schema, or duplicate cell IDs. | Read the `validate` output; if structural, run `repair --backup`.                   |
| `paper_check.py` reports `tectonic not found`.   | Tectonic is not on `PATH` or near the paper. | Pass `--tectonic <path>`, or install it into the project per `references/fixes.md`. |

## Known Limitations

- No automated tests, CI, licence file, or dependency manifest. `nbformat`, `pypdf`, and `pypdfium2` are not version-pinned and no Python version is declared.
- `notebook_doctor.py` is not a secret scanner. Review notebooks manually before sharing them.
