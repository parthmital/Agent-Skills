# Agent Skills

Reusable, model- and harness-neutral agent skills. Each skill is a folder with a `SKILL.md` whose front matter `description` tells the agent when to use it, and whose body tells it how. This is not an application or package: there is nothing to build or deploy.

## Table Of Contents

1. [Skills](#skills)
2. [Installation](#installation)
3. [Repository Structure](#repository-structure)
4. [Notebook Helper](#notebook-helper)
5. [Writing And Maintaining Skills](#writing-and-maintaining-skills)
6. [Troubleshooting](#troubleshooting)
7. [Known Limitations](#known-limitations)

## Skills

| Skill                          | Purpose                                                                                                                          |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `codebase-architecture`        | Reviews, plans, hardens, cleans up, deduplicates, and documents codebase structure.                                              |
| `frontend-design`              | Clean, functional frontend UI and UX with fully custom components and no browser-native UI.                                      |
| `git-commit-and-push`          | Factual commits from inspected changes, `.gitignore` upkeep, strict message format, and push.                                    |
| `internet-research`            | Current, source-based research, comparison, validation, and recommendations.                                                     |
| `kaggle-jupyter-notebooks`     | Safe notebook editing for Kaggle GPU T4 x2, with full hardware use, per-cell explanations, progress, metrics, and an output zip. |
| `linkedin-project-description` | Turns a project README into a LinkedIn description of at most 1000 characters, using only supported claims.                      |
| `readme-generator`             | Verified README generation; notebook repositories get a cell-by-cell walkthrough with every metric and output image.             |
| `repo-local-workspace`         | Keeps tools, caches, helper scripts, logs, outputs, and temp files in a Git-ignored folder inside the repository.                |
| `resume-tailoring`             | Writes or tailors a single-page LaTeX resume from ground-truth Education, Experience, and Projects documentation.                |

## Installation

There is no install script. To use a skill, copy its whole folder into the skills directory of your agent or harness, keeping the folder name and every file in it (`SKILL.md`, `agents/`, `references/`, `scripts/`, `assets/`). The skills directory location depends on the harness.

`agents/openai.yaml` in each skill is optional metadata (`display_name`, `short_description`, `default_prompt`, `allow_implicit_invocation`) for harnesses that read it. Others ignore it.

## Repository Structure

```text
.
|-- AGENTS.md                         general coding and response rules for agents
|-- README.md
|-- .gitattributes                    text normalisation; fonts, images, PDFs, zips as binary
|-- .gitignore                        local folders, Python and Node artefacts, secrets, logs, editor files
|-- .prettierrc.json                  Prettier: tabs, tab width 2
|-- .prettierignore                   skips .agent-local/, .venv/, .cache/
|-- <skill>/
|   |-- SKILL.md                      skill instructions
|   `-- agents/openai.yaml            optional harness metadata
|-- kaggle-jupyter-notebooks/
|   |-- README.md                     setup notes for the helper
|   |-- references/
|   |   |-- kaggle-authoring.md       hardware, progress, metrics, output layout, zip cell
|   |   `-- precommit.md              optional nbdime and nbstripout setup
|   `-- scripts/notebook_doctor.py    notebook maintenance CLI
`-- resume-tailoring/
    `-- assets/Resume.tex             single-page LaTeX resume template
```

`<skill>` stands for each of the 9 skill folders listed above.

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

## Writing And Maintaining Skills

Skills load into the agent's context, so every line costs tokens. Keep them tight:

- Put all "when to use" triggers in the front matter `description`. The body is loaded only after the skill triggers, so it covers how, not when.
- Say each rule once, in imperative form, and give the reason when it is not obvious. A reason generalises better than an all-caps rule.
- Cut anything the agent already does by default or that does not change behaviour.
- Move long material needed only for some tasks into `references/`, with a clear pointer from `SKILL.md` saying when to read it.
- Update `SKILL.md`, `agents/openai.yaml`, and this README together when a skill is added, renamed, or changes behaviour.
- Never commit `.venv/`, `.cache/`, or `.agent-local/`.

Check formatting with a repository-local npm cache:

```powershell
$env:npm_config_cache = "$PWD\.cache\npm"
npx --yes prettier@3 --check "**/*.{md,json,yaml}"
```

## Troubleshooting

| Problem                                          | Likely cause                                 | Resolution                                                                       |
| ------------------------------------------------ | -------------------------------------------- | -------------------------------------------------------------------------------- |
| `python` is not recognised.                      | Python is not installed or not on `PATH`.    | Install Python 3 or use the Python launcher on the machine.                      |
| `notebook_doctor.py` reports `nbformat` missing. | The active environment lacks `nbformat`.     | Install it into `.venv` as shown above and run the script with that interpreter. |
| A notebook is reported as invalid.               | Invalid JSON, schema, or duplicate cell IDs. | Read the `validate` output; if structural, run `repair --backup`.                |

## Known Limitations

- No automated tests, CI, licence file, or dependency manifest. `nbformat` is not version-pinned and no Python version is declared.
- `notebook_doctor.py` is not a secret scanner. Review notebooks manually before sharing them.
