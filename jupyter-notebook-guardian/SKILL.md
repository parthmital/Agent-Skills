---
name: jupyter-notebook-guardian
description: Create, edit, refactor, validate, clean, diff, repair, or merge Jupyter notebooks safely, with Kaggle GPU T4 x2 as the default runtime. Covers full use of both GPUs, VRAM, CPU cores, and RAM, a markdown explanation before every code cell, realtime tqdm progress and output, detailed metrics and plots, and a final cell that zips all outputs with a download link. Use automatically whenever work involves .ipynb files, notebook cells, Kaggle notebooks, Jupyter, JupyterLab, Colab, nbformat, notebook outputs, notebook refactors, notebook cleanup, or notebook merge conflicts. Notebooks are never executed locally.
---

# Jupyter Notebook Guardian

Use this workflow for every `.ipynb` task. The objectives are:

- No corrupted JSON, wrong-cell edits, hidden-state bugs, or noisy diffs.
- Notebooks that run on Kaggle with GPU T4 x2 and use all of that hardware for the shortest possible run time.
- Notebooks that are fully explained, show realtime progress, report detailed metrics and plots, and end with one downloadable zip of every output.

Resolve bundled scripts relative to this skill folder before running them from a target repository. In examples below, replace `<doctor>` with the absolute path to `scripts/notebook_doctor.py` inside this skill, and run it with the repository's local Python environment.

## Target Runtime

- Kaggle is the default runtime. Treat every notebook as a Kaggle notebook unless the user or the notebook clearly targets another environment.
- The default accelerator is GPU T4 x2: two NVIDIA T4 GPUs.
- Never execute notebooks locally. Do not run `jupyter nbconvert --execute`, a local kernel, or local training, and do not install the notebook's runtime dependencies locally. Local work is limited to editing notebook structure and running the static checks in this skill.
- Because the notebook is not executed locally, never claim it runs, how fast it runs, or what its metrics are. Say it must be run on Kaggle to verify.
- Keep Kaggle notebooks self-contained. Do not import from local `src/` modules that will not exist on Kaggle. Put the code in the notebook, or in a Kaggle utility script or dataset only when the user uses one.
- Read inputs from `/kaggle/input/` (read-only). Write every output to `/kaggle/working/`. Do not copy input datasets into `/kaggle/working/` unless the copy is a real output.
- If the notebook needs `pip install`, say in the overview cell that the notebook's Internet setting must be on.

## Non-negotiable Rules

1. Never edit raw notebook JSON with blind text replacement.
2. Use `nbformat` or the bundled `scripts/notebook_doctor.py` for structural changes.
3. Back up the notebook before mutation unless it is already under clean version control. `repair` and `clean` with `--backup` store backups under `<repo>/.agent-local/backups/`.
4. Preserve cell IDs, cell order, cell type, attachments, and unknown metadata unless the task requires changing them.
5. Do not renumber execution counts manually. Clear them.
6. Never assume variables exist because a notebook was previously run. Every cell must work in a fresh top-to-bottom run on Kaggle.
7. Validate before editing and after editing.
8. Never execute the notebook locally.

## Notebook Structure And Documentation

- The first cell is a markdown overview of the whole notebook: goal, data sources, approach, model or method, hardware used (GPU T4 x2), outputs produced, the layout of `/kaggle/working/`, and any Kaggle settings needed, such as accelerator and internet.
- Every code cell has a markdown cell directly before it. That markdown cell explains what the code does, why it is needed, the key choices or parameters, and what output to expect.
- Group the notebook into numbered sections with markdown headings, for example setup, configuration, data loading, exploration, preprocessing, model, training, evaluation, visualisation, inference, and export.
- Put all tunable settings in one configuration cell near the top: paths, seeds, hyperparameters, batch sizes, and number of epochs.
- Keep each code cell focused on one step. Split cells that do several unrelated things.

## Full Hardware Utilisation On Kaggle GPU T4 x2

The goal is the highest throughput and shortest run time on two T4 GPUs, with all CPU cores and RAM used where they help.

Hardware detection (first code cell after imports):

- Print the GPU count, names, and total VRAM per GPU, the CPU core count (`os.cpu_count()`), total and available RAM, and free disk space in `/kaggle/working/`.
- Assert that 2 GPUs are visible. Fail with a clear message telling the user to select GPU T4 x2 as the accelerator.
- Detect hardware at runtime instead of hardcoding core counts or memory sizes.

Use both GPUs:

- PyTorch: prefer DistributedDataParallel with one process per GPU. In a notebook, launch it with `accelerate.notebook_launcher(train_fn, num_processes=2)`, or write the training script with `%%writefile` and run `!torchrun --nproc_per_node=2 train.py`. Use `nn.DataParallel` only as a fallback, because it is slower.
- Hugging Face `Trainer` or `accelerate`: launch across both GPUs with the same launcher.
- TensorFlow or Keras: use `tf.distribute.MirroredStrategy()`.
- XGBoost, LightGBM, CatBoost, and cuML: use their GPU modes. When a library trains on one GPU per model, run two folds, seeds, or models at the same time, one per GPU, instead of leaving a GPU idle.
- Inference and embedding extraction: split the data across both GPUs.

Use all VRAM:

- Find the largest batch size that fits on each GPU with an automatic probe that catches out-of-memory errors. Leave about 10 percent headroom for memory fragmentation and evaluation.
- Use gradient accumulation to reach the target effective batch size when it does not fit in memory.
- Use fp16 mixed precision with `torch.amp.autocast("cuda", dtype=torch.float16)` and a gradient scaler. T4 GPUs have fp16 tensor cores but no fast bf16, so do not use bf16 on T4.
- Log the peak memory per GPU with `torch.cuda.max_memory_allocated(device)` after the first steps and at the end of each epoch.

Keep the GPUs fed:

- Set `DataLoader` `num_workers` from `os.cpu_count()` (divided between processes under DDP), with `pin_memory=True`, `persistent_workers=True`, and a suitable `prefetch_factor`.
- Cache decoded or preprocessed data in RAM when it fits. Move heavy augmentations to the GPU when the CPU is the bottleneck.
- Set `torch.backends.cudnn.benchmark = True` for fixed input shapes. Use `channels_last` for CNNs.
- Try `torch.compile` only when the time it saves is larger than its compile time within the session.
- Parallelise CPU-only stages such as feature engineering and file decoding across all cores with `joblib`, `multiprocessing`, or vectorised libraries.

Monitor and protect the run:

- Show per-GPU utilisation and memory in the progress bar postfix or in a log line each epoch, using `torch.cuda` memory functions or `nvidia-smi` queries. An idle GPU is a bug to fix, not an acceptable result.
- Report throughput (samples per second) and time per epoch.
- Save checkpoints to `/kaggle/working/` regularly so a session timeout does not lose all progress.
- Set seeds for reproducible data splits. Keep `cudnn.benchmark` on for speed unless the user needs bitwise reproducibility.

## Realtime Output And Progress

- Use `tqdm.auto` progress bars for every loop that takes noticeable time: epochs, batches, folds, file loading, preprocessing, inference, and zipping.
- Nest bars with `leave=False` for inner loops. Show live loss, main metric, learning rate, and GPU memory in the bar postfix.
- Under DDP, show progress bars and print only from rank 0.
- Print progress messages with `flush=True` so they appear immediately.
- Print a one-line summary after every epoch and fold.
- Update training curves live during training, for example with an `IPython.display` display handle that is refreshed each epoch.
- Also write logs to `/kaggle/working/logs/` so they are part of the final zip.
- No long-running cell may stay silent.

## Metrics And Visualisations

- Report detailed metrics suitable for the task. Classification: accuracy, precision, recall, and F1 per class and averaged, confusion matrix, ROC and PR curves, and the competition metric. Regression: RMSE, MAE, R2, a residual plot, and a predicted versus actual plot. Other tasks: the standard metrics for that task plus the competition metric.
- Track train and validation metrics per epoch and per fold, and show the cross-validation mean and standard deviation.
- Plot training and validation loss and metric curves, learning rate schedule, data distributions, and error analysis where relevant.
- Report run time per stage, throughput, and peak GPU memory.
- Display every plot inline and also save it as PNG to `/kaggle/working/plots/`.
- Save metrics as JSON or CSV to `/kaggle/working/metrics/`.
- End with a summary table of the key results.

## Output Layout And Final Zip

Write outputs to `/kaggle/working/` in this layout:

```text
/kaggle/working/
  weights/        model weights and checkpoints
  plots/          all saved figures
  metrics/        metrics as JSON or CSV
  logs/           training and run logs
  predictions/    predictions and out-of-fold outputs
  submission.csv  only for competition notebooks
  outputs.zip     created by the final cell
```

The final cell of the notebook zips everything in `/kaggle/working/` except caches and displays a download link. Adapt this pattern:

```python
import os
import shutil
import zipfile
from pathlib import Path

from IPython.display import FileLink, display
from tqdm.auto import tqdm

WORK = Path("/kaggle/working")
ZIP_PATH = WORK / "outputs.zip"
EXCLUDE_PARTS = {"__pycache__", ".cache", ".ipynb_checkpoints", "cache", "tmp", "wandb"}
STORED_SUFFIXES = {".zip", ".png", ".jpg", ".jpeg", ".pt", ".pth", ".bin", ".safetensors", ".gz", ".npz"}

files = [
    path
    for path in WORK.rglob("*")
    if path.is_file()
    and path != ZIP_PATH
    and not EXCLUDE_PARTS.intersection(path.relative_to(WORK).parts)
]
total_bytes = sum(path.stat().st_size for path in files)
free_bytes = shutil.disk_usage(WORK).free
assert free_bytes > total_bytes * 1.05, (
    f"Not enough disk space to zip {total_bytes / 1e9:.2f} GB "
    f"with {free_bytes / 1e9:.2f} GB free."
)

with zipfile.ZipFile(ZIP_PATH, "w", allowZip64=True) as archive:
    for path in tqdm(files, desc="Zipping outputs", unit="file"):
        method = zipfile.ZIP_STORED if path.suffix.lower() in STORED_SUFFIXES else zipfile.ZIP_DEFLATED
        archive.write(path, path.relative_to(WORK), compress_type=method)

print(f"Zipped {len(files)} files ({total_bytes / 1e9:.2f} GB) into {ZIP_PATH}", flush=True)
display(FileLink(os.path.relpath(ZIP_PATH)))
```

- Already compressed files such as weights and images are stored without recompression, which saves time.
- The disk check matters because the zip roughly doubles disk use in `/kaggle/working/`.
- Mention in the markdown cell before it that the zip also appears in the notebook's Output tab after a saved run.

## First-pass Triage

Run:

```bash
python <doctor> inspect path/to/notebook.ipynb
python <doctor> validate path/to/notebook.ipynb
python <doctor> check-kaggle path/to/notebook.ipynb
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
- Kaggle conventions reported by `check-kaggle`

If validation fails, repair structure before making content changes:

```bash
python <doctor> repair path/to/notebook.ipynb --backup
```

## Editing Workflow

### Creating a notebook

1. Build it with `nbformat`, not by hand-writing JSON.
2. Start with the markdown overview cell, then alternate markdown explanation and code cells.
3. Follow every section of this skill: runtime, hardware use, realtime output, metrics, and the final zip cell.
4. Run `validate` and `check-kaggle`.

### Small cell edit

1. Inspect the notebook and locate the target by cell ID or a unique source fragment.
2. Modify through a notebook-aware script.
3. Preserve the existing cell ID.
4. Update the markdown cell before it if the code's behaviour changed.
5. Validate the result and review a semantic diff rather than raw JSON noise:

```bash
python <doctor> diff before.ipynb after.ipynb
```

### Large refactor

1. Export code cells for review:

   ```bash
   python <doctor> export-code notebook.ipynb --output .agent-local/tmp/notebook_cells.py
   ```

2. Remove duplicated logic by defining functions once in an early cell and reusing them.
3. For Kaggle notebooks, keep the code inside the notebook. For notebooks that are not Kaggle notebooks and have a matching repository package, reusable logic may move into `.py` modules.
4. Keep explanatory markdown in step with the code.
5. Run `validate`, `check-kaggle`, and review the semantic diff.

## Output Policy

- Source-controlled Kaggle notebook: clear outputs and execution counts before committing, unless the user wants the Kaggle outputs kept.
- Report notebook where outputs are the deliverable: keep outputs, but remove stale errors.
- Notebook with widgets: preserve widget metadata unless explicitly cleaning it.
- Large binary or base64 outputs: remove them from the notebook. They belong in `/kaggle/working/` and the final zip.

Clean safely:

```bash
python <doctor> clean notebook.ipynb --backup
```

This clears cell outputs and execution counts while preserving source, IDs, attachments, and notebook metadata.

## Hidden-state Detection

Treat these as warnings:

- a name used before its defining cell
- non-monotonic execution counts
- repeated execution counts
- `globals()`, `locals()`, `exec`, or `eval`
- `%run` or notebook-to-notebook dependencies
- mutable global state modified across cells
- imports placed late in the notebook
- environment-dependent paths other than `/kaggle/input/` and `/kaggle/working/`
- cells whose result depends on a previously displayed object

Fix by reordering cells, adding explicit initialisation, or merging tightly coupled cells.

## Merge-conflict Recovery

Do not resolve notebook conflicts as ordinary JSON.

1. Preserve all conflicting versions.
2. Convert each version into a cell-level summary.
3. Merge by cell ID and source meaning.
4. Recreate a valid notebook through `nbformat`.
5. Validate and run `check-kaggle`.

For teams, recommend `nbdime` for notebook-aware diffs and merges and a pre-commit cleaner such as `nbstripout` when output retention is not required. See `references/precommit.md`.

## Completion Checklist

A notebook task is complete only when applicable checks pass:

- [ ] Original backed up or recoverable in version control
- [ ] Notebook passes `validate`
- [ ] Notebook passes `check-kaggle`
- [ ] No merge markers remain
- [ ] Cell IDs are present and unique
- [ ] Requested edits affect the intended cells only
- [ ] First cell is a markdown overview and every code cell has a markdown explanation before it
- [ ] Both T4 GPUs, VRAM, CPU cores, and RAM are used as described above
- [ ] tqdm progress and realtime output cover every long-running step
- [ ] Detailed metrics and plots are produced and saved
- [ ] The final cell zips all outputs except caches and shows a download link
- [ ] Outputs follow the selected output policy
- [ ] No secrets, tokens, or machine-specific paths were introduced
- [ ] The notebook was not executed locally, and this is stated in the report

## Response Format After Notebook Work

Report:

1. Files changed.
2. Cells added or changed, identified by cell ID or short source description.
3. Whether outputs were retained or cleared.
4. `validate` and `check-kaggle` results.
5. That runtime behaviour, speed, hardware use, and metrics are unverified until the notebook is run on Kaggle with GPU T4 x2.
6. Any Kaggle settings the user must set, such as accelerator, internet, or attached datasets.
