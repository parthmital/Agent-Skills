---
name: project-docs
description: Writes, rewrites, audits, and updates a repository's documentation set (README.md, AGENTS.md, ARCHITECTURE.md, DATABASE.md, DESIGN.md, SECURITY.md, RESEARCH.md, CONTRIBUTING.md, CHANGELOG.md) from verified codebase facts, in one compact, agent-first format with one purpose per file and no duplication. Notebook repositories get a cell-by-cell README walkthrough with every metric and output image. Use when the user asks to create, improve, standardise, audit, deduplicate, or update a README, setup or onboarding guide, or any of these files, and whenever another skill writes one of them.
---

# Project Docs

## Overview

Agents and new developers read these docs at the start of tasks, so every line costs context and every wrong line costs a mistake. Each file answers one question, each fact lives in exactly one file and is verified against the repository, and a reader can tell from a file's first lines whether it needs the rest.

## When to Use

- Creating, updating, or auditing `README.md` or any file in the map below, or the whole set. For an audit, report the findings, then fix them.
- Other skills that write a file in the map follow its template here. Their own steps decide the content.

## Documentation Map

| File              | Answers                                     | Create when                              | Content owner             |
| ----------------- | ------------------------------------------- | ---------------------------------------- | ------------------------- |
| `README.md`       | What is this, and how do I run it?          | Always                                   | `project-docs`            |
| `AGENTS.md`       | What must an agent know in every task here? | Always                                   | `project-docs`            |
| `ARCHITECTURE.md` | How is the code organised, and why?         | More than a handful of modules           | `production-architecture` |
| `DATABASE.md`     | What data is stored, and what rules hold?   | A database, schema, or persistent store  | `project-docs`            |
| `DESIGN.md`       | How does the UI look and behave?            | A user-facing UI                         | `frontend-design`         |
| `SECURITY.md`     | How is it protected, and what is at risk?   | A security review ran, or a public repo  | `security-hardening`      |
| `RESEARCH.md`     | What was evaluated before choosing?         | Any researched decision                  | `internet-research`       |
| `CONTRIBUTING.md` | How do outsiders contribute?                | The repo accepts outside contributions   | `project-docs`            |
| `CHANGELOG.md`    | What changed in each release?               | The project publishes versioned releases | `project-docs`            |

Create a file only when it has real content for this repository. Never create stubs.

## Format Rules

- First lines after the H1: `Purpose: <the question it answers>. Read when: <tasks that need it>.`, then `Last verified: YYYY-MM-DD.` (README excepted: it opens with a one-paragraph overview.)
- Section names from [references/doc-templates.md](references/doc-templates.md), so agents can jump to an anchor. Omit sections with nothing to say.
- Write what the code cannot tell quickly: rules, invariants, reasons, boundaries, gotchas, and exact commands. Never list what `ls`, a manifest, or a quick read of the code shows.
- Bullets and tables over prose, one fact per bullet. Repo-relative paths and commands in backticks, exactly as run.
- One home per fact. Elsewhere, link to it (`ARCHITECTURE.md#module-map`). `README.md` ends with the index of the other docs.
- Decisions inline as `<decision>: <reason>`. A researched decision links its `RESEARCH.md` section.
- Keep each file under about 200 lines (README excepted when its depth needs more). Split a detailed topic into `docs/<topic>.md` and link it with a `Read when` line.
- Simple, formal Indian English. ASCII only, including Mermaid: no em or en dashes, semicolons, smart quotes, emojis, or icons. No marketing words (fast, scalable, secure, seamless, production-ready) unless a verified metric supports them. No secrets or personal data.

## Process

1. **Fact ledger.** Build it from source, config, manifests, scripts, environment variable usage, tests, existing docs, routes, schemas, migrations, CI, Docker, and hosting files. Each fact carries its `path:line`. For a large repository, `subagent-delegation` decides whether `research-worker`s gather parts of the ledger.
2. **Inventory existing docs**, including `docs/`, wiki folders, and long code comments that act as docs. Map every section to one file in the map, and mark duplicates, contradictions, stale facts (checked against the ledger), and misplaced content.
3. **Never run** destructive, deployment, database reset, migration, or seed commands, or commands needing secrets, unless asked. Verify them from files and say they were not executed. Do run safe commands the docs promise (install, test, build) when the environment allows.
4. **Write** to the templates. Keep accurate project-specific content, delete stale, duplicated, and unverifiable text, fold orphan docs into their home, and link instead of restating. For a file another skill owns, run that skill when its content needs new work (a fresh security audit), and fix only the format here otherwise.
5. **README depth**: follow any depth the user asks for, else match the project:
   - Small project, script, library, or content repo: overview, quick start, usage, and only what a new developer needs.
   - Standard application: add configuration, environment variables, testing, build, deployment, and troubleshooting as the ledger supports.
   - Large or multi-service system: every README section in the templates that carries real information.
   - Notebook repository with saved outputs or a downloaded outputs folder: always the full walkthrough in [references/notebook-walkthrough.md](references/notebook-walkthrough.md). Read it first.
6. **Links**: update the README documentation index and every link affected by moved sections.
7. **Check**: run Verification, recheck each command, path, port, variable, and version against the ledger, and fix anything that fails.

## Examples

Bad (README quick start, unverified and vague):

```markdown
## Getting Started

Install the dependencies and run the app. It is fast and easy to set up!
```

Good (every command checked against `package.json` and `.env.example`):

```markdown
## Quick Start

1. Install Node.js 22 (pinned in `.nvmrc`), then run `npm ci` in the repository root.
2. Copy `.env.example` to `.env` and set `DATABASE_URL` (see Environment Variables).
3. Run `npm run dev`. The app serves on `http://localhost:5173`. If port 5173 is taken, stop the other process or set `PORT`.
```

Bad (`ARCHITECTURE.md` restating the README and listing files):

```markdown
The project uses React and Express. Files: src/index.ts, src/app.ts, src/routes/users.ts ...
```

Good:

```markdown
## Dependency Rules

- `src/domain/` imports nothing from `src/http/` or `src/db/`: enforced by `dependency-cruiser` in `npm run lint`.
```

## Common Rationalisations

| Rationalisation                      | Reality                                                          |
| ------------------------------------ | ---------------------------------------------------------------- |
| "Every README needs all sections"    | Empty or padded sections hide the useful ones.                   |
| "This command obviously works"       | Verify it against scripts and config, or say it was not run.     |
| "Repeating it in two docs is safer"  | The copies drift, and readers pay to read both.                  |
| "A full file inventory helps agents" | Agents can list files. Document the rules they cannot see.       |
| "Headline metrics are enough"        | Notebook readers need per-fold, per-class, and per-epoch values. |

## Red Flags

- A command, port, path, or environment variable not found in the repository.
- The same command, rule, or explanation in two files.
- A doc without its `Purpose` and `Read when` line, or describing code that no longer exists.
- Non-ASCII characters, em dashes, or semicolons.
- Output images that exist but are not embedded in a notebook README.

## Verification

- [ ] Every command, path, port, environment variable, route, dependency, version, and metric checked against the repository.
- [ ] Every doc follows its template and the Format Rules. No fact appears in two files, and links and anchors resolve.
- [ ] `README.md` indexes every other doc that exists.
- [ ] No secrets, no unsupported claims, valid Markdown with language-tagged code blocks.
- [ ] Notebook repos: every cell covered, every output image embedded with a working relative path, every metric reported.
