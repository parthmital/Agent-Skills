# Agent Skills

## Table Of Contents

1. [Quick Start](#quick-start)
2. [Project Overview](#project-overview)
3. [Skills In This Repository](#skills-in-this-repository)
4. [Repository Structure](#repository-structure)
5. [Technology Stack](#technology-stack)
6. [Prerequisites](#prerequisites)
7. [Local Installation](#local-installation)
8. [Dependency Installation](#dependency-installation)
9. [Running Commands](#running-commands)
10. [Notebook Utility](#notebook-utility)
11. [Environment Configuration](#environment-configuration)
12. [Input Validation And Error Handling](#input-validation-and-error-handling)
13. [Testing And Verification](#testing-and-verification)
14. [Code Quality Checks](#code-quality-checks)
15. [Build, Deployment, And CI](#build-deployment-and-ci)
16. [Repository Metrics](#repository-metrics)
17. [Security Notes](#security-notes)
18. [Maintenance Notes](#maintenance-notes)
19. [Troubleshooting](#troubleshooting)
20. [Known Limitations](#known-limitations)
21. [Contribution Guidelines](#contribution-guidelines)
22. [Licence](#licence)
23. [Support](#support)

## Quick Start

This repository stores reusable agent skills that are intended to be model and harness neutral. It is not a web application, API service, Python package, or Node package.

Run all commands in this section from the repository root.

### 1. Confirm the repository root

```powershell
Get-ChildItem .prettierrc.json
```

What it does: checks that the shell is in the folder that contains the repository level configuration file.

Expected result: PowerShell prints `.prettierrc.json`.

Common error: if the file is not found, change to the folder that contains `README.md` and the skill folders.

### 2. List the available skills

```powershell
Get-ChildItem -Directory | Where-Object { $_.Name -ne ".git" }
```

What it does: lists the top level skill folders.

Expected result: the command shows 14 skill folders, including `readme-generator` and `kaggle-jupyter-notebooks`.

Common error: if only `.git` or unrelated folders are shown, the shell is in the wrong directory.

### 3. Read a skill instruction file

```powershell
Get-Content .\readme-generator\SKILL.md
```

What it does: prints the README generator skill instructions.

Expected result: the file starts with YAML front matter and then the `# README Generator` heading.

Common error: if the path is not found, confirm that the `readme-generator` folder exists in the repository root.

### 4. Smoke test the notebook helper

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py --help
```

What it does: runs the notebook helper in help mode and avoids creating `__pycache__` files.

Expected result: the command prints usage text and these subcommands: `inspect`, `validate`, `repair`, `clean`, `export-code`, `check-kaggle`, and `diff`.

Common errors:

| Problem                                                            | Likely cause                                                  | Resolution                                                                                                         |
| ------------------------------------------------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `python` is not recognised.                                        | Python is not installed or not on `PATH`.                     | Install Python 3 or use the Python launcher available on the machine.                                              |
| Missing dependency: install with `python -m pip install nbformat`. | `nbformat` is not installed in the active Python environment. | Install `nbformat` in a local virtual environment as shown in [Dependency Installation](#dependency-installation). |
| The script path is not found.                                      | The command was not run from the repository root.             | Change to the repository root and run the command again.                                                           |

## Project Overview

This repository contains reusable agent skills. A skill is a folder with a `SKILL.md` file that explains when and how an agent should handle a class of tasks. The `SKILL.md` files avoid depending on any one model or harness.

Each skill in this repository also includes an optional `agents/openai.yaml` metadata file for harnesses that read it. Harnesses that do not use it ignore it. That file provides:

- `display_name`
- `short_description`
- `default_prompt`
- `allow_implicit_invocation`

Seven skills are third-party skills installed from [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill). See [Licence](#licence) for their origin and local changes.

One first-party skill, `kaggle-jupyter-notebooks`, also includes a Python helper script for safe notebook inspection, validation, repair, cleaning, export, Kaggle convention checks, and semantic diff.

## Skills In This Repository

| Skill                      | Purpose                                                                                                                                        | Main files                                                                                                                                                                         |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `banner-design`            | Designs banners for social media, ads, website heroes, and print, with several art direction options. Third-party, MIT.                        | [banner-design/SKILL.md](banner-design/SKILL.md)                                                                                                                                   |
| `brand-guidelines`         | Brand voice, visual identity, messaging frameworks, asset management, and brand consistency checks. Third-party, MIT.                          | [brand-guidelines/SKILL.md](brand-guidelines/SKILL.md), [brand-guidelines/scripts/](brand-guidelines/scripts/)                                                                     |
| `codebase-architecture`    | Reviews, plans, hardens, cleans up, deduplicates, and documents codebase structure.                                                            | [codebase-architecture/SKILL.md](codebase-architecture/SKILL.md), [codebase-architecture/agents/openai.yaml](codebase-architecture/agents/openai.yaml)                             |
| `design-system`            | Three-layer design tokens, component specifications, token validation, and slide generation. Third-party, MIT.                                 | [design-system/SKILL.md](design-system/SKILL.md), [design-system/scripts/](design-system/scripts/)                                                                                 |
| `frontend-design`          | Guides clean, functional frontend UI and UX work with fully custom components and no browser-native UI.                                        | [frontend-design/SKILL.md](frontend-design/SKILL.md), [frontend-design/agents/openai.yaml](frontend-design/agents/openai.yaml)                                                     |
| `git-commit-and-push`      | Creates factual Git commits with inspected changes and strict commit message formatting.                                                       | [git-commit-and-push/SKILL.md](git-commit-and-push/SKILL.md), [git-commit-and-push/agents/openai.yaml](git-commit-and-push/agents/openai.yaml)                                     |
| `graphic-design`           | Brand identity, logos, corporate identity programs, icons, social images, slides, and banners. Optional AI image generation. Third-party, MIT. | [graphic-design/SKILL.md](graphic-design/SKILL.md), [graphic-design/scripts/](graphic-design/scripts/)                                                                             |
| `html-presentations`       | Strategic HTML presentations with Chart.js, design tokens, and copywriting formulas. Third-party, MIT.                                         | [html-presentations/SKILL.md](html-presentations/SKILL.md)                                                                                                                         |
| `internet-research`        | Guides current, source based research, comparison, validation, and recommendation work.                                                        | [internet-research/SKILL.md](internet-research/SKILL.md), [internet-research/agents/openai.yaml](internet-research/agents/openai.yaml)                                             |
| `kaggle-jupyter-notebooks` | Safe notebook editing, with Kaggle GPU T4 x2 as the default runtime and rules for documentation, progress, metrics, and output zips.           | [kaggle-jupyter-notebooks/SKILL.md](kaggle-jupyter-notebooks/SKILL.md), [kaggle-jupyter-notebooks/scripts/notebook_doctor.py](kaggle-jupyter-notebooks/scripts/notebook_doctor.py) |
| `readme-generator`         | Generates or updates a verified repository README from inspected repository facts.                                                             | [readme-generator/SKILL.md](readme-generator/SKILL.md), [readme-generator/agents/openai.yaml](readme-generator/agents/openai.yaml)                                                 |
| `repo-local-workspace`     | Keeps tools, caches, helper scripts, logs, outputs, and temp files in a Git-ignored folder inside the repository.                              | [repo-local-workspace/SKILL.md](repo-local-workspace/SKILL.md), [repo-local-workspace/agents/openai.yaml](repo-local-workspace/agents/openai.yaml)                                 |
| `shadcn-tailwind-ui`       | shadcn/ui components, Tailwind CSS styling, and canvas-based visual designs. Third-party, Apache 2.0.                                          | [shadcn-tailwind-ui/SKILL.md](shadcn-tailwind-ui/SKILL.md), [shadcn-tailwind-ui/scripts/](shadcn-tailwind-ui/scripts/)                                                             |
| `ui-ux-design-reference`   | Searchable UI/UX design data: styles, palettes, font pairings, UX guidelines, charts, and stack guidance. Third-party, MIT.                    | [ui-ux-design-reference/SKILL.md](ui-ux-design-reference/SKILL.md), [ui-ux-design-reference/scripts/search.py](ui-ux-design-reference/scripts/search.py)                           |

## Repository Structure

```text
.
|-- .gitattributes
|-- .gitignore
|-- .prettierignore
|-- .prettierrc.json
|-- AGENTS.md
|-- README.md
|-- banner-design/             third-party: SKILL.md, LICENSE, agents/, references/
|-- brand-guidelines/          third-party: SKILL.md, LICENSE, agents/, references/, scripts/, templates/
|-- codebase-architecture/
|   |-- SKILL.md
|   `-- agents/
|       `-- openai.yaml
|-- design-system/             third-party: SKILL.md, LICENSE, agents/, data/, references/, scripts/, templates/
|-- frontend-design/
|   |-- SKILL.md
|   `-- agents/
|       `-- openai.yaml
|-- git-commit-and-push/
|   |-- SKILL.md
|   `-- agents/
|       `-- openai.yaml
|-- graphic-design/            third-party: SKILL.md, LICENSE, agents/, data/, references/, scripts/
|-- html-presentations/        third-party: SKILL.md, LICENSE, agents/, references/
|-- internet-research/
|   |-- SKILL.md
|   `-- agents/
|       `-- openai.yaml
|-- kaggle-jupyter-notebooks/
|   |-- README.md
|   |-- SKILL.md
|   |-- agents/
|   |   `-- openai.yaml
|   |-- references/
|   |   `-- precommit.md
|   `-- scripts/
|       `-- notebook_doctor.py
|-- readme-generator/
|   |-- SKILL.md
|   `-- agents/
|       `-- openai.yaml
|-- repo-local-workspace/
|   |-- SKILL.md
|   `-- agents/
|       `-- openai.yaml
|-- shadcn-tailwind-ui/        third-party: SKILL.md, LICENSE.txt, agents/, canvas-fonts/, references/, scripts/
`-- ui-ux-design-reference/
    |-- LICENSE
    |-- SKILL.md
    |-- agents/
    |   `-- openai.yaml
    |-- data/           design data CSV and JSON files
    |-- references/     quick-reference.md and pro-rules.md
    `-- scripts/        search.py, core.py, design_system.py, and tests/
```

Important paths:

- `.gitattributes`: enables automatic text file normalisation, pins `ui-ux-design-reference/data/` CSV and JSON files to LF so their stored hashes match, and marks fonts and images as binary.
- `.gitignore`: keeps local folders (`.agent-local/`, `.venv/`, `.cache/`), Python and Node.js artefacts, notebook helper backups, secrets files, logs, and editor files out of Git.
- `.prettierignore`: stops Prettier from reformatting the third-party skills, which are kept identical to upstream apart from the listed local changes.
- `.prettierrc.json`: stores formatter preferences for tabs and tab width.
- `AGENTS.md`: stores general coding and response guidelines for agents working in this repository.
- `*/SKILL.md`: stores the main instructions for each skill.
- `*/agents/openai.yaml`: stores optional display and invocation metadata for harnesses that read it.
- `kaggle-jupyter-notebooks/README.md`: gives short setup notes for the notebook skill.
- `kaggle-jupyter-notebooks/references/precommit.md`: documents optional notebook Git protection commands.
- `kaggle-jupyter-notebooks/scripts/notebook_doctor.py`: provides the notebook maintenance command line tool.
- `ui-ux-design-reference/scripts/search.py`: searches the bundled design data. It uses only the Python standard library and makes no network calls.
- `*/LICENSE` and `shadcn-tailwind-ui/LICENSE.txt`: licences for the third-party skills.

## Technology Stack

| Technology             | Version                       | Purpose                                                            | Where used                                             | Notes                                                         |
| ---------------------- | ----------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------------- |
| Markdown               | Not declared                  | Stores skill instructions and documentation.                       | `README.md`, `SKILL.md`, and reference files.          | Agents read skill behaviour from Markdown files.              |
| YAML                   | Not declared                  | Stores skill metadata.                                             | `agents/openai.yaml` files.                            | Each metadata file enables implicit invocation.               |
| Python                 | Exact version not declared    | Runs the notebook helper and the third-party skill scripts.        | `*/scripts/*.py`.                                      | `shadcn-tailwind-ui` requires Python 3.10 or later.           |
| Node.js                | Exact version not declared    | Runs the `.cjs` scripts in `brand-guidelines` and `design-system`. | `brand-guidelines/scripts/`, `design-system/scripts/`. | `shadcn-tailwind-ui` notes Node.js 18 or later for shadcn/ui. |
| `nbformat`             | Exact version not declared    | Reads, writes, converts, normalises, and validates notebooks.      | Imported by `notebook_doctor.py`.                      | The script exits with an install message if it is missing.    |
| Git                    | Exact version not declared    | Tracks repository changes and applies `.gitattributes`.            | `.git`, `.gitattributes`.                              | The current folder is a Git work tree.                        |
| Prettier configuration | Prettier version not declared | Defines formatting preferences.                                    | `.prettierrc.json`.                                    | The file sets `useTabs` to `true` and `tabWidth` to `2`.      |

No root package manager manifest is present. There is no root `package.json`, `pyproject.toml`, `requirements.txt`, lock file, or setup file. `shadcn-tailwind-ui/scripts/requirements.txt` lists only test dependencies.

## Prerequisites

| Prerequisite                      | Required for                                              | Version                         | Verification                                                                  |
| --------------------------------- | --------------------------------------------------------- | ------------------------------- | ----------------------------------------------------------------------------- |
| Skill compatible agent or harness | Using these folders as skills.                            | Not declared in the repository. | The repository contains skill folders with `SKILL.md`.                        |
| Git                               | Repository maintenance.                                   | Not declared in the repository. | `git rev-parse --is-inside-work-tree` returns `true`.                         |
| Python 3                          | Running `notebook_doctor.py`.                             | Exact version not declared.     | The script has a Python 3 shebang and uses Python 3 syntax.                   |
| `nbformat`                        | Notebook helper commands.                                 | Exact version not declared.     | The script imports `nbformat` and the help command runs when it is installed. |
| Node.js                           | `.cjs` scripts in `brand-guidelines` and `design-system`. | Not declared.                   | `node --version`.                                                             |

## Local Installation

There is no repository level install script.

To use a skill locally:

1. Keep this repository in a stable folder.
2. Copy the required skill folder into the skills directory used by your agent or harness.
3. Preserve the folder name.
4. Preserve the `SKILL.md` file.
5. Preserve any supporting files in that skill folder, such as `scripts/`, `references/`, and `agents/`.

The repository does not declare an exact skills directory path because that depends on the agent or harness in use.

## Dependency Installation

The repository has one verified runtime dependency for the notebook helper: `nbformat`.

Use a repository local virtual environment when installing it:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip --cache-dir .cache\pip
.\.venv\Scripts\python -m pip install nbformat --cache-dir .cache\pip
```

What these commands do:

- Create a local Python virtual environment in `.venv`.
- Upgrade pip inside that virtual environment.
- Install `nbformat` while keeping the pip cache under `.cache\pip`.

Expected result: `.\.venv\Scripts\python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py --help` prints the notebook helper usage text.

These dependency setup commands were not executed while preparing this README because they create local environment and cache folders. The notebook helper itself was smoke tested with the current Python environment.

Optional notebook repository protection tools are documented in [kaggle-jupyter-notebooks/references/precommit.md](kaggle-jupyter-notebooks/references/precommit.md):

```powershell
.\.venv\Scripts\python -m pip install nbformat nbstripout nbdime
.\.venv\Scripts\nbdime config-git --enable
.\.venv\Scripts\nbstripout --install
```

Those optional commands install into the local virtual environment and write to the repository `.git/config`. They were not executed while preparing this README.

## Running Commands

There is no long running application to start.

Useful repository commands:

| Command                                                               | Purpose                               | Expected result                                                           |
| --------------------------------------------------------------------- | ------------------------------------- | ------------------------------------------------------------------------- |
| `rg --files -g '!.git'`                                               | List repository files outside `.git`. | Prints 274 tracked or working tree files in the current repository state. |
| `Get-ChildItem -Directory \| Where-Object { $_.Name -ne ".git" }`     | List skill folders.                   | Prints 14 skill folders.                                                  |
| `Get-Content .\readme-generator\SKILL.md`                             | Read the README generator skill.      | Prints the selected skill instructions.                                   |
| `python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py --help` | Run the notebook helper help command. | Prints usage text and 7 subcommands.                                      |

## Notebook Utility

The notebook helper is [kaggle-jupyter-notebooks/scripts/notebook_doctor.py](kaggle-jupyter-notebooks/scripts/notebook_doctor.py).

Available subcommands:

| Subcommand     | Purpose                                                                                                                                                                                                                                            |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `inspect`      | Prints notebook metadata, cell counts, output size, cell ID health, execution count health, and warnings.                                                                                                                                          |
| `validate`     | Validates notebook structure through `nbformat` and checks duplicate cell IDs.                                                                                                                                                                     |
| `repair`       | Converts the notebook to format 4, normalises it, and repairs missing or duplicate cell IDs.                                                                                                                                                       |
| `clean`        | Clears code cell outputs and execution counts, with optional widget metadata removal.                                                                                                                                                              |
| `export-code`  | Exports code cells to a Python file with cell index and cell ID markers.                                                                                                                                                                           |
| `check-kaggle` | Statically checks Kaggle notebook conventions: markdown overview first, markdown before every code cell, code syntax, tqdm use, `/kaggle/working` outputs, no machine-specific paths, and a final zip cell with a `FileLink`. Nothing is executed. |
| `diff`         | Prints a semantic diff between two notebooks based on cell source, type, outputs, and execution counts.                                                                                                                                            |

Examples:

```powershell
python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py inspect path\to\notebook.ipynb
python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py validate path\to\notebook.ipynb
python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py repair path\to\notebook.ipynb --backup
python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py clean path\to\notebook.ipynb --backup
python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py clean path\to\notebook.ipynb --backup --drop-widgets
python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py export-code path\to\notebook.ipynb --output path\to\notebook_cells.py
python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py check-kaggle path\to\notebook.ipynb
python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py diff before.ipynb after.ipynb
```

When `--backup` is used inside a Git repository, backups are written to `<repo>/.agent-local/backups/`. Outside a repository, they are written next to the notebook.

Notebooks are not executed locally. The skill targets Kaggle, so runtime behaviour is verified only by running the notebook on Kaggle.

## Environment Configuration

The first-party skills read no environment variables. Some scripts in the third-party skills read these optional variables:

| Variable name                | Required | Purpose                                                                                 | Expected format | Safe example value | Default value             | Security notes                              |
| ---------------------------- | -------- | --------------------------------------------------------------------------------------- | --------------- | ------------------ | ------------------------- | ------------------------------------------- |
| `GEMINI_API_KEY`             | Optional | Gemini image generation in `graphic-design` logo, icon, and corporate identity scripts. | API key string  | `your-key-here`    | None                      | Secret. Keep it out of scripts and logs.    |
| `GOOGLE_API_KEY`             | Optional | Alternative name for the Gemini key in `graphic-design` scripts.                        | API key string  | `your-key-here`    | None                      | Secret. Keep it out of scripts and logs.    |
| `ATLASCLOUD_API_KEY`         | Optional | Atlas Cloud image generation in `graphic-design/scripts/logo/generate.py`.              | API key string  | `your-key-here`    | None                      | Secret. Sends prompts to api.atlascloud.ai. |
| `MUAPI_API_KEY`              | Optional | MuAPI image generation in `graphic-design/scripts/logo/generate.py`.                    | API key string  | `your-key-here`    | None                      | Secret. Sends prompts to api.muapi.ai.      |
| `DESIGN_SYSTEM_PROJECT_ROOT` | Optional | Overrides the project root used by `design-system` scripts.                             | Absolute path   | `D:\projects\app`  | Current working directory | Not secret.                                 |

Without these keys, the image generation features in `graphic-design` do not run. All other scripts work without network access or keys.

## Input Validation And Error Handling

The repository contains input validation and error handling in `kaggle-jupyter-notebooks/scripts/notebook_doctor.py`.

Verified behaviour:

- Missing `nbformat` exits with an install message.
- Invalid JSON exits with an explicit message.
- Notebook read failures exit with the failing path and error.
- `validate` runs `nbformat.validate`.
- Duplicate cell IDs are reported as invalid.
- `repair` converts notebooks to format 4 and regenerates missing or duplicate cell IDs.
- `atomic_write` writes to a temporary file, validates the notebook, and then replaces the target file.
- `inspect` warns when embedded notebook outputs exceed 5 MiB.

No API input validation exists because the repository contains no API server.

## Testing And Verification

The third-party skills include pytest and unittest test modules:

| Skill                    | Test modules | Tests | Result |
| ------------------------ | ------------ | ----- | ------ |
| `brand-guidelines`       | 1            | 15    | Passed |
| `graphic-design`         | 1            | 12    | Passed |
| `design-system`          | 1            | 2     | Passed |
| `shadcn-tailwind-ui`     | 2            | 64    | Passed |
| `ui-ux-design-reference` | 9            | 133   | Passed |

`banner-design` and `html-presentations` have no tests. No tests exist for `notebook_doctor.py`.

Run them with pytest from a repository local virtual environment. The `brand-guidelines` tests also need Node.js because they run the `.cjs` scripts.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install pytest pytest-mock --cache-dir .cache\pip
.\.venv\Scripts\python -m pytest -q -p no:cacheprovider brand-guidelines graphic-design design-system shadcn-tailwind-ui ui-ux-design-reference
```

Verification run while preparing this README:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py --help
```

Result: passed. The command printed usage text and listed 7 subcommands.

Other verification checks were performed by repository inspection:

- `rg --files -g '!.git'`
- search for package manifests
- search for environment variable access patterns
- search for API route or server patterns
- search for test files
- search for CI and deployment files
- search for licence files

Notebook validation, repair, clean, export, diff, and execution commands were not run against a real notebook because the repository does not contain a notebook file.

Test coverage percentage:

```text
Not measured in the current repository.
```

## Code Quality Checks

The repository contains this Prettier configuration:

```json
{
	"useTabs": true,
	"tabWidth": 2
}
```

`.prettierignore` excludes the seven third-party skill folders and the local `.agent-local/`, `.venv/`, and `.cache/` folders. Check formatting with a repository local npm cache:

```powershell
$env:npm_config_cache = "$PWD\.cache\npm"
npx --yes prettier@3 --check "**/*.{md,json,yaml}"
```

Result when this README was updated: all matched files use Prettier code style.

Check the third-party design data with the bundled validator:

```powershell
python .\ui-ux-design-reference\scripts\validate_data.py
```

Result when this README was updated: `OK: validated 12 domain files, 22 stack files, and ui-reasoning.csv`.

No formatter script, lint script, type check script, precommit configuration file, or automated test command is declared at the repository root.

## Build, Deployment, And CI

There is no build process. The repository contains Markdown, YAML, CSV and JSON data, fonts, and Python and Node.js helper scripts.

The repository does not contain:

- API server code
- database schema or migrations
- Dockerfile
- Docker Compose file
- deployment configuration
- `.github` workflow files
- package build script
- hosting configuration

## Repository Metrics

| Metric name                       | Verified value                          | Source file or command used for verification                                                 | Notes                                                                            |
| --------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Git work tree                     | Yes                                     | `git rev-parse --is-inside-work-tree`                                                        | Returned `true`.                                                                 |
| Top level skill directories       | 14                                      | `Get-ChildItem -Force -Directory` filtered to exclude `.git`                                 | Counts current working tree folders.                                             |
| Skill definition files            | 14                                      | `rg --files -g '!.git' -g 'SKILL.md'`                                                        | Files named `SKILL.md`.                                                          |
| Agent metadata files              | 14                                      | `rg --files -g '!.git'` filtered for `agents\openai.yaml`                                    | One metadata file per skill.                                                     |
| Repository files outside `.git`   | 274                                     | `rg --files -g '!.git'`                                                                      | 255 are in the seven third-party skills, mostly data, fonts, and references.     |
| Markdown files                    | 70                                      | `rg --files -g '!.git' -g '*.md'`                                                            | Includes this README and all skill Markdown files.                               |
| YAML files                        | 14                                      | `rg --files -g '!.git' -g '*.yaml'`                                                          | Agent metadata files only.                                                       |
| Python scripts                    | 36                                      | `git ls-files -co --exclude-standard` filtered for `.py`                                     | Includes 14 test modules.                                                        |
| Node.js scripts                   | 7                                       | `git ls-files -co --exclude-standard` filtered for `.cjs`                                    | In `brand-guidelines/scripts/` and `design-system/scripts/`.                     |
| Notebook helper subcommands       | 7                                       | `python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py --help`                        | `inspect`, `validate`, `repair`, `clean`, `export-code`, `check-kaggle`, `diff`. |
| Package manifests                 | 0                                       | Search for `package.json`, `pyproject.toml`, `requirements.txt`, setup files, and lock files | No package manager metadata found.                                               |
| API endpoints                     | 0                                       | Search for common route and server patterns                                                  | No API server code found.                                                        |
| Environment variables             | 5                                       | Search for common environment access patterns                                                | All optional and in third-party skills. See Environment Configuration.           |
| Database models                   | 0                                       | Repository file inspection                                                                   | No database files found.                                                         |
| Test files                        | 14                                      | `git ls-files -co --exclude-standard` filtered for `test_*.py`                               | All in the third-party skills. 226 tests passed.                                 |
| CI or deployment files            | 0                                       | Search for common CI, Docker, compose, and hosting files                                     | No deployment pipeline found.                                                    |
| Default ports                     | 0                                       | Repository file inspection                                                                   | No server or port configuration found.                                           |
| Notebook output warning threshold | 5 MiB                                   | `kaggle-jupyter-notebooks/scripts/notebook_doctor.py`                                        | Used by the `inspect` command.                                                   |
| Test coverage percentage          | Not measured in the current repository. | No coverage report found                                                                     | Coverage cannot be verified.                                                     |

## Security Notes

- No secrets, tokens, passwords, private keys, or connection strings were found during README inspection.
- No environment variables are required. The optional API keys for `graphic-design` image generation are secrets and send prompts to external services when set.
- Notebook outputs can contain sensitive data. The notebook skill instructs users to check for secrets and machine specific paths before finalising notebook work.
- `notebook_doctor.py` can create backups when `--backup` is passed to `repair` or `clean`. Inside a Git repository they go to `.agent-local/backups/`.
- `notebook_doctor.py` is not a secret scanner. Review notebooks manually before sharing them.

## Maintenance Notes

- Keep each skill in its own top level folder.
- Keep each main skill instruction file named `SKILL.md`.
- Keep each agent metadata file at `agents/openai.yaml`.
- Update this README when adding, renaming, or removing a skill.
- Update the matching `agents/openai.yaml` when a skill name, description, default prompt, or invocation policy changes.
- Add a dependency manifest if more Python dependencies are introduced.
- Add tests if `notebook_doctor.py` gains more behaviour.
- Do not commit local folders such as `.venv`, `.cache`, or `.agent-local`.

## Troubleshooting

| Problem                                                               | Likely cause                                                                | Diagnostic command                                                                             | Resolution                                                                                                               |
| --------------------------------------------------------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `python` is not recognised.                                           | Python is not installed or not on `PATH`.                                   | `python --version`                                                                             | Install Python 3 or use the Python launcher available on the machine.                                                    |
| `notebook_doctor.py` reports missing `nbformat`.                      | The active Python environment does not have `nbformat`.                     | `python -m pip show nbformat`                                                                  | Install `nbformat` in a repository local virtual environment.                                                            |
| The notebook path is not found.                                       | The command uses a placeholder path or the shell is in the wrong directory. | `Get-Location`                                                                                 | Run the command from the repository root or pass the correct notebook path.                                              |
| A notebook is reported as invalid.                                    | The file has invalid JSON, invalid notebook schema, or duplicate cell IDs.  | `python .\kaggle-jupyter-notebooks\scripts\notebook_doctor.py validate path\to\notebook.ipynb` | Inspect the error. If structure repair is appropriate, run `repair` with `--backup`.                                     |
| New `.venv` or `.cache` folders appear after dependency installation. | Local dependency setup was run.                                             | `git status --short`                                                                           | Keep those folders local and do not commit them unless the repository intentionally adds tooling configuration for them. |

## Known Limitations

- There is no root package manifest.
- Dependency versions are not pinned.
- The exact supported Python version is not declared.
- There is no automated test suite for the first-party skills.
- There is no coverage report.
- There is no lint, type check, or format script.
- There is no CI or CD setup.
- There is no deployment configuration.
- There is no API service or database layer.
- Third-party skills are copies. Upstream updates must be merged manually, and the local changes listed under Licence must be reapplied.
- `notebook_doctor.py` has no automated tests.

## Contribution Guidelines

No formal contributing guide is present.

Use these repository rules for changes:

- Make small, focused edits.
- Preserve each skill folder as a self contained unit.
- Update `SKILL.md` and `agents/openai.yaml` together when skill behaviour changes.
- Update this README when repository structure or commands change.
- Use repository local tooling and caches for task specific dependencies.
- Do not commit secrets, notebook outputs with private data, local virtual environments, or machine specific paths.

## Licence

No repository level licence file is present. Licence terms for the repository as a whole cannot be verified from the current files.

Seven skills are third-party code from [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill): `banner-design`, `brand-guidelines`, `graphic-design`, `design-system`, `html-presentations`, `shadcn-tailwind-ui`, and `ui-ux-design-reference`.

- Six are under the upstream MIT licence. A copy is kept in each folder as `LICENSE`.
- `shadcn-tailwind-ui` ships its own Apache 2.0 licence as `shadcn-tailwind-ui/LICENSE.txt`. Its `canvas-fonts/` folder includes an OFL licence file for each font family.

They were copied from upstream commit `dcc40ff` (version 2.13.0, 21 September 2026), folder `.claude/skills/`, with these local changes:

- `ui-ux-design-reference/SKILL.md` script commands use `<skill-dir>/scripts/search.py` instead of the Claude Code plugin path `${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py`.
- Harness-specific wording was made neutral: references to the `AskUserQuestion` tool now say to ask the user, subagent use is conditional on harness support, the note about Claude Code reporting the skill base directory now refers to agent harnesses in general, and the `/slides:create` and `/brand:update` slash command examples were replaced with plain requests.
- The `design-system` reference to an upstream example file that is not shipped (`assets/designs/slides/claudekit-pitch-251223.html`) was removed.
- Four `ui-ux-design-reference` test modules and their fixtures were removed because they test the upstream repository layout: `test_catalog_refresh.py`, `test_catalog_summary_line_endings.py`, `test_relevance_evaluator.py`, and `test_skill_script_paths.py`.
- The committed coverage database `shadcn-tailwind-ui/scripts/.coverage` was not copied.
- `LICENSE` files (except in `shadcn-tailwind-ui`) and `agents/openai.yaml` files were added.
- Five skills were renamed from their upstream names so the names describe their content: `brand` to `brand-guidelines`, `design` to `graphic-design`, `slides` to `html-presentations`, `ui-styling` to `shadcn-tailwind-ui`, and `ui-ux-pro-max` to `ui-ux-design-reference`. References between the skills were updated to match. `banner-design` and `design-system` keep their upstream names.

Other upstream folders, such as the `cli/` installer, `src/` templates, `docs/`, `gallery/`, `preview/`, and `screenshots/`, are upstream project tooling and marketing material, not skills, and were not copied.

The skills refer to each other with relative paths such as `../design-system/scripts/generate-tokens.cjs`, so keep them as sibling folders when copying them elsewhere.

## Support

No support contact, issue tracker, maintainer email, or project URL is present in the repository.
