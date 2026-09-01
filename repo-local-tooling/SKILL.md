---
name: repo-local-tooling
description: "Keep all task tooling, dependencies, helper scripts, caches, downloads, generated files, virtual environments, package stores, browser binaries, analysis artifacts, and temporary work local to the target repository or workspace. Use automatically before running Python helpers, installing packages, downloading tools, extracting or converting files, processing PDFs or documents, running package managers, using Playwright or browser tooling, creating scripts, cloning reference code, generating build artifacts, or any coding task that could write to global locations, user home caches, system package stores, or shared machine state. Avoid global installs, user-level installs, global caches, and system-wide changes unless the user explicitly authorises them."
---

# Repo Local Tooling

Use this skill to keep the machine clean. All task-specific tools, dependencies, scripts, caches, downloads, and generated artifacts must live inside the target repository or workspace, not in global Python, global Node, the user home directory, system package stores, or shared machine caches.

If a tool cannot be made repo-local, ask before using it and state what global path or system state it would touch.

## Core Rule

Before running helper code or installing anything:

1. Identify the target repo or workspace root.
2. Reuse an existing repo-local environment if it exists.
3. If none exists, create a local environment inside that repo.
4. Put helper scripts, caches, outputs, downloads, and temporary files under repo-local paths.
5. Use tool commands with repo-local cache and install locations.
6. Clean up temporary artifacts when they are no longer useful.

Never use:

- Global package installs such as `pip install` outside a venv, `pip install --user`, `npm install -g`, `yarn global`, `pnpm add -g`, `pipx install`, `gem install`, or system package managers.
- User-home caches such as default pip, npm, pnpm, Playwright, Maven, Gradle, Go, Cargo, NuGet, or browser caches when a local override is available.
- Random scripts in the user profile, OS temp folders, desktop, downloads folder, or global tool directories.

## Local Layout

Prefer these repo-local paths:

```text
repo/
  .venv/                 Python virtual environment
  .codex-local/
    scripts/             one-off helper scripts
    tmp/                 temporary intermediate files
    output/              generated analysis output
    downloads/           task-specific downloads
  .cache/
    pip/
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
```

If these folders are created in a Git repo, add local-only generated paths to `.gitignore` unless the user explicitly wants them tracked:

```gitignore
.venv/
.codex-local/
.cache/
```

Do not ignore source files, fixtures, required assets, lockfiles, or project configuration.

## Python

Use the repo-local Python environment for any Python work, including one-off PDF extraction, document parsing, data conversion, code generation, validation scripts, or analysis.

Windows pattern:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip --cache-dir .cache\pip
.\.venv\Scripts\python -m pip install <package> --cache-dir .cache\pip
.\.venv\Scripts\python .codex-local\scripts\task.py
```

POSIX pattern:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip --cache-dir .cache/pip
./.venv/bin/python -m pip install <package> --cache-dir .cache/pip
./.venv/bin/python .codex-local/scripts/task.py
```

Rules:

- Use an existing `.venv`, `venv`, or project-managed environment if it is already repo-local and healthy.
- Do not install into the system interpreter.
- Do not use `--user`.
- Keep helper scripts under `.codex-local/scripts/` unless they are durable project code.
- Keep extracted text, converted files, and intermediate outputs under `.codex-local/output/` or a user-requested repo path.
- If dependencies are already declared in `pyproject.toml`, `requirements.txt`, `uv.lock`, `Pipfile`, or `poetry.lock`, follow the repo's toolchain while keeping environment and cache paths local.

## JavaScript And Frontend Tooling

Use project-local package managers and binaries.

Rules:

- Use existing `node_modules/.bin`, package scripts, or package-manager exec commands.
- Do not install global Node packages.
- Keep npm cache local with `npm_config_cache=.cache/npm`.
- Keep pnpm store local with `pnpm config set store-dir .cache/pnpm` or a command-local equivalent.
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
- Use disposable browser profiles under `.codex-local/tmp/`.
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

- Put downloaded files under `.codex-local/downloads/`.
- Put cloned reference repositories under `.codex-local/vendor/` unless the clone is intended to be part of the project.
- Record source URLs in a short note or script comment when the downloaded material affects reproducibility.
- Delete downloads after use unless they are useful evidence or requested outputs.

## Cleanup

Before finishing a task:

- Remove temporary scripts that are no longer needed.
- Remove intermediate outputs that are not deliverables.
- Keep durable helper scripts only when they are useful project tooling.
- Leave `.venv/`, `.cache/`, and `.codex-local/` ignored by Git unless the user wants otherwise.
- Report any repo-local artifacts left behind and why.

## Final Check

Confirm:

- No global install commands were used.
- No user-home or system cache was intentionally written when a repo-local alternative existed.
- All helper scripts and temporary artifacts are inside the repo or workspace.
- Dependency and browser caches are repo-local where supported.
- Any unavoidable global effect was explicitly authorised or clearly reported.
