---
name: readme-generator
description: Generates, rewrites, audits, or updates a repository README.md from verified codebase facts, covering setup, scripts, APIs, environment variables, testing, deployment, architecture, and troubleshooting; notebook repositories with downloaded outputs get a cell-by-cell walkthrough with every metric and output image. Use when the user asks to create, write, rewrite, improve, refresh, fix, audit, or update a project README, repository documentation, setup guide, or developer onboarding guide.
---

# README Generator

## Overview

Write the root `README.md` so a new developer understands and runs the project without other help, with every claim traceable to the repository.

## When to Use

- Creating, updating, or auditing a README or onboarding guide.
- For an audit, report the findings, then fix them in `README.md`.

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
- Notebook repository with outputs (`.ipynb` files with saved outputs or a downloaded outputs folder): always the full walkthrough in [references/notebook-walkthrough.md](references/notebook-walkthrough.md); read it first.

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
