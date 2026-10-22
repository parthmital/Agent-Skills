---
name: kaggle-jupyter-notebooks
description: Creates, edits, refactors, validates, cleans, diffs, repairs, and merges Jupyter notebooks safely, targeting Kaggle GPU T4 x2 by default with full hardware use, per-cell explanations, logged progress and heartbeats, deadlock-safe multiprocessing, metrics, and an output zip. Use when work involves .ipynb files, notebook cells, Kaggle, Jupyter, JupyterLab, Colab, nbformat, notebook outputs, refactors or cleanup, notebook merge conflicts, or a Kaggle run that looks stuck, hangs, deadlocks, is slow, or shows no new log output. Notebooks are never executed locally.
---

# Kaggle Jupyter Notebooks

## Overview

No corrupted JSON, wrong-cell edits, hidden-state bugs, or noisy diffs; notebooks that run on Kaggle GPU T4 x2, use all its hardware, explain every step, show realtime progress, report detailed metrics and plots, and end with one downloadable zip.

`<doctor>` is the absolute path to this skill's `scripts/notebook_doctor.py`, run with the repo-local Python that has `nbformat`.

## When to Use

- Any `.ipynb` creation, edit, cleanup, diff, repair, or merge.
- Kaggle GPU T4 x2 is the runtime unless the user or notebook clearly targets another.

## Rules

1. Never execute notebooks locally: no `nbconvert --execute`, local kernels, training, or installs of the notebook's runtime dependencies. Never claim a notebook runs, its speed, or its metrics; those need a Kaggle run.
2. Never edit raw notebook JSON with text replacement; use `nbformat` or `<doctor>`.
3. Back up before mutating unless the file is clean in version control (`--backup` writes to `<repo>/.agent-local/backups/`).
4. Preserve cell IDs, order, types, attachments, and unknown metadata unless the task or a fix requires a change. Clear execution counts; never renumber them.
5. Every cell works in a fresh top-to-bottom Kaggle run, with no state from earlier runs.
6. Self-contained: no imports of local modules absent on Kaggle, unless via a Kaggle utility script or dataset.
7. Read from `/kaggle/input/` (read-only); write every output to `/kaggle/working/`.
8. No silent stretches. A saved Kaggle run's log shows only stdout and stderr, not tqdm bars or `display()` output. Every stage logs its start, end and duration. Every long loop logs progress with an ETA, and the log never goes more than about 2 minutes without a line, so the log alone shows whether a step is running, stuck or failed.
9. No fork after CUDA or threads. Process pools use a `spawn` context with worker functions in a `%%writefile` module, DataLoaders are created once per run, and every wait has a timeout. Forking Kaggle's multithreaded kernel deadlocks silently.

## Structure

- First cell: markdown overview of goal, data sources, approach, model, hardware, outputs and `/kaggle/working/` layout, and required Kaggle settings (accelerator, attached datasets, Internet if `pip install` is used).
- A markdown cell before every code cell: what it does, why, key choices, expected output. Update it when the code changes.
- Numbered sections (setup, configuration, data, exploration, preprocessing, model, training, evaluation, visualisation, inference, export).
- One configuration cell near the top for paths, seeds, hyperparameters, batch sizes, epochs.
- One job per code cell.

Before creating a notebook or changing hardware setup, multiprocessing, training, inference, evaluation, plotting, logging, or export code, read [references/kaggle-authoring.md](references/kaggle-authoring.md). It covers multi-GPU, VRAM, CPU and RAM use; the `log`, `heartbeat` and `progress` helpers; deadlock prevention; watching worker processes; diagnosing stuck runs; metrics and plots; the output layout; and the final zip cell.

## Process

1. Triage: `python <doctor> inspect nb.ipynb`, `validate`, and `check-kaggle`. Also check kernel metadata, oversized outputs, widget state, magics, undefined names, secrets, absolute local paths, and merge markers. If invalid, `repair --backup` before changing content.
2. Edit by task:
   - New: choose the approach, pretrained models, and datasets with `research-driven-development`, then build with `nbformat`, overview first, then alternating markdown and code cells per the authoring reference.
   - Small: locate the cell by ID or unique source fragment, change it with a notebook-aware script, keep its ID, update its markdown, then review `python <doctor> diff before.ipynb after.ipynb`.
   - Large refactor: `python <doctor> export-code nb.ipynb --output .agent-local/tmp/notebook_cells.py` for review, define shared functions once in an early cell, keep markdown in step. Only non-Kaggle notebooks with a matching package may move logic into `.py` modules.
   - Stuck or silent run (the user pastes a log that stopped, or says a run is slow or hanging): follow "Diagnosing a Run That Looks Stuck" in the authoring reference. Locate the silent stretch after the last logged line, compare it with earlier runs' timings, and diff against the last version that got past it. Fix the root cause, add logging to every stage in that stretch, and apply the liveness and deadlock rules to the whole notebook, not only the cell that hung.
   - Every edit: bring the cells you touch up to rules 8 and 9 as well.
3. Fix hidden state: names used before their defining cell, irregular execution counts, `globals()`, `locals()`, `exec`, `eval`, `%run` or cross-notebook dependencies, mutable globals changed across cells, late imports, paths outside `/kaggle/input/` and `/kaggle/working/`, cells relying on a previously displayed object. Reorder, initialise explicitly, or merge coupled cells.
4. Apply the output policy:
   - Source-controlled Kaggle notebook: clear outputs and counts before committing unless the user wants Kaggle outputs kept.
   - Report notebook whose outputs are the deliverable: keep outputs, remove stale errors.
   - Remove large binary or base64 outputs; they belong in `/kaggle/working/` and the zip. Keep widget metadata unless cleaning it.
   - `python <doctor> clean nb.ipynb --backup` clears outputs and counts; `--drop-widgets` also drops widget state.
5. Merge conflicts: never resolve as plain JSON. Keep every version, summarise each per cell, merge by cell ID and meaning, rebuild with `nbformat`. For teams, suggest `nbdime config-git --enable` for notebook-aware diffs and `nbstripout --install` when outputs need not be kept, both installed in `.venv` and repo-scoped (no `--global` unless asked), and never stripping intentional output deliverables.
6. Run `validate` and `check-kaggle` again.

## Common Rationalizations

| Rationalization                            | Reality                                                                                   |
| ------------------------------------------ | ----------------------------------------------------------------------------------------- |
| "A quick local run would confirm it works" | Local hardware and paths differ from Kaggle; it proves nothing and installs runtime deps. |
| "A regex on the JSON is faster"            | It corrupts escaping, IDs, and outputs.                                                   |
| "One GPU is enough for this"               | T4 x2 idle capacity doubles run time; the authoring reference says how to use both.       |
| "The tqdm bar shows progress"              | Not in a saved run's log; without log lines a slow step looks exactly like a deadlock.    |
| "It's probably just slow"                  | Compare with earlier timings; far beyond them, treat it as a hang and find the cause.     |
| "Fork worked last time"                    | It deadlocks once CUDA or a thread pool starts earlier; one unrelated change triggers it. |
| "The code is self-explanatory"             | Every code cell needs its markdown explanation.                                           |

## Red Flags

- Code cells with no markdown before them.
- Silent long-running cells: no tqdm, or tqdm with no log lines, or a single long call with no heartbeat.
- `ProcessPoolExecutor` or `multiprocessing.Pool` without a `spawn` context; a DataLoader created inside the epoch loop; `notebook_launcher` after CUDA use; waits without timeouts.
- Worker subprocesses whose output the notebook neither relays nor watches for stalls and failed exits.
- Paths outside `/kaggle/input/` or `/kaggle/working/`.
- A final cell that is not the zip-and-download cell.

## Verification

- [ ] Original backed up or recoverable from version control.
- [ ] `validate` and `check-kaggle` pass; no merge markers; cell IDs present and unique.
- [ ] Only intended cells and cells with fixed issues changed; overview and per-cell explanations present.
- [ ] Authoring reference followed: both GPUs, VRAM, CPU, RAM used; metrics and plots saved; final zip cell with download link.
- [ ] Liveness: every stage logs start, end and duration; long loops use `progress`, long calls `heartbeat`; workers are relayed with 5-minute status lines, stall warnings, a `faulthandler` watchdog and fail-fast exit checks. Read top to bottom, no stretch of the notebook could leave the log silent for more than about 2 minutes.
- [ ] Deadlocks: `check-kaggle` reports no fork-based pools; DataLoaders are created once; every wait has a timeout.
- [ ] Output policy applied; no secrets, tokens, or machine paths added.
- [ ] Report: files and cells changed, outputs kept or cleared, check results, that runtime, speed, hardware use, and metrics are unverified until run on Kaggle GPU T4 x2, and Kaggle settings the user must set. For a stuck run, also report whether the diagnosis is proven by the log or inferred, and tell the user to stop the hung session before rerunning.
