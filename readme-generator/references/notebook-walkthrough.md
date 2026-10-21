# Notebook Repository Walkthrough

Applies when the repo has `.ipynb` files with downloaded outputs (usually `outputs/` or an extracted `outputs.zip` with `plots/`, `metrics/`, `logs/`, `predictions/`, `weights/`), or saved cell outputs.

- Read every cell in order, including saved outputs, and every file in the outputs folder, including all metrics, logs, CSV, and JSON. Never execute notebooks.
- One subsection per notebook, in execution order. Per code cell or small group doing one job: what, why, key parameters, and what it produced, quoting exact printed or saved results (shapes, class counts, hyperparameters, per-epoch or per-fold scores, final values).
- Results section: every metric in tables of metric, value, split or fold, and source, including per-class, per-fold, and per-epoch values.
- Embed every output image with a relative path (spaces as `%20`) beside the cell or result that produced it, with a caption on what it shows; unattached images go in results.
- Describe prediction and submission files (contents, shape, columns). List weights and checkpoints with size and purpose, not embedded.
- Interpret only as far as the numbers go. If a notebook has no saved outputs, say so.
