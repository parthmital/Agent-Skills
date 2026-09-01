---
name: jupyter-notebook-guardian
description: Safely inspect, edit, refactor, validate, clean, diff, execute, repair, or merge Jupyter notebooks without corrupting JSON, metadata, outputs, or execution state. Use automatically whenever work involves .ipynb files, notebook cells, Jupyter Notebook, JupyterLab, Colab notebooks, nbconvert, nbformat, notebook outputs, notebook execution, notebook refactors, notebook cleanup, or notebook merge conflicts. Prefer Python modules for reusable logic and treat notebooks as thin orchestration and presentation layers.
---

# Jupyter Notebook Guardian

Use this workflow for every `.ipynb` task. The objective is to prevent corrupted JSON, hidden-state bugs, noisy diffs, accidental output loss, wrong-cell edits, and execution-order failures.

Resolve bundled scripts relative to this skill folder before running them from a target repository. In examples below, replace `<doctor>` with the absolute path to `scripts/notebook_doctor.py` inside this skill.

## Non-negotiable rules

1. Never edit raw notebook JSON with blind text replacement.
2. Use `nbformat` or the bundled `scripts/notebook_doctor.py` for structural changes.
3. Back up the notebook before mutation unless the file is generated or already under clean version control.
4. Preserve cell IDs, cell order, cell type, attachments, and unknown metadata unless the task explicitly requires changing them.
5. Do not renumber execution counts manually. Clear them or regenerate them by execution.
6. Never assume variables exist because a notebook was previously run. Analyse and verify from a fresh kernel.
7. Prefer moving reusable functions, classes, constants, and data transformations into `.py` modules.
8. Keep notebooks for orchestration, narrative, compact experiments, tables, and visualisation.
9. Validate before editing and after editing.
10. When execution is possible, restart and run all cells from top to bottom before declaring success.

## First-pass triage

Run:

```bash
python <doctor> inspect path/to/notebook.ipynb
python <doctor> validate path/to/notebook.ipynb
```

Check:

- notebook format and kernel metadata
- duplicate or missing cell IDs
- invalid notebook schema
- oversized outputs
- widget state
- execution counts that are non-monotonic or duplicated
- cells using shell commands, magics, dynamic globals, or undefined names
- embedded secrets or absolute local paths
- merge-conflict markers

If validation fails, repair structure before making content changes:

```bash
python <doctor> repair path/to/notebook.ipynb --backup
```

## Editing workflow

### Small cell edit

1. Inspect the notebook and locate the target by cell ID or a unique source fragment.
2. Modify through a notebook-aware script.
3. Preserve the existing cell ID.
4. Validate the result.
5. Show a semantic diff rather than raw JSON noise.

Use:

```bash
python <doctor> diff before.ipynb after.ipynb
```

### Large refactor

1. Export code cells to a temporary script for analysis.
2. Identify reusable logic.
3. Move reusable logic to `src/` or a nearby package.
4. Replace notebook implementations with imports and concise calls.
5. Keep plotting and explanatory cells in the notebook.
6. Run static checks on extracted modules.
7. Execute the notebook from a clean kernel.

Suggested layout:

```text
project/
  notebooks/
    analysis.ipynb
  src/
    preprocessing.py
    modelling.py
    plotting.py
  tests/
    test_preprocessing.py
    test_modelling.py
```

Export code for review:

```bash
python <doctor> export-code notebook.ipynb --output /tmp/notebook_cells.py
```

## Output policy

Default behaviour depends on intent:

- Source-controlled analytical notebook: clear transient outputs before final commit.
- Report notebook where outputs are the deliverable: retain outputs, but remove stale errors and verify regeneration.
- Notebook with widgets: preserve widget metadata unless explicitly cleaning it.
- Large binary or base64 outputs: remove or externalise them.

Clean safely:

```bash
python <doctor> clean notebook.ipynb --backup
```

This clears cell outputs and execution counts while preserving source, IDs, attachments, and notebook metadata.

## Execution verification

Preferred command:

```bash
jupyter nbconvert \
  --to notebook \
  --execute notebook.ipynb \
  --output notebook.executed.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3
```

Then validate:

```bash
python <doctor> validate notebook.executed.ipynb
```

Execution requirements:

- fresh kernel
- top-to-bottom execution
- no reliance on interactive state
- no hidden manual inputs unless documented
- deterministic seeds where randomness affects correctness
- explicit working directory assumptions
- clear errors when data or credentials are unavailable

If dependencies or data prevent execution, state exactly what could not be verified. Do not claim the notebook runs.

## Hidden-state detection

Treat these as warnings:

- a name used before its defining cell
- non-monotonic execution counts
- repeated execution counts
- `globals()`, `locals()`, `exec`, or `eval`
- `%run` or notebook-to-notebook dependencies
- mutable global state modified across cells
- imports placed late in the notebook
- environment-dependent paths
- cells whose result depends on a previously displayed object

Fix by reordering cells, adding explicit initialisation, extracting modules, or merging tightly coupled cells.

## Merge-conflict recovery

Do not resolve notebook conflicts as ordinary JSON.

1. Preserve all conflicting versions.
2. Convert each version into a cell-level summary.
3. Merge by cell ID and source meaning.
4. Recreate a valid notebook through `nbformat`.
5. Validate and execute.

For teams, recommend `nbdime` for notebook-aware diffs and merges and a pre-commit cleaner such as `nbstripout` when output retention is not required.

## Completion checklist

A notebook task is complete only when applicable checks pass:

- [ ] Original backed up or recoverable in version control
- [ ] Notebook parses as JSON
- [ ] Notebook passes `nbformat` validation
- [ ] No merge markers remain
- [ ] Cell IDs are present and unique
- [ ] Requested edits affect the intended cells only
- [ ] Outputs follow the selected output policy
- [ ] Reusable logic is extracted where worthwhile
- [ ] Fresh-kernel execution succeeds, or limitations are stated
- [ ] Semantic diff is reviewed
- [ ] No secrets, tokens, or machine-specific paths were introduced

## Response format after notebook work

Report:

1. Files changed.
2. Cells changed, identified by cell ID or short source description.
3. Whether outputs were retained or cleared.
4. Validation result.
5. Fresh-kernel execution result.
6. Any unresolved dependency, data, credential, or environment issue.
