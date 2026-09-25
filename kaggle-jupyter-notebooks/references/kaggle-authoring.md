# Kaggle Notebook Authoring

Target: the highest throughput and shortest run time on two T4 GPUs, with every CPU core and all RAM used where they help.

## Hardware Check

In the first code cell after imports, print the GPU count, names, and VRAM per GPU, `os.cpu_count()`, total and available RAM, and free disk space in `/kaggle/working/`. Assert that 2 GPUs are visible, failing with a message telling the user to select GPU T4 x2 as the accelerator. Detect hardware at runtime; never hardcode core counts or memory sizes.

## Use Both GPUs

- PyTorch: DistributedDataParallel with one process per GPU, launched with `accelerate.notebook_launcher(train_fn, num_processes=2)` or a `%%writefile` script run with `!torchrun --nproc_per_node=2 train.py`. Use `nn.DataParallel` only as a fallback, because it is slower.
- Hugging Face `Trainer` or `accelerate`: the same launchers.
- TensorFlow or Keras: `tf.distribute.MirroredStrategy()`.
- XGBoost, LightGBM, CatBoost, and cuML: GPU modes. When a model trains on one GPU, run two folds, seeds, or models at once, one per GPU.
- Inference and embedding extraction: split the data across both GPUs.

## Use All VRAM

- Find the largest batch size per GPU with a probe that catches out-of-memory errors, leaving about 10 percent headroom for fragmentation and evaluation.
- Use gradient accumulation to reach the target effective batch size.
- Use fp16 mixed precision with `torch.amp.autocast("cuda", dtype=torch.float16)` and a gradient scaler. T4 has fp16 tensor cores but no fast bf16, so never use bf16.
- Log peak memory per GPU with `torch.cuda.max_memory_allocated(device)` after the first steps and at the end of each epoch.

## Keep The GPUs Fed

- `DataLoader`: `num_workers` from `os.cpu_count()` (divided between DDP processes), `pin_memory=True`, `persistent_workers=True`, and a suitable `prefetch_factor`.
- Cache decoded or preprocessed data in RAM when it fits. Move heavy augmentation to the GPU when the CPU is the bottleneck.
- Set `torch.backends.cudnn.benchmark = True` for fixed input shapes, unless the user needs bitwise reproducibility. Use `channels_last` for CNNs.
- Use `torch.compile` only when it saves more time than it takes to compile within the session.
- Parallelise CPU-only stages, such as feature engineering and file decoding, across all cores with `joblib`, `multiprocessing`, or vectorised libraries.

## Monitor And Protect

- Show per-GPU utilisation and memory each epoch, in the progress bar postfix or a log line, using `torch.cuda` memory functions or `nvidia-smi`. An idle GPU is a bug to fix.
- Report throughput in samples per second and time per epoch.
- Checkpoint to `/kaggle/working/` regularly so a session timeout does not lose all progress.
- Seed data splits for reproducibility.

## Realtime Output

No long-running cell may stay silent.

- Use `tqdm.auto` bars for every loop that takes noticeable time: epochs, batches, folds, file loading, preprocessing, inference, and zipping. Inner bars use `leave=False`. Show live loss, main metric, learning rate, and GPU memory in the postfix.
- Under DDP, show bars and print only from rank 0.
- Print with `flush=True`, with a one-line summary after every epoch and fold.
- Refresh training curves live each epoch, for example with an `IPython.display` display handle.
- Also write logs to `/kaggle/working/logs/`.

## Metrics And Plots

- Classification: accuracy, precision, recall, and F1 per class and averaged, confusion matrix, ROC and PR curves, and the competition metric. Regression: RMSE, MAE, R2, a residual plot, and predicted versus actual. Other tasks: the standard metrics plus the competition metric.
- Track train and validation metrics per epoch and fold, with the cross-validation mean and standard deviation.
- Plot loss and metric curves, the learning rate schedule, data distributions, and error analysis where relevant.
- Report run time per stage, throughput, and peak GPU memory.
- Display every plot inline and save it as PNG to `plots/`. Save metrics as JSON or CSV to `metrics/`.
- End with a summary table of the key results.

## Output Layout

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

## Final Zip Cell

The last cell zips everything in `/kaggle/working/` except caches and shows a download link. Its markdown cell should mention that the zip also appears in the notebook's Output tab after a saved run. Adapt this pattern:

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

Already compressed files such as weights and images are stored without recompression to save time. The disk check matters because the zip roughly doubles disk use in `/kaggle/working/`.
