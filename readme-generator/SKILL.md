---
name: readme-generator
description: Generates, rewrites, audits, or updates a repository README.md from verified codebase facts, covering setup, scripts, APIs, environment variables, testing, deployment, architecture, and troubleshooting; notebook repositories with downloaded outputs get a cell-by-cell walkthrough with every metric and output image. Use when the user asks to create, write, rewrite, improve, refresh, fix, audit, or update a project README, repository documentation, setup guide, or developer onboarding guide.
---

# README Generator

## Overview

Write the root `README.md` so a new developer understands and runs the project without other help, with every claim traceable to the repository.

## When to Use

- Creating, updating, or auditing a README or onboarding guide.
- For an audit, report findings and proposed changes without writing to `README.md` unless asked.

## Process

1. Build a fact ledger from source, config, dependency files, scripts, env var usage, tests, existing docs, API routes, schemas, migrations, seeds, CI/CD, Docker, and hosting files.
2. Never run destructive, deployment, database reset, migration, or seed commands, or commands needing secrets, unless asked. Verify them from files and say they were not executed.
3. Choose depth (below) and write. When updating, keep accurate project-specific content and remove stale, unverifiable, duplicated, or misleading claims.
4. Run Verification, then write `README.md` at the root.

## Depth

Longer is not better. Follow any depth the user asks for; otherwise:

- Small project, script, library, or content repo: title, overview, quick start, usage, structure, and only other sections a new developer needs.
- Standard application: add configuration, testing, build, deployment, troubleshooting as supported.
- Large or multi-service system: all candidate sections that carry real information.
- Notebook repository with outputs: always the full walkthrough below.

Candidates: table of contents, quick start, overview, problem, goals, features, use cases, architecture, workflow, tech stack, structure, prerequisites, installation, environment, database setup, running, scripts, API, auth, validation, error handling, logging, testing, code quality, build, deployment, CI/CD, security, performance, monitoring, troubleshooting, known limitations, contributing, coding standards, licence, support. No empty sections or "none found" tables unless the absence helps readers.

## Writing Rules

- Simple, beginner-friendly Indian English that is still technical and formal.
- ASCII only, including Mermaid: no em or en dashes, smart quotes, emojis, or icons.
- Never invent features, commands, metrics, URLs, credentials, or config values. No vague claims (fast, scalable, secure, lightweight, production-ready, optimised, easy) unless a verified metric supports them, given with its evidence. Badges only when verifiable.
- Valid Markdown: clear heading hierarchy, short paragraphs, ordered steps, tables for structured data, language-tagged code blocks, relative links, working table-of-contents anchors.
- Never duplicate other docs: summarise `ARCHITECTURE.md`, `DESIGN.md`, `RESEARCH.md`, `SECURITY.md`, `CONTRIBUTING.md`, and similar in a line or two and link them.

## Section Requirements

- Quick start, near the top: minimum verified steps; for each command, what it does, where to run it, expected result, and common errors with fixes.
- Tech stack: name, version if known, purpose, where used, why needed, how it interacts with the rest.
- Environment variables table: name, required or optional, purpose, format, safe example, default, security notes. Never real secrets or personal data.
- API, only when endpoints exist, verified from code: method, route, purpose, auth, headers, parameters, body, validation, responses, status codes, example request and response.
- Structure: ASCII tree with the purpose of every important directory and file.
- Mermaid diagrams only when the repo holds enough information for an accurate one.
- Troubleshooting table: problem, likely cause, diagnostic command, resolution.
- Metrics only when they help readers: verifiable counts and limits with name, value, source file or command, notes. Never estimate; for an important unverifiable metric write exactly `Not measured in the current repository.`

## Notebook Repositories

Applies when the repo has `.ipynb` files with downloaded outputs (usually `outputs/` or an extracted `outputs.zip` with `plots/`, `metrics/`, `logs/`, `predictions/`, `weights/`), or saved cell outputs.

- Read every cell in order, including saved outputs, and every file in the outputs folder, including all metrics, logs, CSV, and JSON. Never execute notebooks.
- One subsection per notebook, in execution order. Per code cell or small group doing one job: what, why, key parameters, and what it produced, quoting exact printed or saved results (shapes, class counts, hyperparameters, per-epoch or per-fold scores, final values).
- Results section: every metric in tables of metric, value, split or fold, and source, including per-class, per-fold, and per-epoch values.
- Embed every output image with a relative path (spaces as `%20`) beside the cell or result that produced it, with a caption on what it shows; unattached images go in results.
- Describe prediction and submission files (contents, shape, columns). List weights and checkpoints with size and purpose, not embedded.
- Interpret only as far as the numbers go. If a notebook has no saved outputs, say so.

## Common Rationalizations

| Rationalization                   | Reality                                                          |
| --------------------------------- | ---------------------------------------------------------------- |
| "Every README needs all sections" | Empty or padded sections hide the useful ones.                   |
| "This command obviously works"    | Verify it against scripts and config, or say it was not run.     |
| "Headline metrics are enough"     | Notebook readers need per-fold, per-class, and per-epoch values. |

## Red Flags

- A command, port, or env var not found in the repo.
- Non-ASCII characters.
- Output images that exist but are not embedded.

## Verification

- [ ] Every command, path, port, env var, route, dependency, version, and metric checked against the repo.
- [ ] No secrets, ASCII only, valid Markdown, no unsupported claims.
- [ ] Notebook repos: every cell covered, every output image embedded with a working relative path, every output metric reported.
