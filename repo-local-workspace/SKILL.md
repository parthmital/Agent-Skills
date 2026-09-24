---
name: repo-local-workspace
description: "Keep everything a task creates or needs inside the target repository: dependencies, virtual environments, caches, browser binaries, helper scripts, logs, outputs, downloads, and temporary files, stored in an organised, Git-ignored folder so nothing touches system folders and past scripts can be reused. Use automatically before installing packages, running package managers or Python helpers, writing helper scripts, saving logs or outputs, downloading tools, using Playwright or browser tooling, converting documents, cloning reference code, or any step that could write outside the repository."
---

# Repo Local Workspace

Use this skill to keep the machine clean and keep all task work in one place. Everything a task creates or needs must live inside the target repository or workspace: tools, dependencies, helper scripts, caches, downloads, logs, outputs, and temporary files. Nothing goes into global Python, global Node, the user home directory, OS temp folders, system package stores, or shared machine caches.

This local work area is never committed, but it is kept between tasks so earlier scripts, logs, and outputs can be found and reused.

If a tool cannot be made repo-local, ask before using it and state what global path or system state it would touch.

If the harness offers its own scratch or temp directory outside the repository, do not use it. Use `.agent-local/` instead unless the user explicitly says otherwise.

## Core Rule

Before running helper code or installing anything:

1. Identify the target repo or workspace root.
2. Reuse an existing repo-local environment if it exists.
3. If none exists, create a local environment inside that repo.
4. Before writing a new helper script, check `.agent-local/scripts/` and its index for an existing script that does the job. Reuse or extend it instead of creating a near-duplicate.
5. Put helper scripts, logs, caches, outputs, downloads, and temporary files under repo-local paths.
6. Use tool commands with repo-local cache, install, and temp locations.
7. Keep the local work area organised so it stays useful for later tasks.

Never use:

- Global package installs such as `pip install` outside a venv, `pip install --user`, `npm install -g`, `yarn global`, `pnpm add -g`, `pipx install`, `uv tool install`, `gem install`, or system package managers.
- Commands that write user-level or system-level configuration, such as `npm config set`, `pnpm config set`, `git config --global`, or `pip config set`, unless the setting is scoped to the project, for example `npm config set --location project`.
- User-home caches such as default pip, npm, pnpm, Playwright, Maven, Gradle, Go, Cargo, NuGet, or browser caches when a local override is available.
- Random scripts in the user profile, OS temp folders, desktop, downloads folder, or global tool directories.

## Local Layout

Prefer these repo-local paths:

```text
repo/
  .venv/                 Python virtual environment
  .agent-local/
    README.md            index of scripts and what they do
    scripts/             helper scripts, kept for reuse
    logs/                command and script logs
    tmp/                 temporary intermediate files
    output/              generated analysis output
    downloads/           task-specific downloads
    vendor/              cloned reference repositories
    backups/             copies made before risky edits
  .cache/
    pip/
    uv/
    npm/
    pnpm/
    yarn/
    playwright/
    maven/
    gradle/
    go-build/
    go-mod/
    cargo/
    nuget/
    huggingface/
```

If these folders are created in a Git repo and are not already ignored, add them to `.git/info/exclude` so they stay untracked without modifying a tracked file. Edit `.gitignore` instead only when the user wants the rule shared with the team.

```gitignore
.venv/
.agent-local/
.cache/
```

Do not ignore source files, fixtures, required assets, lockfiles, or project configuration.

## Scripts, Logs, And Outputs

- Give helper scripts descriptive names such as `extract_pdf_tables.py`, not `script.py`, `test2.py`, or `tmp.py`.
- Start each script with a short header comment stating its purpose, inputs, outputs, and the exact command to run it.
- Make scripts take paths and options as arguments instead of hardcoding one-off values, so they can be rerun later.
- Keep `.agent-local/README.md` as a one-line-per-script index. Update it whenever a script is added, renamed, or removed.
- Write command and script logs to `.agent-local/logs/`, named by date and purpose, for example `2026-09-25_pdf-extract.log`.
- Write generated results to `.agent-local/output/<task-name>/` so outputs from different tasks do not mix.
- Point temp directories at the repo for spawned tools: set `TMPDIR`, `TMP`, and `TEMP` to the absolute path of `.agent-local/tmp` when running commands that create temp files.
- Do not store secrets, tokens, or credentials in scripts, logs, or outputs.

## Python

Use the repo-local Python environment for any Python work, including one-off PDF extraction, document parsing, data conversion, code generation, validation scripts, or analysis.

Windows pattern:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip --cache-dir .cache\pip
.\.venv\Scripts\python -m pip install <package> --cache-dir .cache\pip
.\.venv\Scripts\python .agent-local\scripts\task.py
```

POSIX pattern:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip --cache-dir .cache/pip
./.venv/bin/python -m pip install <package> --cache-dir .cache/pip
./.venv/bin/python .agent-local/scripts/task.py
```

Rules:

- Use an existing `.venv`, `venv`, or project-managed environment if it is already repo-local and healthy.
- Do not install into the system interpreter.
- Do not use `--user`.
- Keep helper scripts under `.agent-local/scripts/` unless they are durable project code.
- Keep extracted text, converted files, and intermediate outputs under `.agent-local/output/` or a user-requested repo path.
- If dependencies are already declared in `pyproject.toml`, `requirements.txt`, `uv.lock`, `Pipfile`, or `poetry.lock`, follow the repo's toolchain while keeping environment and cache paths local.
- Set `PIP_CACHE_DIR=.cache/pip` for commands that invoke pip indirectly. For uv, set `UV_CACHE_DIR=.cache/uv`. For Poetry, set `POETRY_VIRTUALENVS_IN_PROJECT=true` and `POETRY_CACHE_DIR=.cache/poetry`.
- For Hugging Face models and datasets, set `HF_HOME=.cache/huggingface`.

## JavaScript And Frontend Tooling

Use project-local package managers and binaries.

Rules:

- Use existing `node_modules/.bin`, package scripts, or package-manager exec commands.
- Do not install global Node packages.
- Keep npm cache local with `npm_config_cache=.cache/npm`.
- Keep pnpm store local with `pnpm install --store-dir .cache/pnpm` or `store-dir=.cache/pnpm` in the project `.npmrc`. Do not use a bare `pnpm config set`, which writes to user-level configuration.
- `npx` and `npm exec` share the npm cache, so `npm_config_cache` also keeps their downloads local.
- Keep Yarn cache local with repo-local Yarn configuration where the project supports it.
- Prefer adding a dev dependency to the repo over using a global CLI when the tool is needed repeatedly.
- For one-off execution, prefer package-manager commands that can use local cache paths and do not alter global state.

Examples:

```powershell
$env:npm_config_cache = ".cache\npm"
npm install
npm run test
```

```bash
npm_config_cache=.cache/npm npm install
npm_config_cache=.cache/npm npm run test
```

## Browser And Playwright Tooling

Browser automation often downloads binaries to user-level caches by default. Keep them repo-local.

Use:

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH = ".cache\playwright"
```

```bash
PLAYWRIGHT_BROWSERS_PATH=.cache/playwright
```

Rules:

- Prefer the repo's existing Playwright setup.
- If installing Playwright browsers, set `PLAYWRIGHT_BROWSERS_PATH` first.
- Use disposable browser profiles under `.agent-local/tmp/`.
- Do not attach to a personal browser profile.

## Other Ecosystems

Use repo-local caches and install paths where possible:

- Maven: `-Dmaven.repo.local=.cache/maven`
- Gradle: `GRADLE_USER_HOME=.cache/gradle`
- Go: `GOCACHE=.cache/go-build` and `GOMODCACHE=.cache/go-mod`
- Rust: `CARGO_HOME=.cache/cargo` for task-specific commands when compatible
- .NET: `NUGET_PACKAGES=.cache/nuget`
- Ruby: `bundle config set path vendor/bundle`

If the ecosystem requires a global SDK or system package that is not already installed, ask before installing it.

## Downloads And External Repos

Keep downloads local:

- Put downloaded files under `.agent-local/downloads/`.
- Put cloned reference repositories under `.agent-local/vendor/` unless the clone is intended to be part of the project.
- Record source URLs in a short note or script comment when the downloaded material affects reproducibility.
- Keep downloads that may be needed again. Delete only large files that can be downloaded again easily and are clearly no longer needed.

## Cleanup

Before finishing a task:

- Keep helper scripts, logs, and outputs in `.agent-local/` for later reuse. Do not delete them just because the current task is done.
- Delete only clearly disposable files in `.agent-local/tmp/`, and superseded copies of the same output.
- Update the `.agent-local/README.md` index.
- Make sure `.venv/`, `.cache/`, and `.agent-local/` are ignored by Git and are not staged or committed.
- Report which scripts, logs, and outputs were created or updated.

## Final Check

Confirm:

- No global install commands were used.
- No user-home or system cache was intentionally written when a repo-local alternative existed.
- All helper scripts, logs, outputs, and temporary artifacts are inside the repo, in `.agent-local/`.
- Nothing was written to OS temp folders, the user profile, or harness scratch directories outside the repo.
- Dependency and browser caches are repo-local where supported.
- Any unavoidable global effect was explicitly authorised or clearly reported.
