---
name: kaggle-jupyter-notebooks
description: Create, edit, refactor, validate, clean, diff, repair, or merge Jupyter notebooks safely, with Kaggle GPU T4 x2 as the default runtime. Covers full use of both GPUs, VRAM, CPU cores, and RAM, a markdown explanation before every code cell, realtime tqdm progress, detailed metrics and plots, and a final cell that zips all outputs with a download link. Use whenever work involves .ipynb files, notebook cells, Kaggle notebooks, Jupyter, JupyterLab, Colab, nbformat, notebook outputs, notebook refactors or cleanup, or notebook merge conflicts. Notebooks are never executed locally.
---

# Kaggle Jupyter Notebooks

Goals: no corrupted JSON, wrong-cell edits, hidden-state bugs, or noisy diffs; notebooks that run on Kaggle GPU T4 x2 and use all of its hardware; and notebooks that are fully explained, show realtime progress, report detailed metrics and plots, and end with one downloadable zip of every output.

`<doctor>` below is the absolute path to this skill's `scripts/notebook_doctor.py`. Run it with the target repository's local Python environment, which needs `nbformat`.

## Rules

1. Kaggle with GPU T4 x2 is the runtime unless the user or the notebook clearly targets another environment.
2. Never execute notebooks locally: no `jupyter nbconvert --execute`, local kernels, local training, or local installs of the notebook's runtime dependencies. Local work is structural editing plus the static checks here. So never claim a notebook runs, how fast it runs, or what its metrics are; say it must be run on Kaggle to verify.
3. Never edit raw notebook JSON with text replacement. Use `nbformat` or `<doctor>`.
4. Back up before mutating unless the file is clean in version control. `--backup` on `repair` and `clean` writes to `<repo>/.agent-local/backups/`.
5. Preserve cell IDs, order, types, attachments, and unknown metadata unless the task requires a change. Clear execution counts; never renumber them by hand.
6. Every cell must work in a fresh top-to-bottom run on Kaggle. Never rely on state from an earlier run.
7. Keep Kaggle notebooks self-contained: no imports from local modules that will not exist on Kaggle, unless the user uses a Kaggle utility script or dataset.
8. Read inputs from `/kaggle/input/` (read-only) and write every output to `/kaggle/working/`. Copy inputs there only if the copy is a real output.
9. Validate before and after editing.

## Structure

- First cell: markdown overview of the goal, data sources, approach, model or method, hardware (GPU T4 x2), outputs and the `/kaggle/working/` layout, and required Kaggle settings: accelerator, attached datasets, and Internet on if the notebook uses `pip install`.
- A markdown cell directly before every code cell, explaining what the code does, why it is needed, key choices or parameters, and the expected output. Update it whenever the code's behaviour changes.
- Numbered markdown sections, such as setup, configuration, data loading, exploration, preprocessing, model, training, evaluation, visualisation, inference, and export.
- One configuration cell near the top for paths, seeds, hyperparameters, batch sizes, and epochs.
- One job per code cell. Split cells that do unrelated things.

Before creating a notebook, or writing or changing its hardware setup, training, inference, evaluation, plotting, logging, or export code, read [references/kaggle-authoring.md](references/kaggle-authoring.md). It defines full GPU, VRAM, CPU, and RAM use, realtime progress, required metrics and plots, the output layout, and the final zip cell.

## Triage

```bash
python <doctor> inspect nb.ipynb
python <doctor> validate nb.ipynb
python <doctor> check-kaggle nb.ipynb
```

Also check kernel metadata, oversized outputs, widget state, shell commands and magics, undefined names, embedded secrets, absolute local paths, and merge-conflict markers. If validation fails, repair structure before changing content: `python <doctor> repair nb.ipynb --backup`.

## Editing

- New notebook: build it with `nbformat`, overview first, then alternating markdown and code cells following the authoring reference. Run `validate` and `check-kaggle`.
- Small edit: locate the cell by ID or a unique source fragment, change it with a notebook-aware script, keep its ID, update the markdown before it, validate, and review `python <doctor> diff before.ipynb after.ipynb` instead of raw JSON.
- Large refactor: export code for review with `python <doctor> export-code nb.ipynb --output .agent-local/tmp/notebook_cells.py`, define shared functions once in an early cell, keep markdown in step, then run `validate`, `check-kaggle`, and `diff`. Only notebooks that are not Kaggle notebooks and have a matching repository package may move logic into `.py` modules.

## Output Policy

- Source-controlled Kaggle notebook: clear outputs and execution counts before committing, unless the user wants the Kaggle outputs kept.
- Report notebook whose outputs are the deliverable: keep outputs, remove stale errors.
- Keep widget metadata unless explicitly cleaning it.
- Remove large binary or base64 outputs. They belong in `/kaggle/working/` and the zip.

`python <doctor> clean nb.ipynb --backup` clears outputs and execution counts while keeping source, IDs, attachments, and metadata. Add `--drop-widgets` to remove widget state.

## Hidden State

Warn on names used before their defining cell, non-monotonic or repeated execution counts, `globals()`, `locals()`, `exec`, `eval`, `%run` or cross-notebook dependencies, mutable globals changed across cells, late imports, paths other than `/kaggle/input/` and `/kaggle/working/`, and cells that depend on a previously displayed object. Fix by reordering, adding explicit initialisation, or merging tightly coupled cells.

## Merge Conflicts

Never resolve them as ordinary JSON. Keep every conflicting version, summarise each at cell level, merge by cell ID and meaning, rebuild with `nbformat`, then run `validate` and `check-kaggle`. For teams, recommend `nbdime` for notebook-aware diffs and merges, and `nbstripout` when outputs need not be kept; see [references/precommit.md](references/precommit.md).

## Done When

- The original is backed up or recoverable from version control.
- `validate` and `check-kaggle` pass, no merge markers remain, and cell IDs are present and unique.
- Only the intended cells changed, and the overview and per-cell explanations are present.
- The authoring reference is followed: both GPUs, VRAM, CPU cores, and RAM used; tqdm and realtime output on every long step; metrics and plots produced and saved; final zip cell with a download link.
- The output policy is applied, and no secrets, tokens, or machine-specific paths were introduced.

Report: files changed; cells added or changed, by ID or short description; whether outputs were kept or cleared; `validate` and `check-kaggle` results; that runtime behaviour, speed, hardware use, and metrics are unverified until the notebook runs on Kaggle with GPU T4 x2; and Kaggle settings the user must set, such as accelerator, Internet, and attached datasets.
