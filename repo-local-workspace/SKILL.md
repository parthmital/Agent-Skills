---
name: repo-local-workspace
description: "Keeps everything a task creates or needs inside the target repository: dependencies, virtual environments, caches, browser binaries, helper scripts, logs, outputs, downloads, and temporary files, in an organised, Git-ignored folder so nothing touches system folders and past scripts can be reused. Use before installing packages, running package managers or Python helpers, writing helper scripts, saving logs or outputs, downloading tools, using Playwright or browser tooling, converting documents, cloning reference code, or any step that could write outside the repository."
---

# Repo Local Workspace

## Overview

Nothing goes into global Python or Node, the user home, OS temp, system package stores, or shared caches. The machine stays clean, and because the work area persists between tasks (never committed), earlier scripts and outputs can be reused.

## When to Use

- Any install, download, helper script, log, output, cache, or temp file.
- Use `.agent-local/` even when the harness offers its own scratch or temp directory, unless the user says otherwise.
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
    downloads/        downloaded files
    vendor/           cloned reference repositories
    backups/          copies made before risky edits
  .cache/             tool caches (pip, uv, npm, pnpm, playwright, maven, ...)
```

Add `.venv/`, `.agent-local/`, and `.cache/` to the root `.gitignore` if missing, following its grouping. Never ignore source, fixtures, required assets, lockfiles, or project config.

## Process

1. Find the repository root.
2. Reuse a healthy repo-local environment (`.venv`, `venv`, or project-managed); create one only if none exists. Use the repo's declared toolchain (`pyproject.toml`, `requirements.txt`, `uv.lock`, `Pipfile`, `poetry.lock`) with local paths.
3. Before writing a helper script, check `.agent-local/scripts/` and its index; extend an existing script rather than adding a near-duplicate.
4. Run every tool with repo-local cache, install, and temp paths; set `TMPDIR`, `TMP`, and `TEMP` to the absolute path of `.agent-local/tmp` for tools that spawn temp files.

## Local Paths

- Python: `python -m venv .venv`, then `.venv/bin/python -m pip install <pkg> --cache-dir .cache/pip` (Windows: `.venv\Scripts\python`). `PIP_CACHE_DIR=.cache/pip`, `UV_CACHE_DIR=.cache/uv`, `POETRY_VIRTUALENVS_IN_PROJECT=true` with `POETRY_CACHE_DIR=.cache/poetry`, `HF_HOME=.cache/huggingface`.
- Node: `node_modules/.bin`, package scripts, or exec commands; a dev dependency for repeated tools. `npm_config_cache=.cache/npm` (PowerShell: `$env:npm_config_cache = ".cache\npm"`); `pnpm install --store-dir .cache/pnpm` or `store-dir` in project `.npmrc`; Yarn's repo-local cache where supported.
- Playwright: `PLAYWRIGHT_BROWSERS_PATH=.cache/playwright`; disposable profiles under `.agent-local/tmp/`, never a personal profile.
- Maven `-Dmaven.repo.local=.cache/maven`; Gradle `GRADLE_USER_HOME=.cache/gradle`; Go `GOCACHE=.cache/go-build`, `GOMODCACHE=.cache/go-mod`; Rust `CARGO_HOME=.cache/cargo` when compatible; .NET `NUGET_PACKAGES=.cache/nuget`; Ruby `bundle config set path vendor/bundle`.
- Downloads in `.agent-local/downloads/`, reference clones in `.agent-local/vendor/`; record source URLs when they affect reproducibility.

Never: `pip install` outside a venv or with `--user`, `npm install -g`, `yarn global`, `pnpm add -g`, `pipx install`, `uv tool install`, `gem install`, system package managers, user- or system-level config writes (`npm config set`, `git config --global`, `pip config set`) unless project-scoped, or files in the user profile, OS temp, desktop, or downloads folder.

## Scripts And Outputs

- Name scripts by purpose (`extract_pdf_tables.py`, never `script.py` or `tmp.py`), with a header comment giving purpose, inputs, outputs, and run command. Take paths and options as arguments.
- Update `.agent-local/README.md` whenever a script is added, renamed, or removed.
- Results go in `.agent-local/output/<task>/` unless the user names another path; durable project code goes in the project.
- Never store secrets in scripts, logs, or outputs.

## Common Rationalizations

| Rationalization                      | Reality                                                         |
| ------------------------------------ | --------------------------------------------------------------- |
| "The harness scratch folder is fine" | It is lost after the session; scripts cannot be reused.         |
| "One global install is harmless"     | It pollutes the machine and hides the dependency from the repo. |
| "I'll write a quick new script"      | Check the index first; near-duplicates pile up.                 |

## Red Flags

- `-g`, `--user`, or `--global` in a command.
- Paths under the user profile, `%TEMP%`, or `/tmp`.
- Generic script names or a stale index.

## Verification

- [ ] `.venv/`, `.cache/`, `.agent-local/` ignored and not staged.
- [ ] Only disposable `tmp/` files, superseded outputs, and large easily refetched downloads deleted; reusable scripts, logs, and outputs kept.
- [ ] Index updated; created or updated scripts, logs, and outputs reported.
- [ ] No global installs or writes outside the repo, or each unavoidable one reported with whether it was authorised.
