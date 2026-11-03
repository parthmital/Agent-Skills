# Agent Skills

Reusable, model- and harness-neutral agent skills. Each skill is a folder with a `SKILL.md` whose front matter `description` tells the agent when to use it, and whose body tells it how. This is not an application or package: there is nothing to build or deploy.

## Table Of Contents

1. [Skills](#skills)
2. [Installation](#installation)
3. [Repository Structure](#repository-structure)
4. [Notebook Helper](#notebook-helper)
5. [Paper Checker](#paper-checker)
6. [Writing And Maintaining Skills](#writing-and-maintaining-skills)
7. [Checks](#checks)
8. [Troubleshooting](#troubleshooting)
9. [Known Limitations](#known-limitations)
10. [Documentation](#documentation)

## Skills

| Skill                          | Purpose                                                                                                                                                                                                                                                                          |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frontend-design`              | Clean, intuitive, fully responsive frontend UI in light and dark modes, built on proven patterns and libraries, with custom components and no browser-native UI.                                                                                                                 |
| `git-commit-and-push`          | Docs check and full local CI until green, then factual commits, `.gitignore` upkeep, strict message format, and push.                                                                                                                                                            |
| `internet-research`            | Current, source-based research, fact-checking, comparison, and recommendations, weighing every source on its evidence rather than who publishes it.                                                                                                                              |
| `kaggle-jupyter-notebooks`     | Safe notebook editing for Kaggle GPU T4 x2, with full hardware use, per-cell explanations, progress, metrics, and an output zip.                                                                                                                                                 |
| `latex-research-papers`        | Picks the best-fit journal and uses its official LaTeX template; fact-checks every claim and reference; compiles via local Tectonic: no overflow, well-placed floats, peer-reviewed in-order references, clickable links, no semicolons, plus anonymised and no-references PDFs. |
| `linkedin-project-description` | Turns a project README into a LinkedIn description of at most 500 characters, using only supported claims.                                                                                                                                                                       |
| `production-architecture`      | Whole-repo re-architecture for production readiness, scalability, modularity, zero redundancy, and a one-command `npm run dev`.                                                                                                                                                  |
| `project-docs`                 | One compact, agent-first format for the project doc set (`AGENTS.md`, `ARCHITECTURE.md`, `DATABASE.md`, and others), with one purpose per file and no duplication.                                                                                                               |
| `readme-generator`             | Verified README generation; notebook repositories get a cell-by-cell walkthrough with every metric and output image.                                                                                                                                                             |
| `repo-local-workspace`         | Keeps tools, caches, helper scripts, logs, outputs, and temp files in a Git-ignored folder inside the repository.                                                                                                                                                                |
| `research-driven-development`  | Decides whether a task needs research; if so, finds existing libraries, projects, datasets, models, skills, and MCP servers to adopt or adapt before building.                                                                                                                   |
| `resume-tailoring`             | Writes or tailors a single-page LaTeX resume from ground-truth Education, Experience, and Projects documentation.                                                                                                                                                                |
| `security-hardening`           | Scans the whole repository and its history for every class of vulnerability, then fixes and verifies them.                                                                                                                                                                       |
| `skill-improvement`            | Records each solved hard problem in the skill that loads when it recurs, merging rather than appending, so every problem is solved once.                                                                                                                                         |

`research-driven-development` is the entry point for new work. `AGENTS.md` routes non-trivial tasks to it, and `frontend-design`, `production-architecture`, and `kaggle-jupyter-notebooks` use it for library, architecture, model, and dataset choices. It picks a tier from the task's complexity, scope, and novelty: Skip (small, well-understood changes), Quick (one bounded choice), or Full (new project, unfamiliar domain, or stack choice). It judges sources by the `internet-research` rules and records lasting decisions in a `RESEARCH.md` at the target repository's root. The prior art behind this design is in this repository's [RESEARCH.md](RESEARCH.md).

`skill-improvement` closes the loop. `AGENTS.md` tells the agent to search the skills for an error's text before debugging it, and to record every hard problem it solves in the skill that loads when the problem recurs. Fixes with no owning skill go in `skill-improvement/references/fixes.md`.

`project-docs` owns the documentation format of target repositories: which file answers which question, when a file should exist, and one template per file. The skills that write `ARCHITECTURE.md`, `DESIGN.md`, `SECURITY.md`, and `RESEARCH.md` follow its templates, and `README.md` links the rest.

## Installation

There is no install script. Link each skill folder into the skills directory of your agent or harness, keeping the folder name. A link keeps one source of truth: edits made by `skill-improvement` from any project land in this repository.

### Claude Code

On Windows a directory junction needs no administrator rights:

```powershell
foreach ($d in Get-ChildItem -Directory | Where-Object { Test-Path "$($_.FullName)\SKILL.md" }) {
  New-Item -ItemType Junction -Path "$HOME\.claude\skills\$($d.Name)" -Target $d.FullName
}
```

On POSIX use `ln -s "$PWD/<skill>" ~/.claude/skills/<skill>`.

### Google Antigravity

Link this repository as the global skills directory and link the global agent rules (`AGENTS.md`):

```powershell
# Global skills directory junction
New-Item -ItemType Junction -Path "$HOME\.gemini\config\skills" -Target "$PWD"

# Global agent rules symbolic link
cmd.exe /c "mklink `"$HOME\.gemini\config\rules\AGENTS.md`" `"$PWD\AGENTS.md`""
```

A harness that does not follow links needs a copy of the whole folder (`SKILL.md`, `agents/`, `references/`, `scripts/`, `assets/`), recopying it after every change.

`agents/openai.yaml` in each skill is optional metadata (`display_name`, `short_description`, `default_prompt`, `allow_implicit_invocation`) for harnesses that read it. Others ignore it.

## Repository Structure

```text
.
|-- .github/
|   |-- dependabot.yml
|   `-- workflows/ci.yml
|-- scripts/
|   `-- check_repo.py
|-- tests/
|   |-- conftest.py
|   |-- test_notebook_doctor.py
|   `-- test_paper_check.py
|-- <skill>/
|   |-- SKILL.md
|   `-- agents/openai.yaml
|-- frontend-design/references/custom-controls.md
|-- kaggle-jupyter-notebooks/
|   |-- references/kaggle-authoring.md
|   |-- references/runtime-budget.md
|   `-- scripts/notebook_doctor.py
|-- latex-research-papers/
|   |-- references/fixes.md
|   `-- scripts/paper_check.py
|-- production-architecture/references/local-launch.md
|-- project-docs/references/doc-templates.md
|-- readme-generator/references/notebook-walkthrough.md
|-- resume-tailoring/assets/Resume.tex
|-- security-hardening/references/scanner-fixes.md
|-- skill-improvement/references/fixes.md
|-- .gitattributes
|-- .gitignore
|-- .prettierignore
|-- .prettierrc.json
|-- .skillsaw.yaml
|-- AGENTS.md
|-- README.md
|-- RESEARCH.md
|-- pyproject.toml
`-- requirements.txt
```

`<skill>` stands for each of the 14 skill folders listed above. Each has a `SKILL.md` (the instructions) and an `agents/openai.yaml` (optional harness metadata).

| Path                                                      | Purpose                                                                                         |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `frontend-design/references/custom-controls.md`           | Browser-native UI to replace with custom components.                                            |
| `kaggle-jupyter-notebooks/references/kaggle-authoring.md` | Hardware use, liveness logging, deadlock prevention, metrics, output layout, final zip cell.    |
| `kaggle-jupyter-notebooks/references/runtime-budget.md`   | Kaggle session time limit, elastic work, splitting into several notebooks.                      |
| `kaggle-jupyter-notebooks/scripts/notebook_doctor.py`     | Notebook maintenance CLI ([Notebook Helper](#notebook-helper)).                                 |
| `latex-research-papers/references/fixes.md`               | Overflow, float placement, bibliography, and link fixes, and the Tectonic install.              |
| `latex-research-papers/scripts/paper_check.py`            | Tectonic compile plus layout, reference, and citation checks ([Paper Checker](#paper-checker)). |
| `production-architecture/references/local-launch.md`      | Rules for the one-command `npm run dev` launcher.                                               |
| `project-docs/references/doc-templates.md`                | One template per project doc.                                                                   |
| `readme-generator/references/notebook-walkthrough.md`     | Cell-by-cell README rules for notebook repositories.                                            |
| `resume-tailoring/assets/Resume.tex`                      | Single-page LaTeX resume template.                                                              |
| `security-hardening/references/scanner-fixes.md`          | checkov, gitleaks, and zizmor quirks in CI.                                                     |
| `skill-improvement/references/fixes.md`                   | Tool and environment fixes that no other skill owns.                                            |
| `scripts/check_repo.py`                                   | This repository's own skill conventions ([Checks](#checks)).                                    |
| `tests/`                                                  | pytest tests for `notebook_doctor.py` and `paper_check.py`.                                     |
| `.github/workflows/ci.yml`                                | Runs every check in [Checks](#checks) on each push to `main` and each pull request.             |
| `.github/dependabot.yml`                                  | Monthly update pull requests for `requirements.txt` and the pinned GitHub Actions.              |
| `requirements.txt`                                        | Pinned Python packages for the helper scripts and the checks.                                   |
| `pyproject.toml`                                          | ruff and pytest settings only. This is not a Python package.                                    |
| `.skillsaw.yaml`                                          | skillsaw lint settings, with each disabled rule's reason.                                       |
| `.gitattributes`                                          | LF normalisation, and fonts, images, PDFs, and zips as binary.                                  |
| `.prettierrc.json`, `.prettierignore`                     | Prettier settings (tabs, tab width 2) and the local folders it skips.                           |

## Notebook Helper

[kaggle-jupyter-notebooks/scripts/notebook_doctor.py](kaggle-jupyter-notebooks/scripts/notebook_doctor.py) needs Python 3.11 or later and `nbformat`. Install the pinned packages into a repository-local virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt --cache-dir .cache\pip
.\.venv\Scripts\python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py --help
```

On POSIX shells use `./.venv/bin/python` and forward slashes. The helper writes notebooks and exported code with LF line endings on every OS.

| Subcommand     | Purpose                                                                                                                                                                       |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `inspect`      | Metadata, cell counts, output size (warns above 5 MiB), cell ID and execution count health, hidden-state warnings.                                                            |
| `validate`     | `nbformat` validation plus duplicate cell ID check.                                                                                                                           |
| `repair`       | Converts to format 4.5 or later, normalises, and fixes missing or duplicate cell IDs.                                                                                         |
| `clean`        | Clears outputs and execution counts; `--drop-widgets` also removes widget state.                                                                                              |
| `export-code`  | Writes code cells to a Python file with cell index and ID markers (`--output`).                                                                                               |
| `check-kaggle` | Static checks: markdown overview first, markdown before every code cell, code syntax, tqdm used, `/kaggle/working` outputs, no machine paths, final zip cell with `FileLink`. |
| `diff`         | Semantic diff of two notebooks by cell source, type, outputs, and execution counts.                                                                                           |

`repair` and `clean` accept `--backup`. Inside a Git repository, backups go to `<repo>/.agent-local/backups/`; outside one, next to the notebook. The helper never executes notebooks; runtime behaviour is verified only by running on Kaggle.

## Paper Checker

[latex-research-papers/scripts/paper_check.py](latex-research-papers/scripts/paper_check.py) needs Python 3.11 or later and a Tectonic binary. It uses `--tectonic <path>`, else `$TECTONIC`, else `tectonic` on `PATH`, else `tectonic.exe` in the paper folder, its parents, and their direct subfolders. The PDF checks need `pypdf`, and `--render` also needs `pypdfium2` and `pillow`; without them those checks are skipped. Install them into a repository-local virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt --cache-dir .cache\pip
.\.venv\Scripts\python .\latex-research-papers\scripts\paper_check.py <paper>\main.tex --render .agent-local\output\paper-pages
```

| Option              | Purpose                                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------------------- |
| `--tectonic <path>` | Tectonic binary to use.                                                                              |
| `--outdir <dir>`    | Build directory; default `<repo>/.agent-local/tmp/latex-build/`.                                     |
| `--allow <regex>`   | Accept a log or BibTeX line confirmed harmless in the PDF, such as a template-internal overfull box. |
| `--render <dir>`    | Render every page to `page-NN.png` for visual inspection.                                            |
| `--check-links`     | Request every external link in the PDF (HEAD, then GET if refused) and print its HTTP status.        |

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
- Run every command in [Checks](#checks) before committing.

## Checks

CI ([.github/workflows/ci.yml](.github/workflows/ci.yml)) runs these on every push to `main` and every pull request. Run the same commands locally from the repository root after installing `requirements.txt` into `.venv` (see [Notebook Helper](#notebook-helper)). Prettier needs Node.js.

```powershell
$env:npm_config_cache = "$PWD\.cache\npm"
$env:RUFF_CACHE_DIR = "$PWD\.cache\ruff"
.\.venv\Scripts\ruff check .
.\.venv\Scripts\ruff format --check .
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\skillsaw
.\.venv\Scripts\python scripts\check_repo.py
npx --yes prettier@3.9.10 --check "**/*.{md,json,yaml,yml}"
```

| Check                   | What it verifies                                                                                                                                                                                                                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ruff`                  | Lint and formatting of the Python helper scripts and tests.                                                                                                                                                                                                                                      |
| `pytest`                | Behaviour of `notebook_doctor.py` and `paper_check.py`. Nothing calls Tectonic or the network.                                                                                                                                                                                                   |
| `skillsaw`              | [Agent Skills specification](https://agentskills.io/specification) front matter, broken internal references, and content rules. Fails on warnings. Disabled rules and their reasons are in `.skillsaw.yaml`.                                                                                     |
| `scripts/check_repo.py` | This repository's conventions: front matter has only `name` and `description`, every required section exists, `agents/openai.yaml` is complete and names `$<skill>`, every support file is mentioned in its `SKILL.md` and this README, and the Skills table and folder count match the folders. |
| Prettier                | Formatting of Markdown, JSON, and YAML.                                                                                                                                                                                                                                                          |

## Troubleshooting

| Problem                                                                                   | Likely cause                                                                                     | Resolution                                                                                                                           |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| `python` is not recognised.                                                               | Python is not installed or not on `PATH`.                                                        | Install Python 3 or use the Python launcher on the machine.                                                                          |
| `notebook_doctor.py` reports `nbformat` missing.                                          | The active environment lacks `nbformat`.                                                         | Install it into `.venv` as shown above and run the script with that interpreter.                                                     |
| A notebook is reported as invalid.                                                        | Invalid JSON, schema, or duplicate cell IDs.                                                     | Read the `validate` output; if structural, run `repair --backup`.                                                                    |
| `paper_check.py` reports `tectonic not found`.                                            | Tectonic is not on `PATH` or near the paper.                                                     | Pass `--tectonic <path>`, or install it into the project per `references/fixes.md`.                                                  |
| Many files show as modified after formatting, or Git warns "LF will be replaced by CRLF". | Git for Windows checks out CRLF while formatters write LF.                                       | Apply the line-ending entry in `skill-improvement/references/fixes.md`; `git diff --ignore-cr-at-eol --stat` shows the real changes. |
| `check_repo.py` reports a README or `agents/openai.yaml` problem.                         | A skill was added, renamed, or given a support file without updating the README or its metadata. | Update the Skills table, the folder count, the structure tree and table, and `agents/openai.yaml` together.                          |
| `skillsaw` fails on a warning.                                                            | A skill breaks a spec or content rule.                                                           | Run `skillsaw explain <rule-id>`. Fix the skill, or disable a rule in `.skillsaw.yaml` only with its reason.                         |

## Known Limitations

- No licence file, so others have no stated right to reuse these skills.
- `paper_check.py` tests cover its parsing and checks, not a real Tectonic compile or PDF. Run it on a paper after changing it.
- `notebook_doctor.py` is not a secret scanner. Review notebooks manually before sharing them.

## Documentation

| File                       | Answers                                                                         |
| -------------------------- | ------------------------------------------------------------------------------- |
| [AGENTS.md](AGENTS.md)     | Rules every agent follows: skills, communication, implementation, verification. |
| [RESEARCH.md](RESEARCH.md) | What was evaluated before each design decision in this repository.              |
