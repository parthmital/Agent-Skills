# Kaggle Notebook Authoring

Target: the highest throughput and shortest run time on two T4 GPUs, with every CPU core and all RAM used where they help.

## Hardware Check

In the first code cell after imports, print the GPU count, names, and VRAM per GPU, `os.cpu_count()`, total and available RAM, and free disk space in `/kaggle/working/`. Assert that 2 GPUs are visible, failing with a message telling the user to select GPU T4 x2 as the accelerator. Detect hardware at runtime; never hardcode core counts or memory sizes.

## Use Both GPUs

- PyTorch: DistributedDataParallel with one process per GPU, launched with `accelerate.notebook_launcher(train_fn, num_processes=2)` (only if the notebook has not touched CUDA yet, see "Prevent Deadlocks") or a `%%writefile` script run with `!torchrun --nproc_per_node=2 train.py`. Use `nn.DataParallel` only as a fallback, because it is slower.
- Hugging Face `Trainer` or `accelerate`: the same launchers.
- TensorFlow or Keras: `tf.distribute.MirroredStrategy()`.
- XGBoost, LightGBM, CatBoost, and cuML: GPU modes. When a model trains on one GPU, run two folds, seeds, or models at once, one per GPU.
- Inference and embedding extraction: split the data across both GPUs.

## Use All VRAM

- Find the largest batch size per GPU with a probe that catches out-of-memory errors, leaving about 10 percent headroom for fragmentation and evaluation.
- Use gradient accumulation to reach the target effective batch size.
- Use fp16 mixed precision with `torch.amp.autocast("cuda", dtype=torch.float16)` and a gradient scaler. T4 has fp16 tensor cores but no fast bf16, so never use bf16.
- Log peak memory per GPU with `torch.cuda.max_memory_allocated(device)` after the first steps and at the end of each epoch.
- **`OutOfMemoryError` in a post-training cell (Grad-CAM, inference) with GBs "reserved but unallocated"**: the notebook process fragments memory and stacks every model on one GPU. Set `os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"` in the first cell before importing torch (workers too), spread models over both GPUs, and per item retry once after `gc.collect()` and `empty_cache()` outside the `except`, then skip with a warning. Grad-CAM: freeze weights, return `output.detach().requires_grad_()` from the forward hook and take `torch.autograd.grad(target, leaf)`, which gives identical maps without the encoder graph or weight gradients. Check: compare maps with the full-backward version on CPU.

## Keep The GPUs Fed

- `DataLoader`: `num_workers` from `os.cpu_count()` (divided between DDP processes), `pin_memory=True`, `persistent_workers=True`, and a suitable `prefetch_factor`, created once per run, not per epoch.
- Cache decoded or preprocessed data in RAM when it fits. Move heavy augmentation to the GPU when the CPU is the bottleneck.
- Set `torch.backends.cudnn.benchmark = True` for fixed input shapes, unless the user needs bitwise reproducibility. Use `channels_last` for CNNs.
- Use `torch.compile` only when it saves more time than it takes to compile within the session.
- Parallelise CPU-only stages, such as feature engineering and file decoding, across all cores with `joblib`, `multiprocessing`, or vectorised libraries.

## Monitor And Protect

- Show per-GPU utilisation and memory each epoch, in the progress bar postfix or a log line, using `torch.cuda` memory functions or `nvidia-smi`. An idle GPU is a bug to fix.
- Report throughput in samples per second and time per epoch.
- Checkpoint to `/kaggle/working/` regularly so a session timeout does not lose all progress.
- A time budget covers the whole run, not only training epochs: set the training deadline from the notebook start minus a reserve for the post-training cells and zip, stop before an epoch when that epoch plus the evaluation (estimated from the measured validation time) would pass it, and still evaluate the best checkpoint so later cells have every model.
- Seed data splits for reproducibility.

## Realtime Output and Liveness

A saved Kaggle run ("Save & Run All") is watched through its log, and that log shows only stdout and stderr streams. `tqdm.auto` bars are widgets and `display()` output is rich output: neither appears there. A cell whose only output is a bar or a table therefore looks dead, and a slow stage, a deadlock and a crashed worker all look the same: no new lines. The goal is that the log alone always answers three questions: what is running, how far it has got, and whether it is still moving.

- **Never more than about 2 minutes without a log line** while the notebook works, and a line at the start and end of every stage that takes more than a few seconds, with its duration and key counts (cases found, rows, files, batch size chosen).
- Define `log`, `heartbeat` and `progress` (below) in the configuration cell and use them everywhere. `progress` replaces bare `tqdm` for every loop that takes noticeable time: epochs, folds, file loading, preprocessing, inference, scoring and zipping. Its bar still updates in an interactive session, and it adds log lines every tenth of the items, with elapsed time and ETA.
- Wrap long calls that have no loop (model download or build, `torch.compile`, a big file read, `pip install`, a library `fit` with no callback) in `with heartbeat("..."):`.
- Training logs one line per epoch (loss, main metric, learning rate, throughput, peak GPU memory, epoch time) and an intra-epoch status line at least every few minutes. Keras: `verbose=2` (one line per epoch, not a bar). Hugging Face `Trainer`: `disable_tqdm=True` with `logging_steps`, so its `PrinterCallback` prints plain lines.
- Under DDP, log only from rank 0. Rank 0 also includes every rank's status where it can, so a single stuck rank is visible.
- Worker scripts (`torchrun`, one process per GPU, background jobs) log plain timestamped lines with `flush=True`, not tqdm bars, because bars in a redirected log turn into carriage-return noise. The notebook relays their lines and watches them (see "Watch Worker Processes").
- Refresh training curves live each epoch, for example with an `IPython.display` display handle.
- Everything logged also goes to `/kaggle/working/logs/`.

```python
import faulthandler
import math
import threading
import time
from contextlib import contextmanager

from tqdm.auto import tqdm

LOGS = WORK / "logs"
LOGS.mkdir(parents=True, exist_ok=True)
RUN_START = time.time()
_last_log = [RUN_START]


def log(message):
    """Timestamped line on stdout (the only output a saved run's log shows) and in logs/notebook.log."""
    _last_log[0] = time.time()
    line = f"[{time.strftime('%H:%M:%S')} +{(_last_log[0] - RUN_START) / 60:.1f}m] {message}"
    print(line, flush=True)
    with open(LOGS / "notebook.log", "a") as handle:
        handle.write(line + "\n")


@contextmanager
def heartbeat(desc, status=None, quiet_seconds=120, stall_seconds=1200):
    """Proof of life for a long step. Logs `desc` (and `status()`) whenever nothing has been logged
    for `quiet_seconds`. If `status` is given and its value stops changing for `stall_seconds`, dumps
    every thread's stack to logs/stacks.log, so a deadlock shows where it is stuck."""
    stop, start = threading.Event(), time.time()

    def beat():
        last, changed = (status() if status else None), time.time()
        while not stop.wait(15):
            now, current = time.time(), (status() if status else None)
            if current != last:
                last, changed = current, now
            if now - _last_log[0] >= quiet_seconds:
                log(f"{desc}: still running after {(now - start) / 60:.1f} min {current or ''}".rstrip())
            if status and now - changed >= stall_seconds:
                with open(LOGS / "stacks.log", "a") as handle:
                    handle.write(f"\n=== {time.strftime('%H:%M:%S')} {desc}: no progress ===\n")
                    handle.flush()
                    faulthandler.dump_traceback(file=handle, all_threads=True)
                log(f"WARNING {desc}: no progress for {(now - changed) / 60:.0f} min; stacks in logs/stacks.log")
                changed = now

    thread = threading.Thread(target=beat, daemon=True)
    log(f"{desc}: started")
    thread.start()
    try:
        yield
    finally:
        stop.set()
        thread.join()
        log(f"{desc}: finished in {(time.time() - start) / 60:.1f} min")


def progress(iterable, desc, total=None, log_fraction=0.1):
    """tqdm bar plus log lines every tenth of the items, a heartbeat while the log is quiet, and a
    stack dump if no item finishes for 20 minutes."""
    if total is None and hasattr(iterable, "__len__"):
        total = len(iterable)
    step = max(1, math.ceil(total * log_fraction)) if total else None
    done, start = [0], time.time()
    with heartbeat(desc, status=lambda: f"({done[0]}/{total or '?'} done)"):
        for item in tqdm(iterable, total=total, desc=desc):
            yield item
            done[0] += 1
            if step and done[0] % step == 0:
                elapsed = time.time() - start
                eta = (total - done[0]) * elapsed / done[0]
                log(f"{desc}: {done[0]}/{total} in {elapsed / 60:.1f} min, ETA {eta / 60:.1f} min")
```

`progress` is a generator, so it starts on the first item and finishes after the last one has been processed. When it is zipped with another sequence, put it first (`zip(progress(results, ...), names)`). Otherwise `zip` stops on the shorter partner and the closing log line never runs.

## Prevent Deadlocks

Hangs on Kaggle usually come from forking. Kaggle's kernel already runs threads: the IPython kernel, Kaggle's debugger, tqdm's monitor, and the CUDA and OpenMP pools that start once PyTorch has touched a GPU or run a large CPU operation. `fork()` copies only the calling thread. A child that later needs a lock or thread pool another thread held at the moment of the fork waits forever, silently. Python 3.14 stopped defaulting to `fork` on Linux for this reason, but Kaggle's Python still defaults to it.

- **Process pools** (`ProcessPoolExecutor`, `multiprocessing.Pool`): pass `mp_context=multiprocessing.get_context("spawn")` (or use `get_context("spawn").Pool`). Spawned children are fresh interpreters, so the worker function must live in an importable module written with `%%writefile` (for example `src/lib.py`, with `src/` on `sys.path`), not in the notebook. Spawn children inherit the parent's `sys.path`. Prefer `ProcessPoolExecutor`: if a worker is killed (for example out of memory), it raises `BrokenProcessPool`, while `multiprocessing.Pool` can wait forever.
- Pool workers that only do CPU work should not call PyTorch, CUDA or thread-pool APIs (`torch.set_num_threads`, `torch.cuda.*`). joblib's default `loky` backend already starts fresh processes.
- **DataLoader**: create it once per run, with `persistent_workers=True` or one iterator spanning all epochs (for example `itertools.islice` per epoch). Do not create it each epoch: every new iterator forks the workers again from a process with live CUDA and threads.
- **`accelerate.notebook_launcher`** forks the kernel and refuses to start once CUDA has been initialised. Do no CUDA work in the notebook before it, or launch a `%%writefile` script with `torchrun` instead.
- **Timeouts on every wait**: `future.result(timeout=...)`, `process.wait(timeout=...)`, polling loops that also check `process.poll()`, and `dist.init_process_group(..., timeout=timedelta(minutes=30))`, so that a hung collective raises instead of blocking forever. No bare `.join()` or `.wait()` on something that might never finish.
- Collectives must be reached by every rank: no rank-dependent early `return`/`break` or rank-0-only evaluation that calls `all_reduce`/`barrier`.

## Watch Worker Processes

When training runs in subprocesses (one per GPU or `torchrun` in the background), the notebook cell that waits for them must:

- Relay new complete lines from each worker's log file as they arrive. Read in binary mode from a saved offset and keep a partial last line for the next poll.
- Log one status line per worker every 5 minutes (job, step/total, loss, memory), even when the workers print nothing.
- Warn with the tail of the worker's log when a worker's log or status file has not changed for a stall window (for example 30 minutes).
- Check `process.poll()` on every loop. When a worker exits non-zero, stop the others and raise with the last 40 lines of its log, rather than waiting for the rest.

Inside each worker script, call `faulthandler.enable()` at start-up, so crashes print a traceback to the worker log. Re-arm `faulthandler.dump_traceback_later(STALL_SECONDS, repeat=True)` after every logged step, and cancel it at the end. If a step hangs, the worker then writes every thread's stack to its own log, and that shows exactly where it is stuck.

## Diagnosing a Run That Looks Stuck

When the user reports a run that shows no new output:

1. Find the last line in the log and the cell that printed it. List the cells after it that write nothing to stdout (only bars, `display()` or files). The run is somewhere in that stretch.
2. Compare the time since that line with earlier runs (`logs/notebook.log` in downloaded outputs, or stage timings in the README) or with an estimate from data size. If it is far beyond, treat it as a hang, not as slowness.
3. Diff the notebook against the last version that got past that point (`git log`/`git diff`). Most hangs come from a recent change, such as models now built on the CPU or CUDA initialised earlier.
4. Check the usual causes: fork after CUDA or threads (pools, DataLoaders, `notebook_launcher`), a collective not reached by every rank, a wait without a timeout on a dead subprocess, a polling loop that never checks the exit code, an out-of-memory-killed worker under `multiprocessing.Pool`, an `input()` or interactive prompt, a pip install waiting for a resolver.
5. Fix the root cause, and also add the logging above to every stage in the silent stretch, so the next run localises any remaining stall to one stage.
6. Tell the user to stop the current session and rerun. Say whether the cause is proven by the log or inferred.

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
  logs/           notebook.log, worker logs, stacks.log (thread stacks of any detected stall)
  predictions/    predictions and out-of-fold outputs
  submission.csv  only for competition notebooks
  outputs.zip     created by the final cell
```

## Final Zip Cell

The last cell zips everything in `/kaggle/working/` except caches and shows a download link. Its markdown cell should mention that the zip also appears in the notebook's Output tab after a saved run. Adapt this pattern (`log` and `progress` come from the configuration cell):

```python
import os
import shutil
import zipfile
from pathlib import Path

from IPython.display import FileLink, display

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
    for path in progress(files, "Zipping outputs"):
        method = zipfile.ZIP_STORED if path.suffix.lower() in STORED_SUFFIXES else zipfile.ZIP_DEFLATED
        archive.write(path, path.relative_to(WORK), compress_type=method)

log(f"Zipped {len(files)} files ({total_bytes / 1e9:.2f} GB) into {ZIP_PATH}")
display(FileLink(os.path.relpath(ZIP_PATH)))
```

Already compressed files such as weights and images are stored without recompression to save time. The disk check matters because the zip roughly doubles disk use in `/kaggle/working/`.
