---
name: repo-local-workspace
description: "Keep everything a task creates or needs inside the target repository: dependencies, virtual environments, caches, browser binaries, helper scripts, logs, outputs, downloads, and temporary files, in an organised, Git-ignored folder so nothing touches system folders and past scripts can be reused. Use before installing packages, running package managers or Python helpers, writing helper scripts, saving logs or outputs, downloading tools, using Playwright or browser tooling, converting documents, cloning reference code, or any step that could write outside the repository."
---

# Repo Local Workspace

Everything a task creates or needs lives inside the target repository: tools, dependencies, helper scripts, caches, downloads, logs, outputs, and temp files. Nothing goes into global Python or Node, the user home directory, OS temp folders, system package stores, or shared caches. This keeps the machine clean, and because the work area is kept between tasks (never committed), earlier scripts and outputs can be found and reused.

Use `.agent-local/` even if the harness offers its own scratch or temp directory outside the repository, unless the user says otherwise. If a tool cannot be made repo-local, ask first and state what global path or system state it would touch. The same applies to any global SDK or system package that is not already installed.

## Layout

```text
repo/
  .venv/              Python virtual environment
  .agent-local/
    README.md         one-line-per-script index
    scripts/          helper scripts, kept for reuse
    logs/             command and script logs
    tmp/              disposable intermediate files
    output/<task>/    generated results, one folder per task
    downloads/        downloaded files
    vendor/           cloned reference repositories
    backups/          copies made before risky edits
  .cache/             tool caches: pip, uv, poetry, npm, pnpm, yarn, playwright,
                      maven, gradle, go-build, go-mod, cargo, nuget, huggingface
```

If these folders are not already ignored in a Git repository, add `.venv/`, `.agent-local/`, and `.cache/` to `.git/info/exclude`, which keeps them untracked without editing a tracked file. Edit `.gitignore` instead only when the user wants the rule shared. Never ignore source, fixtures, required assets, lockfiles, or project config.

## Workflow

1. Find the repository or workspace root.
2. Reuse an existing healthy repo-local environment (`.venv`, `venv`, or a project-managed one); create one only if none exists.
3. Before writing a helper script, check `.agent-local/scripts/` and its index, and reuse or extend an existing script rather than creating a near-duplicate.
4. Run every tool with repo-local cache, install, and temp paths. For spawned tools that create temp files, set `TMPDIR`, `TMP`, and `TEMP` to the absolute path of `.agent-local/tmp`.

Never use:

- Global installs: `pip install` outside a venv, `pip install --user`, `npm install -g`, `yarn global`, `pnpm add -g`, `pipx install`, `uv tool install`, `gem install`, or system package managers.
- User- or system-level config writes such as `npm config set`, `pnpm config set`, `git config --global`, or `pip config set`, unless scoped to the project, such as `npm config set --location project`.
- Default user-home caches for pip, npm, pnpm, Playwright, Maven, Gradle, Go, Cargo, NuGet, or browsers when a local override exists.
- Scripts or files in the user profile, OS temp, desktop, downloads folder, or global tool directories.

## Scripts, Logs, And Outputs

- Name scripts by purpose, such as `extract_pdf_tables.py`, never `script.py`, `test2.py`, or `tmp.py`.
- Start each script with a header comment giving its purpose, inputs, outputs, and exact run command. Take paths and options as arguments so it can be rerun.
- Update the `.agent-local/README.md` index whenever a script is added, renamed, or removed.
- Name logs by date and purpose, such as `.agent-local/logs/2026-09-25_pdf-extract.log`.
- Keep scripts in `.agent-local/scripts/` unless they are durable project code, and results in `.agent-local/output/<task>/` unless the user names another repository path.
- Never store secrets, tokens, or credentials in scripts, logs, or outputs.

## Python

Use the repo-local environment for all Python work, including one-off extraction, parsing, conversion, generation, validation, and analysis.

```bash
python -m venv .venv
./.venv/bin/python -m pip install <package> --cache-dir .cache/pip
./.venv/bin/python .agent-local/scripts/task.py
```

On Windows use `.\.venv\Scripts\python` and backslash paths.

- If the repository declares dependencies in `pyproject.toml`, `requirements.txt`, `uv.lock`, `Pipfile`, or `poetry.lock`, use its toolchain with local environment and cache paths.
- Set `PIP_CACHE_DIR=.cache/pip` for indirect pip use, `UV_CACHE_DIR=.cache/uv` for uv, `POETRY_VIRTUALENVS_IN_PROJECT=true` and `POETRY_CACHE_DIR=.cache/poetry` for Poetry, and `HF_HOME=.cache/huggingface` for Hugging Face.

## JavaScript

- Use `node_modules/.bin`, package scripts, or package-manager exec commands. Never install global Node packages; add a dev dependency when a tool is needed repeatedly.
- npm, `npx`, and `npm exec`: set `npm_config_cache=.cache/npm` (in PowerShell, `$env:npm_config_cache = ".cache\npm"`).
- pnpm: `pnpm install --store-dir .cache/pnpm`, or `store-dir=.cache/pnpm` in the project `.npmrc`.
- Yarn: repo-local cache configuration where the project supports it.

## Browsers And Playwright

- Set `PLAYWRIGHT_BROWSERS_PATH=.cache/playwright` before installing browsers, and prefer the repository's existing Playwright setup.
- Use disposable browser profiles under `.agent-local/tmp/`. Never attach to a personal browser profile.

## Other Ecosystems

- Maven: `-Dmaven.repo.local=.cache/maven`
- Gradle: `GRADLE_USER_HOME=.cache/gradle`
- Go: `GOCACHE=.cache/go-build` and `GOMODCACHE=.cache/go-mod`
- Rust: `CARGO_HOME=.cache/cargo` for task-specific commands when compatible
- .NET: `NUGET_PACKAGES=.cache/nuget`
- Ruby: `bundle config set path vendor/bundle`

## Downloads And External Repos

Put downloads in `.agent-local/downloads/` and reference clones in `.agent-local/vendor/`, unless the clone is meant to be part of the project. Record source URLs in a note or script comment when they affect reproducibility.

## Before Finishing

- Keep scripts, logs, outputs, and downloads that may be needed again. Delete only disposable files in `.agent-local/tmp/`, superseded copies of the same output, and large downloads that are easy to fetch again and clearly no longer needed.
- Update the `.agent-local/README.md` index.
- Confirm `.venv/`, `.cache/`, and `.agent-local/` are ignored and not staged.
- Confirm no global installs were run and nothing was written to OS temp, the user profile, or scratch directories outside the repository. Report any unavoidable global effect and whether it was authorised.
- Report which scripts, logs, and outputs were created or updated.
