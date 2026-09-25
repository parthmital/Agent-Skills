---
name: readme-generator
description: Generate, rewrite, audit, or update a repository README.md by inspecting the codebase and documenting verified setup, scripts, APIs, environment variables, testing, deployment, architecture, troubleshooting, security, and maintenance. For repositories with Kaggle or Jupyter notebooks and downloaded outputs, explains every notebook cell by cell with all metrics and embeds every output image. Use when the user asks to create, write, rewrite, improve, refresh, fix, audit, or update a project README, repository documentation, setup guide, developer onboarding guide, or README quality review.
---

# README Generator

Create or update the repository root `README.md` from verified repository facts.

## Writing Rules

- Simple, beginner-friendly Indian English that is still technical, accurate, and formal. A new developer should understand the project without other help.
- ASCII only: no em or en dashes, smart quotes, emojis, or icons. This includes Mermaid diagrams.
- State only facts found in the repository. Never invent features, commands, metrics, URLs, credentials, or config values.
- Avoid vague claims such as fast, scalable, secure, lightweight, production-ready, highly available, optimised, or easy to use, unless a verified metric supports the claim; then give the metric and its evidence.
- Add badges only when their URLs and values can be verified.
- Valid Markdown: clear heading hierarchy, short paragraphs, ordered steps for procedures, tables for structured data, language-tagged code blocks, relative repository links, and a table of contents with working anchors.
- When updating an existing README, keep accurate, useful project-specific content and remove stale, unverifiable, duplicated, or misleading claims.
- For an audit or review request, report findings and proposed changes without writing to `README.md` unless the user asks.

## Inspect First

Build a fact ledger from files and command output so every claim traces to evidence. Review source code, config, package and dependency files, scripts, environment variable usage, tests, existing docs, API routes, database schemas, migrations, and seeds, deployment and CI or CD files, and Docker, compose, server, and hosting files.

Do not run destructive, deployment, database reset, migration, or seed commands, or commands needing secrets, unless the user explicitly asks. Verify such commands from files and state that they were not executed.

## Depth

A longer README is not a better one. Follow any depth the user asks for; otherwise:

- Small project, script, library, or content repository: title, overview, quick start, usage, repository structure, and only other sections a new developer needs.
- Standard application: add configuration, testing, build, deployment, and troubleshooting as supported.
- Large or multi-service system: the full candidate list, where each section carries real information.
- Notebook repository with downloaded outputs: always the full walkthrough in Notebook Repositories, however long it becomes.

Candidate sections: title, table of contents, quick start, overview, problem statement, goals, key features, use cases, architecture, workflow, technology stack, repository structure, prerequisites, installation, environment configuration, database setup, running, scripts and commands, API documentation, authentication and authorisation, input validation, error handling, logging, testing, code quality checks, build, deployment, CI or CD, security, performance, monitoring and maintenance, troubleshooting, known limitations, contributing, coding standards, licence, and support. Omit sections that do not apply. No empty sections or tables that only say "none found", unless the absence itself helps readers.

## Section Requirements

- Quick start, near the top: the minimum verified steps to install and run locally. For every command, give the exact command, what it does, where to run it, the expected result, and common errors with fixes.
- Technology stack: for each technology, its name, version if known, purpose, where it is used, why it is needed, and how it interacts with the rest of the system.
- Environment variables: a table of name, required or optional, purpose, format, safe example value, default, and security notes. Never expose real passwords, tokens, keys, connection strings, or personal data.
- API documentation, only when endpoints exist: for each, method, route, purpose, auth, headers, path and query parameters, request body, validation rules, success and error responses, status codes, and example request and response, all verified from code.
- Repository structure: an ASCII tree, with the purpose of every important directory and file.
- Diagrams: Mermaid only when the repository holds enough information for an accurate one, such as architecture, request flow, auth flow, database relationships, or deployment.
- Troubleshooting: a table of problem, likely cause, diagnostic command, and resolution.
- Metrics, only when they help readers understand or operate the project: verifiable counts and limits such as features, modules, endpoints, models, env vars, scripts, tests, coverage, build time, bundle size, runtime versions, ports, timeouts, retries, and pagination, file size, or rate limits. Give each metric's name, value, source file or command, and notes. Never estimate. If an important metric cannot be verified, write exactly: `Not measured in the current repository.`

## Notebook Repositories

Apply when the repository has Kaggle or Jupyter notebooks (`.ipynb`) with downloaded run outputs. Outputs usually sit in an `outputs/` folder or an extracted `outputs.zip`, often with `plots/`, `metrics/`, `logs/`, `predictions/`, and `weights/` subfolders. Saved cell outputs inside the notebook also count.

- Read every notebook cell in order, markdown and code, including saved outputs. List every file in the outputs folder and read every metrics, log, CSV, and JSON file, however many there are. Never execute the notebooks.
- Explain each notebook end to end in its own subsection, in execution order. For each code cell, or small group of cells doing one job, explain what it does, why, its key parameters and choices, and what it produced. Quote the exact results it printed or saved: dataset shapes, class counts, hyperparameters, training progress, per-epoch or per-fold scores, and final values.
- Add a results section with every metric in tables: metric, value, split or fold, and source file or cell. Include per-class, per-fold, and per-epoch values, not only headline numbers.
- Embed every image in the outputs folder with a relative path, such as `![Confusion matrix](outputs/plots/confusion_matrix.png)`, percent-encoding spaces as `%20`. Place each image beside the cell or result that produced it, with a caption on what it shows and what it says about the results. Unattached images go in the results section.
- Describe prediction and submission files: contents, shape, and columns. List weight and checkpoint files with their size and purpose, without embedding them.
- Interpret only as far as the numbers support, such as which model or fold scored best. Do not claim causes, generalisation, or real-world performance the outputs do not show. If a notebook has no saved outputs or matching output files, say so instead of describing results.

## Final Validation

Before writing, verify every command, file path, port, environment variable, API route, dependency, version, and metric against the repository. Confirm no secrets are exposed, all characters are ASCII, the Markdown is valid, and no unsupported claim was added. For notebook repositories, confirm every cell is covered, every output image is embedded with a working relative path, and every output metric is reported.

Unless the user asked for an audit only, write the result to `README.md` in the repository root.
