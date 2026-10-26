# Runtime Budget

A Kaggle session runs for at most 12 hours on CPU or GPU and 9 hours on TPU. When the limit hits, the session is killed and nothing after that point is saved. GPU sessions also use the weekly GPU quota (about 30 hours, floating). Figures checked 2026-10-26; see this repository's `RESEARCH.md`.

Goal: one "Save & Run All" session completes the full required scope with every output, inside the limit, and spends any spare time only on work that improves the results. A task that needs 20 minutes runs for 20 minutes.

## Plan Before Writing

1. List the required scope: every stage, model, fold, and output the task needs. It all completes. Never cut, shorten, or skip any of it to fit the time.
2. Estimate each stage: from stage durations in earlier runs' `logs/notebook.log`, otherwise from data size and known throughput for the model and hardware. Multiply by 1.3 for uncertainty.
3. Budget: `BUDGET = LIMIT - margin`, where `LIMIT` is 12 hours (9 on TPU) and the margin is the larger of 45 minutes and 10 percent of the limit. The margin absorbs installs, data loading variance, and slow sessions.
4. The required scope's estimate exceeds the budget: split the work (below) before writing code.
5. Otherwise, choose elastic work for the remaining budget, but only work that the task benefits from.

## Elastic Work

Ordered by typical value. Pick what helps this task, and stop each once it stops paying off:

- More epochs while validation still improves. Early stopping with patience ends training; the budget only caps it.
- More folds, seeds, or models for the ensemble and a tighter cross-validation estimate.
- A larger model, input resolution, or context length, when the timing probe shows it fits.
- Hyperparameter search with a time limit from the budget, for example Optuna `study.optimize(objective, timeout=seconds)`.
- Test-time augmentation, or a refit on all data after cross-validation.

Never fill time with work that cannot change the outputs: repeated identical runs, epochs after early stopping triggers, waiting, or redundant evaluation.

## Size It At Runtime

- `RUN_START` must be the session start: if any cell, such as `pip install`, runs before the configuration cell, set `RUN_START = time.time()` in the first code cell and remove it from the logging helpers.
- After the batch-size probe, time a short run (a few hundred steps or a small fraction of an epoch) and log seconds per step and per epoch.
- Reserve time for everything after training (evaluation, inference, plots, zip), estimated from measured validation time times 1.5.
- Compute the plan from the measurements: `units = min(max_useful, floor((BUDGET - elapsed - reserve) / unit_seconds))` for epochs, folds, seeds, or trials. Log it, for example `Plan: 5 folds x 18 epochs, estimated 8.7 h, finishing at +10.9 h of 12 h`.
- Schedules that need the total step count (cosine, OneCycle) take it from the plan, computed before training starts.
- Order work so required units come first and elastic units after them.
- Before each epoch, fold, seed, or trial, check that elapsed time plus that unit plus the reserve stays within `BUDGET`. Otherwise stop it, log why, and continue with the best checkpoint so every later cell still runs. A guard stop inside the required scope means the estimate was wrong: report it.

## Splitting Into Several Notebooks

When the required scope cannot finish in one session:

- Split along independent units: models, folds, seeds, experiments, or data shards. Each notebook is complete on its own: it loads its inputs, does its work, evaluates it, saves metrics and plots, and ends with the zip cell, all within its own budget.
- Each notebook starts from original inputs. A later notebook that combines results (an ensemble or final inference) reads earlier notebooks' final outputs only by attaching their saved versions as inputs in Kaggle (Add Input, Notebook Output), set up before the run, never by manual upload during it.
- Never resume: no notebook continues another session's unfinished work or reloads checkpoints written to continue a run later. Checkpoints within a session, such as the best weights for evaluation, are fine.
- Name them in run order (`<project>-01-<part>.ipynb`, `<project>-02-<part>.ipynb`). Each overview cell states its part, its inputs (including attached notebook outputs), and where it sits in the order.
- Report the estimated GPU hours per notebook and in total against the weekly quota.
