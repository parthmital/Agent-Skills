---
name: kaggle-jupyter-notebooks
description: Creates, edits, refactors, validates, cleans, diffs, repairs, and merges Jupyter notebooks safely, targeting Kaggle GPU T4 x2 by default with full GPU, VRAM, CPU, and RAM use, a markdown explanation before every code cell, realtime tqdm progress, detailed metrics and plots, and a final zip-and-download cell. Use when work involves .ipynb files, notebook cells, Kaggle, Jupyter, JupyterLab, Colab, nbformat, notebook outputs, refactors or cleanup, or notebook merge conflicts. Notebooks are never executed locally.
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
4. Preserve cell IDs, order, types, attachments, and unknown metadata unless the task requires a change. Clear execution counts; never renumber them.
5. Every cell works in a fresh top-to-bottom Kaggle run, with no state from earlier runs.
6. Self-contained: no imports of local modules absent on Kaggle, unless via a Kaggle utility script or dataset.
7. Read from `/kaggle/input/` (read-only); write every output to `/kaggle/working/`.

## Structure

- First cell: markdown overview of goal, data sources, approach, model, hardware, outputs and `/kaggle/working/` layout, and required Kaggle settings (accelerator, attached datasets, Internet if `pip install` is used).
- A markdown cell before every code cell: what it does, why, key choices, expected output. Update it when the code changes.
- Numbered sections (setup, configuration, data, exploration, preprocessing, model, training, evaluation, visualisation, inference, export).
- One configuration cell near the top for paths, seeds, hyperparameters, batch sizes, epochs.
- One job per code cell.

Before creating a notebook or changing hardware setup, training, inference, evaluation, plotting, logging, or export code, read [references/kaggle-authoring.md](references/kaggle-authoring.md): multi-GPU, VRAM, CPU, and RAM use, progress, metrics and plots, output layout, and the final zip cell.

## Process

1. Triage: `python <doctor> inspect nb.ipynb`, `validate`, and `check-kaggle`. Also check kernel metadata, oversized outputs, widget state, magics, undefined names, secrets, absolute local paths, and merge markers. If invalid, `repair --backup` before changing content.
2. Edit by task:
   - New: build with `nbformat`, overview first, then alternating markdown and code cells per the authoring reference.
   - Small: locate the cell by ID or unique source fragment, change it with a notebook-aware script, keep its ID, update its markdown, then review `python <doctor> diff before.ipynb after.ipynb`.
   - Large refactor: `python <doctor> export-code nb.ipynb --output .agent-local/tmp/notebook_cells.py` for review, define shared functions once in an early cell, keep markdown in step. Only non-Kaggle notebooks with a matching package may move logic into `.py` modules.
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
| "The code is self-explanatory"             | Every code cell needs its markdown explanation.                                           |

## Red Flags

- Code cells with no markdown before them.
- Silent long-running cells with no tqdm.
- Paths outside `/kaggle/input/` or `/kaggle/working/`.
- A final cell that is not the zip-and-download cell.

## Verification

- [ ] Original backed up or recoverable from version control.
- [ ] `validate` and `check-kaggle` pass; no merge markers; cell IDs present and unique.
- [ ] Only intended cells changed; overview and per-cell explanations present.
- [ ] Authoring reference followed: both GPUs, VRAM, CPU, RAM used; tqdm and realtime output on long steps; metrics and plots saved; final zip cell with download link.
- [ ] Output policy applied; no secrets, tokens, or machine paths added.
- [ ] Report: files and cells changed, outputs kept or cleared, check results, that runtime, speed, hardware use, and metrics are unverified until run on Kaggle GPU T4 x2, and Kaggle settings the user must set.
