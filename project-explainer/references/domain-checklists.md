# Domain Checklists

Read the sections that match the repository; most projects match more than one. Each item is explained if present, or noted as absent when a reader would expect it.

## Machine Learning And Data Science

- Task type (classification, regression, segmentation, generation, ranking) and why the problem is framed that way.
- Dataset: source, licence, size, features or modalities, labels and how they were made, class balance, splits, leakage risks, and why this dataset over the alternatives.
- Preprocessing, cleaning, augmentation, and feature engineering, each with its reason.
- Every model and method: the intuition, how it works step by step, why it fits, and the alternatives (simpler baselines and stronger options).
- Every hyperparameter: what it controls, the value used, why, and what changing it would do.
- Training: loss, optimiser, schedule, epochs, batch size, hardware, run time, early stopping, seeds.
- Evaluation: validation scheme, every metric (what it measures, its formula in words, its range, what good looks like here), baselines, per-class and per-fold results, plots and what each shows.
- Error analysis, overfitting signs, fairness, limitations, and what would improve the results.

## Web And Mobile Applications

- Users and the main flows, screen by screen or endpoint by endpoint.
- Frontend: framework, routing, state, styling, accessibility, and why.
- Backend: framework, request lifecycle, every endpoint group, validation, errors, background jobs.
- Data: database choice, schema, relations, migrations, caching.
- Authentication, authorisation, sessions, and security measures.
- External services and APIs, with what happens when they fail.
- Hosting, build, deployment, environments, configuration, and cost.

## Libraries, CLIs, And Developer Tools

- The public API or commands, each with an example and its output.
- Design principles, extension points, error handling, and compatibility promises.
- Packaging, versioning, and distribution.

## Data Pipelines And Infrastructure

- Sources, stages, schedules, and sinks, with data volumes and formats.
- Orchestration, idempotency, retries, monitoring, and failure recovery.
- Infrastructure as code, networking, scaling, and cost.

## LLM And Agent Systems

- Models and providers, prompts, tools, retrieval, memory, and guardrails, each with its reason.
- Evaluation of output quality, cost per request, latency, and failure modes such as hallucination and prompt injection.

## Research Papers And Notebooks

- The research question, hypothesis, contribution, and related work.
- Every experiment, cell group, figure, and table, with what it shows.

## Every Project

- Tech stack: each item's role and why it was chosen.
- Repository layout: what each folder holds.
- Testing, CI, code quality, and documentation.
- History: major changes from `git log` and why they happened.
