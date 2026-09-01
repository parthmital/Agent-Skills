# Codex Skills

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

This repository stores local Codex skills. It is not a web application, API service, Python package, or Node package.

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

Expected result: the command shows 8 skill folders, including `readme-generator` and `jupyter-notebook-guardian`.

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
python .\jupyter-notebook-guardian\scripts\notebook_doctor.py --help
```

What it does: runs the notebook helper in help mode and avoids creating `__pycache__` files.

Expected result: the command prints usage text and these subcommands: `inspect`, `validate`, `repair`, `clean`, `export-code`, and `diff`.

Common errors:

| Problem                                                            | Likely cause                                                  | Resolution                                                                                                         |
| ------------------------------------------------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `python` is not recognised.                                        | Python is not installed or not on `PATH`.                     | Install Python 3 or use the Python launcher available on the machine.                                              |
| Missing dependency: install with `python -m pip install nbformat`. | `nbformat` is not installed in the active Python environment. | Install `nbformat` in a local virtual environment as shown in [Dependency Installation](#dependency-installation). |
| The script path is not found.                                      | The command was not run from the repository root.             | Change to the repository root and run the command again.                                                           |

## Project Overview

This repository contains reusable Codex skills. A skill is a folder with a `SKILL.md` file that explains when and how Codex should handle a class of tasks.

Each skill in this repository also includes an `agents/openai.yaml` metadata file. That file provides:

- `display_name`
- `short_description`
- `default_prompt`
- `allow_implicit_invocation`

One skill, `jupyter-notebook-guardian`, also includes a Python helper script for safe notebook inspection, validation, repair, cleaning, export, and semantic diff.

## Skills In This Repository

| Skill                       | Purpose                                                                                                               | Main files                                                                                                                                                                             |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `codebase-architecture`     | Reviews, plans, hardens, cleans up, deduplicates, and documents codebase structure.                                   | [codebase-architecture/SKILL.md](codebase-architecture/SKILL.md), [codebase-architecture/agents/openai.yaml](codebase-architecture/agents/openai.yaml)                                 |
| `detailed-git-commit`       | Creates factual Git commits with inspected changes and strict commit message formatting.                              | [detailed-git-commit/SKILL.md](detailed-git-commit/SKILL.md), [detailed-git-commit/agents/openai.yaml](detailed-git-commit/agents/openai.yaml)                                         |
| `frontend-design`           | Guides clean, functional frontend UI and UX work with custom accessible components.                                   | [frontend-design/SKILL.md](frontend-design/SKILL.md), [frontend-design/agents/openai.yaml](frontend-design/agents/openai.yaml)                                                         |
| `internet-research`         | Guides current, source based research, comparison, validation, and recommendation work.                               | [internet-research/SKILL.md](internet-research/SKILL.md), [internet-research/agents/openai.yaml](internet-research/agents/openai.yaml)                                                 |
| `jupyter-notebook-guardian` | Protects Jupyter notebook edits from JSON corruption, hidden state, noisy diffs, and execution order errors.          | [jupyter-notebook-guardian/SKILL.md](jupyter-notebook-guardian/SKILL.md), [jupyter-notebook-guardian/scripts/notebook_doctor.py](jupyter-notebook-guardian/scripts/notebook_doctor.py) |
| `readme-generator`          | Generates or updates a verified repository README from inspected repository facts.                                    | [readme-generator/SKILL.md](readme-generator/SKILL.md), [readme-generator/agents/openai.yaml](readme-generator/agents/openai.yaml)                                                     |
| `repo-local-tooling`        | Keeps task tools, dependency caches, helper scripts, downloads, and generated artifacts inside the target repository. | [repo-local-tooling/SKILL.md](repo-local-tooling/SKILL.md), [repo-local-tooling/agents/openai.yaml](repo-local-tooling/agents/openai.yaml)                                             |
| `test-local-app-end-to-end` | Guides local web application testing with Playwright, disposable browser sessions, logs, and retesting.               | [test-local-app-end-to-end/SKILL.md](test-local-app-end-to-end/SKILL.md), [test-local-app-end-to-end/agents/openai.yaml](test-local-app-end-to-end/agents/openai.yaml)                 |

## Repository Structure

```text
.
|-- .gitattributes
|-- .prettierrc.json
|-- README.md
|-- codebase-architecture/
|   |-- SKILL.md
|   `-- agents/
|       `-- openai.yaml
|-- detailed-git-commit/
|   |-- SKILL.md
|   `-- agents/
|       `-- openai.yaml
|-- frontend-design/
|   |-- SKILL.md
|   `-- agents/
|       `-- openai.yaml
|-- internet-research/
|   |-- SKILL.md
|   `-- agents/
|       `-- openai.yaml
|-- jupyter-notebook-guardian/
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
|-- repo-local-tooling/
|   |-- SKILL.md
|   `-- agents/
|       `-- openai.yaml
`-- test-local-app-end-to-end/
    |-- SKILL.md
    `-- agents/
        `-- openai.yaml
```

Important paths:

- `.gitattributes`: enables automatic text file normalisation through Git.
- `.prettierrc.json`: stores formatter preferences for tabs and tab width.
- `*/SKILL.md`: stores the main instructions for each skill.
- `*/agents/openai.yaml`: stores display and invocation metadata for each skill.
- `jupyter-notebook-guardian/README.md`: gives short setup notes for the notebook skill.
- `jupyter-notebook-guardian/references/precommit.md`: documents optional notebook Git protection commands.
- `jupyter-notebook-guardian/scripts/notebook_doctor.py`: provides the notebook maintenance command line tool.

## Technology Stack

| Technology             | Version                       | Purpose                                                       | Where used                                              | Notes                                                      |
| ---------------------- | ----------------------------- | ------------------------------------------------------------- | ------------------------------------------------------- | ---------------------------------------------------------- |
| Markdown               | Not declared                  | Stores skill instructions and documentation.                  | `README.md`, `SKILL.md`, and reference files.           | Codex reads skill behaviour from Markdown files.           |
| YAML                   | Not declared                  | Stores skill metadata.                                        | `agents/openai.yaml` files.                             | Each metadata file enables implicit invocation.            |
| Python                 | Exact version not declared    | Runs the notebook helper script.                              | `jupyter-notebook-guardian/scripts/notebook_doctor.py`. | The script uses Python 3 syntax and a Python 3 shebang.    |
| `nbformat`             | Exact version not declared    | Reads, writes, converts, normalises, and validates notebooks. | Imported by `notebook_doctor.py`.                       | The script exits with an install message if it is missing. |
| Git                    | Exact version not declared    | Tracks repository changes and applies `.gitattributes`.       | `.git`, `.gitattributes`.                               | The current folder is a Git work tree.                     |
| Prettier configuration | Prettier version not declared | Defines formatting preferences.                               | `.prettierrc.json`.                                     | The file sets `useTabs` to `true` and `tabWidth` to `2`.   |

No root package manager manifest is present. There is no `package.json`, `pyproject.toml`, `requirements.txt`, lock file, or setup file.

## Prerequisites

| Prerequisite                        | Required for                            | Version                         | Verification                                                                                           |
| ----------------------------------- | --------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Codex skills compatible environment | Using these folders as Codex skills.    | Not declared in the repository. | The repository contains skill folders with `SKILL.md`.                                                 |
| Git                                 | Repository maintenance.                 | Not declared in the repository. | `git rev-parse --is-inside-work-tree` returns `true`.                                                  |
| Python 3                            | Running `notebook_doctor.py`.           | Exact version not declared.     | The script has a Python 3 shebang and uses Python 3 syntax.                                            |
| `nbformat`                          | Notebook helper commands.               | Exact version not declared.     | The script imports `nbformat` and the help command runs when it is installed.                          |
| Jupyter `nbconvert`                 | Fresh kernel notebook execution checks. | Not declared in the repository. | The command is documented in `jupyter-notebook-guardian/SKILL.md`, but no dependency file declares it. |

## Local Installation

There is no repository level install script.

To use a skill locally:

1. Keep this repository in a stable folder.
2. Copy the required skill folder into your Codex skills directory.
3. Preserve the folder name.
4. Preserve the `SKILL.md` file.
5. Preserve any supporting files in that skill folder, such as `scripts/`, `references/`, and `agents/`.

The repository does not declare the exact Codex skills directory path because that depends on the local Codex setup.

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

Expected result: `.\.venv\Scripts\python .\jupyter-notebook-guardian\scripts\notebook_doctor.py --help` prints the notebook helper usage text.

These dependency setup commands were not executed while preparing this README because they create local environment and cache folders. The notebook helper itself was smoke tested with the current Python environment.

Optional notebook repository protection tools are documented in [jupyter-notebook-guardian/references/precommit.md](jupyter-notebook-guardian/references/precommit.md):

```powershell
python -m pip install nbformat nbstripout nbdime
nbdime config-git --enable
nbstripout --install
```

Those optional commands modify local Python or Git configuration depending on the active environment. They were not executed while preparing this README.

## Running Commands

There is no long running application to start.

Useful repository commands:

| Command                                                                | Purpose                               | Expected result                                                          |
| ---------------------------------------------------------------------- | ------------------------------------- | ------------------------------------------------------------------------ |
| `rg --files -g '!.git'`                                                | List repository files outside `.git`. | Prints 20 tracked or working tree files in the current repository state. |
| `Get-ChildItem -Directory                                              | Where-Object { $_.Name -ne ".git" }`  | List skill folders.                                                      | Prints 8 skill folders. |
| `Get-Content .\readme-generator\SKILL.md`                              | Read the README generator skill.      | Prints the selected skill instructions.                                  |
| `python .\jupyter-notebook-guardian\scripts\notebook_doctor.py --help` | Run the notebook helper help command. | Prints usage text and 6 subcommands.                                     |

## Notebook Utility

The notebook helper is [jupyter-notebook-guardian/scripts/notebook_doctor.py](jupyter-notebook-guardian/scripts/notebook_doctor.py).

Available subcommands:

| Subcommand    | Purpose                                                                                                   |
| ------------- | --------------------------------------------------------------------------------------------------------- |
| `inspect`     | Prints notebook metadata, cell counts, output size, cell ID health, execution count health, and warnings. |
| `validate`    | Validates notebook structure through `nbformat` and checks duplicate cell IDs.                            |
| `repair`      | Converts the notebook to format 4, normalises it, and repairs missing or duplicate cell IDs.              |
| `clean`       | Clears code cell outputs and execution counts, with optional widget metadata removal.                     |
| `export-code` | Exports code cells to a Python file with cell index and cell ID markers.                                  |
| `diff`        | Prints a semantic diff between two notebooks based on cell source, type, outputs, and execution counts.   |

Examples:

```powershell
python .\jupyter-notebook-guardian\scripts\notebook_doctor.py inspect path\to\notebook.ipynb
python .\jupyter-notebook-guardian\scripts\notebook_doctor.py validate path\to\notebook.ipynb
python .\jupyter-notebook-guardian\scripts\notebook_doctor.py repair path\to\notebook.ipynb --backup
python .\jupyter-notebook-guardian\scripts\notebook_doctor.py clean path\to\notebook.ipynb --backup
python .\jupyter-notebook-guardian\scripts\notebook_doctor.py clean path\to\notebook.ipynb --backup --drop-widgets
python .\jupyter-notebook-guardian\scripts\notebook_doctor.py export-code path\to\notebook.ipynb --output path\to\notebook_cells.py
python .\jupyter-notebook-guardian\scripts\notebook_doctor.py diff before.ipynb after.ipynb
```

The notebook skill also documents this fresh kernel execution check:

```bash
jupyter nbconvert \
  --to notebook \
  --execute notebook.ipynb \
  --output notebook.executed.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3
```

This command was not executed while preparing this README because the repository does not contain a notebook file and does not declare Jupyter as a dependency.

## Environment Configuration

No environment variables are read by the current repository files.

| Variable name | Required | Purpose        | Expected format | Safe example value | Default value  | Security notes                                   |
| ------------- | -------- | -------------- | --------------- | ------------------ | -------------- | ------------------------------------------------ |
| None found    | No       | Not applicable | Not applicable  | Not applicable     | Not applicable | No secret values are required by the repository. |

## Input Validation And Error Handling

The repository contains input validation and error handling in `jupyter-notebook-guardian/scripts/notebook_doctor.py`.

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

No automated test files are present.

Verification run while preparing this README:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python .\jupyter-notebook-guardian\scripts\notebook_doctor.py --help
```

Result: passed. The command printed usage text and listed 6 subcommands.

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

The repository also contains `.gitattributes`:

```text
# Auto detect text files and perform LF normalization
* text=auto
```

No formatter script, lint script, type check script, precommit configuration file, or automated test command is declared at the repository root.

## Build, Deployment, And CI

There is no build process. The repository contains Markdown, YAML, and one Python helper script.

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

| Metric name                           | Verified value                          | Source file or command used for verification                                                 | Notes                                                                             |
| ------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Git work tree                         | Yes                                     | `git rev-parse --is-inside-work-tree`                                                        | Returned `true`.                                                                  |
| Top level skill directories           | 8                                       | `Get-ChildItem -Force -Directory` filtered to exclude `.git`                                 | Counts current working tree folders.                                              |
| Skill definition files                | 8                                       | `rg --files -g '!.git' -g 'SKILL.md'`                                                        | Files named `SKILL.md`.                                                           |
| Agent metadata files                  | 8                                       | `rg --files -g '!.git'` filtered for `agents\openai.yaml`                                    | One metadata file per skill.                                                      |
| Repository files outside `.git`       | 20                                      | `rg --files -g '!.git'`                                                                      | Includes root files, skill docs, metadata, reference docs, and the Python script. |
| Markdown files                        | 11                                      | `rg --files -g '!.git'` filtered for `.md`                                                   | Includes this README and all skill Markdown files.                                |
| YAML files                            | 8                                       | `rg --files -g '!.git'` filtered for `.yaml`                                                 | Agent metadata files only.                                                        |
| Python scripts                        | 1                                       | `rg --files -g '!.git'` filtered for `.py`                                                   | `notebook_doctor.py`.                                                             |
| Notebook helper subcommands           | 6                                       | `python .\jupyter-notebook-guardian\scripts\notebook_doctor.py --help`                       | `inspect`, `validate`, `repair`, `clean`, `export-code`, and `diff`.              |
| Package manifests                     | 0                                       | Search for `package.json`, `pyproject.toml`, `requirements.txt`, setup files, and lock files | No package manager metadata found.                                                |
| API endpoints                         | 0                                       | Search for common route and server patterns                                                  | No API server code found.                                                         |
| Environment variables                 | 0                                       | Search for common environment access patterns                                                | No environment reads found.                                                       |
| Database models                       | 0                                       | Repository file inspection                                                                   | No database files found.                                                          |
| Test files                            | 0                                       | Search for `*test*`, `*.spec.*`, and `*.test.*`                                              | No automated tests found.                                                         |
| CI or deployment files                | 0                                       | Search for common CI, Docker, compose, and hosting files                                     | No deployment pipeline found.                                                     |
| Default ports                         | 0                                       | Repository file inspection                                                                   | No server or port configuration found.                                            |
| Notebook output warning threshold     | 5 MiB                                   | `jupyter-notebook-guardian/scripts/notebook_doctor.py`                                       | Used by the `inspect` command.                                                    |
| Documented notebook execution timeout | 600 seconds                             | `jupyter-notebook-guardian/SKILL.md`                                                         | Used in the documented `jupyter nbconvert` command.                               |
| Test coverage percentage              | Not measured in the current repository. | No coverage report found                                                                     | Coverage cannot be verified.                                                      |

## Security Notes

- No secrets, tokens, passwords, private keys, or connection strings were found during README inspection.
- No environment variables are required by repository code.
- Notebook outputs can contain sensitive data. The notebook skill instructs users to check for secrets and machine specific paths before finalising notebook work.
- `notebook_doctor.py` can create backups when `--backup` is passed to `repair` or `clean`.
- `notebook_doctor.py` is not a secret scanner. Review notebooks manually before sharing them.

## Maintenance Notes

- Keep each skill in its own top level folder.
- Keep each main skill instruction file named `SKILL.md`.
- Keep each agent metadata file at `agents/openai.yaml`.
- Update this README when adding, renaming, or removing a skill.
- Update the matching `agents/openai.yaml` when a skill name, description, default prompt, or invocation policy changes.
- Add a dependency manifest if more Python dependencies are introduced.
- Add tests if `notebook_doctor.py` gains more behaviour.
- Do not commit local dependency folders such as `.venv` or `.cache`.

## Troubleshooting

| Problem                                                               | Likely cause                                                                | Diagnostic command                                                                              | Resolution                                                                                                               |
| --------------------------------------------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `python` is not recognised.                                           | Python is not installed or not on `PATH`.                                   | `python --version`                                                                              | Install Python 3 or use the Python launcher available on the machine.                                                    |
| `notebook_doctor.py` reports missing `nbformat`.                      | The active Python environment does not have `nbformat`.                     | `python -m pip show nbformat`                                                                   | Install `nbformat` in a repository local virtual environment.                                                            |
| The notebook path is not found.                                       | The command uses a placeholder path or the shell is in the wrong directory. | `Get-Location`                                                                                  | Run the command from the repository root or pass the correct notebook path.                                              |
| A notebook is reported as invalid.                                    | The file has invalid JSON, invalid notebook schema, or duplicate cell IDs.  | `python .\jupyter-notebook-guardian\scripts\notebook_doctor.py validate path\to\notebook.ipynb` | Inspect the error. If structure repair is appropriate, run `repair` with `--backup`.                                     |
| `jupyter nbconvert` is unavailable.                                   | Jupyter is not installed in the active Python environment.                  | `python -m pip show jupyter nbconvert`                                                          | Install the required Jupyter tools in a local virtual environment before running execution checks.                       |
| New `.venv` or `.cache` folders appear after dependency installation. | Local dependency setup was run.                                             | `git status --short`                                                                            | Keep those folders local and do not commit them unless the repository intentionally adds tooling configuration for them. |

## Known Limitations

- There is no root package manifest.
- Dependency versions are not pinned.
- The exact supported Python version is not declared.
- There is no automated test suite.
- There is no coverage report.
- There is no lint, type check, or format script.
- There is no CI or CD setup.
- There is no deployment configuration.
- There is no API service or database layer.
- There is no repository level `.gitignore` for local virtual environments or caches.
- `jupyter-notebook-guardian` is the only skill with an executable helper script.

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

No repository level licence file is present. Licence terms cannot be verified from the current files.

## Support

No support contact, issue tracker, maintainer email, or project URL is present in the repository.
