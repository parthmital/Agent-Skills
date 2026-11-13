---
name: repo-local-workspace
description: Keeps everything a task creates or needs (dependencies, environments, caches, browser binaries, helper scripts, logs, outputs, downloads, temp files) in Git-ignored folders inside the target repository. Use before installing packages, running package managers or Python helpers, writing helper scripts, saving logs or outputs, downloading tools, using Playwright or browser tooling, converting documents, cloning reference code, or any step that could write outside the repository.
---

# Repo Local Workspace

## Overview

Nothing goes into global Python or Node, the user home, OS temp, system package stores, or shared caches. The machine stays clean, every dependency is visible in the repository, and because the work area persists between tasks (never committed), earlier scripts and outputs are reused instead of rewritten.

## When to Use

- Any install, download, helper script, log, output, cache, or temp file.
- Use `.agent-local/` even when the harness offers its own scratch or temp directory, unless the user says otherwise.
- Subagent briefs name this layout, so workers write to the same folders.
- If a tool cannot be made repo-local, or needs a global SDK or system package not already installed, ask first and state what global path or state it would touch.

## Layout

```text
repo/
  .venv/              Python virtual environment
  .agent-local/
    README.md         one-line-per-script index
    scripts/          helper scripts, kept for reuse
    logs/             <date>_<purpose>.log
    tmp/              disposable intermediate files
    output/<task>/    generated results
    downloads/        downloaded files (untrusted)
    vendor/           cloned reference repositories (untrusted)
    backups/          copies made before risky edits
  .cache/             tool caches (pip, uv, npm, pnpm, playwright, maven, ...)
```

## Process

1. Find the repository root. Add `.venv/`, `.agent-local/`, and `.cache/` to the root `.gitignore` if missing, following its grouping.
2. Reuse a healthy repo-local environment (`.venv`, `venv`, or project-managed). Create one only if none exists, with the repository's declared toolchain (`pyproject.toml`, `requirements.txt`, `uv.lock`, `Pipfile`, `poetry.lock`, `package.json` and its lockfile).
3. Before writing a helper script, check `.agent-local/README.md` and `scripts/`. Extend an existing script rather than adding a near-duplicate.
4. Run every tool with repo-local cache, install, and temp paths (Local Paths below). Set `TMPDIR`, `TMP`, and `TEMP` to the absolute path of `.agent-local/tmp` for tools that spawn temp files.
5. Treat downloads and clones as untrusted: one new folder each, read install scripts before running them, and run Python that reads them with `-I`.
6. Before finishing, delete disposable `tmp/` files, update the index, and report what was created.

## Local Paths

- Python: `python -m venv .venv`, then `.venv/bin/python -m pip install <pkg> --cache-dir .cache/pip` (Windows: `.venv/Scripts/python`). `PIP_CACHE_DIR=.cache/pip`, `UV_CACHE_DIR=.cache/uv`, `POETRY_VIRTUALENVS_IN_PROJECT=true` with `POETRY_CACHE_DIR=.cache/poetry`, `HF_HOME=.cache/huggingface`.
- uv Python: `UV_PYTHON_INSTALL_DIR=.cache/python uv python install --no-bin <ver>`. Without `--no-bin`, uv writes `python<ver>.exe` into `%USERPROFILE%\.local\bin`, outside the repository.
- Node: `node_modules/.bin`, package scripts, or `npx` for one-off tools, a dev dependency for repeated ones. `npm_config_cache=.cache/npm` (PowerShell: `$env:npm_config_cache = ".cache\npm"`), `pnpm install --store-dir .cache/pnpm` or `store-dir` in the project `.npmrc`, Yarn's repo-local cache where supported.
- Playwright: `PLAYWRIGHT_BROWSERS_PATH=.cache/playwright`, disposable profiles under `.agent-local/tmp/`, never a personal profile.
- Maven `-Dmaven.repo.local=.cache/maven`, Gradle `GRADLE_USER_HOME=.cache/gradle`, Go `GOCACHE=.cache/go-build` and `GOMODCACHE=.cache/go-mod`, Rust `CARGO_HOME=.cache/cargo` when compatible, .NET `NUGET_PACKAGES=.cache/nuget`, Ruby `bundle config set --local path vendor/bundle`.
- Downloads in `.agent-local/downloads/`, reference clones in `.agent-local/vendor/`. Record source URLs when they affect reproducibility.

Never: `pip install` outside a venv or with `--user`, `npm install -g`, `yarn global`, `pnpm add -g`, `pipx install`, `uv tool install`, `gem install`, system package managers, user- or system-level config writes (`npm config set`, `git config --global`, `pip config set`) unless project-scoped, or files in the user profile, OS temp, desktop, or downloads folder.

## Scripts and Outputs

- Name scripts per `naming-conventions`: snake_case, verb first, with a header comment giving purpose, inputs, outputs, and run command. Take paths and options as arguments.
- Update `.agent-local/README.md` whenever a script is added, renamed, or removed.
- Results go in `.agent-local/output/<task>/` unless the user names another path. Durable project code goes in the project.
- Never store secrets in scripts, logs, or outputs.

## Examples

Bad: `pip install pdfplumber` then a new `tmp.py` in the system temp folder.

Good:

```text
.venv/Scripts/python -m pip install pdfplumber --cache-dir .cache/pip
.agent-local/scripts/extract_pdf_tables.py   # header: purpose, inputs, outputs, run command
.agent-local/README.md                       # - extract_pdf_tables.py: PDF tables to CSV in output/<task>/
```

## Common Rationalisations

| Rationalisation                      | Reality                                                         |
| ------------------------------------ | --------------------------------------------------------------- |
| "The harness scratch folder is fine" | It is lost after the session, so scripts cannot be reused.      |
| "One global install is harmless"     | It pollutes the machine and hides the dependency from the repo. |
| "I'll write a quick new script"      | Check the index first. Near-duplicates pile up.                 |

## Red Flags

- `-g`, `--user`, or `--global` in a command.
- Paths under the user profile, `%TEMP%`, or `/tmp`.
- Generic script names (`script.py`, `tmp.py`, `test2.py`) or a stale index.

## Verification

- [ ] `.venv/`, `.cache/`, `.agent-local/` ignored and not staged.
- [ ] Only disposable `tmp/` files, superseded outputs, and large easily refetched downloads deleted. Reusable scripts, logs, and outputs kept.
- [ ] Index updated, and created or updated scripts, logs, and outputs reported.
- [ ] No global installs or writes outside the repository, or each unavoidable one reported with whether it was authorised.
