---
name: project-docs
description: Defines and maintains the standard documentation set of a repository (README.md, AGENTS.md, ARCHITECTURE.md, DATABASE.md, DESIGN.md, SECURITY.md, RESEARCH.md, CONTRIBUTING.md, CHANGELOG.md) in one compact, agent-first format with one purpose per file and no duplication, and writes AGENTS.md, DATABASE.md, CONTRIBUTING.md, and CHANGELOG.md itself. Use when the user asks to write, standardise, audit, restructure, deduplicate, or update project documentation or any of these files, and whenever another skill writes one of them.
---

# Project Docs

## Overview

Agents read these docs at the start of tasks, so every line costs context in every session that opens the file. Each file answers one question, each fact lives in exactly one file, and an agent can tell from a file's first lines whether it needs the rest.

## When to Use

- Creating, auditing, or standardising any file in the map below, or the whole set.
- Other skills that write a file in the map follow its template here; their own steps decide the content.
- Not for `EXPLAINER.md`, which is for humans (`project-explainer`).

## Documentation Map

| File              | Answers                                     | Create when                              | Owner                         |
| ----------------- | ------------------------------------------- | ---------------------------------------- | ----------------------------- |
| `README.md`       | What is this, and how do I run it?          | Always                                   | `readme-generator`            |
| `AGENTS.md`       | What must an agent know in every task here? | Always                                   | `project-docs`                |
| `ARCHITECTURE.md` | How is the code organised, and why?         | More than a handful of modules           | `production-architecture`     |
| `DATABASE.md`     | What data is stored, and what rules hold?   | A database, schema, or persistent store  | `project-docs`                |
| `DESIGN.md`       | How does the UI look and behave?            | A user-facing UI                         | `frontend-design`             |
| `SECURITY.md`     | How is it protected, and what is at risk?   | A security review ran, or a public repo  | `security-hardening`          |
| `RESEARCH.md`     | What was evaluated before choosing?         | Any researched decision                  | `research-driven-development` |
| `CONTRIBUTING.md` | How do outsiders contribute?                | The repo accepts outside contributions   | `project-docs`                |
| `CHANGELOG.md`    | What changed in each release?               | The project publishes versioned releases | `project-docs`                |

Create a file only when it has real content for this repository. Never create stubs.

## Format Rules

- First lines after the H1: `Purpose: <the question it answers>. Read when: <tasks that need it>.`, then `Last verified: YYYY-MM-DD.`
- Use the section names from [references/doc-templates.md](references/doc-templates.md) so agents can jump to an anchor. Omit sections with nothing to say.
- Write what the code cannot tell quickly: rules, invariants, reasons, boundaries, gotchas, and exact commands. Do not list what `ls`, a manifest, or a quick read of the code shows.
- Bullets and tables, not prose. One fact per bullet. Repo-relative paths and commands in backticks, exactly as run.
- One home per fact. Elsewhere, link to it (`ARCHITECTURE.md#module-map`) instead of restating it. `README.md` holds the index of the other docs.
- Decisions inline as `<decision>: <reason>`; a researched decision links its `RESEARCH.md` section.
- Keep each file under about 200 lines. When a file outgrows that, move a detailed topic into `docs/<topic>.md` and link it with a `Read when` line.
- ASCII only, no em dashes, no marketing words, no secrets or personal data.

## Process

1. Inventory existing docs, including `docs/`, wiki-style folders, and long code comments that act as docs.
2. Map every section of every doc to one file in the map. Mark duplicates, contradictions, stale facts (check them against the code), and content that belongs in another file.
3. Rewrite to the templates: keep each fact once in its home, link from elsewhere, delete stale and duplicate text, and fold orphan docs into their home or into `docs/<topic>.md`.
4. Write the files this skill owns, using the templates. For a file another skill owns, run that skill when its content needs new work, such as a fresh security audit, and fix only the format here otherwise.
5. Update `README.md`'s documentation index and every link affected by moved sections.

## Common Rationalizations

| Rationalization                           | Reality                                                               |
| ----------------------------------------- | --------------------------------------------------------------------- |
| "Repeating it in two docs is safer"       | The copies drift, and agents pay to read both.                        |
| "A full file inventory helps agents"      | Agents can list files themselves; document the rules they cannot see. |
| "Add every doc so the set looks complete" | Empty or stub docs waste a read and imply facts that do not exist.    |

## Red Flags

- The same command, rule, or explanation in two files.
- A doc without its `Purpose` and `Read when` line.
- A doc that describes code that no longer exists.
- A file over about 200 lines with no `docs/` split.

## Verification

- [ ] Every doc follows its template and the Format Rules.
- [ ] No fact appears in two files; links resolve.
- [ ] Every command, path, and name in the docs was checked against the repository.
- [ ] `README.md` indexes every doc that exists.
