# Doc Templates

Every file starts with its H1, then `Purpose: ... Read when: ...` and `Last verified: YYYY-MM-DD.` as in the examples. Omit any section with nothing to say for this repository.

## README.md

Content and depth follow `readme-generator`. It ends with a `## Documentation` table of every other doc that exists: file and the question it answers.

## AGENTS.md

Loaded by most agents in every session, so keep it to what most tasks need, ideally under 60 lines.

```markdown
# Agent Guide

Purpose: rules and commands every agent task in this repository needs. Read when: always.
Last verified: YYYY-MM-DD.

## Commands

Install, run, test (all, and one file), lint, format, type-check, build: one line each, exactly as run.

## Conventions

Rules the code follows that a linter does not enforce: naming, error handling, file placement, test style.

## Gotchas

Non-obvious traps, each as `- **<symptom>**: <cause>. <fix>.`

## Docs

One line per other doc: when to read it.
```

## ARCHITECTURE.md

```markdown
# Architecture

Purpose: how the code is organised and why. Read when: adding a module, moving code, or changing dependencies between parts.
Last verified: YYYY-MM-DD.

## Overview

Runtime model (processes, services, jobs) and the main data flow, with a small diagram if it helps.

## Module Map

Table: module or path, responsibility, public API, may depend on.

## Dependency Rules

Allowed directions and how they are enforced.

## Where New Code Goes

One line per kind of change.

## Decisions

`<decision>: <reason>`, linking `RESEARCH.md` where researched.

## Allowed Duplication

Each exception and its reason.

## Growth Signals

Measurable signs that the next restructuring is due.
```

## DATABASE.md

```markdown
# Database

Purpose: what data is stored and which rules hold. Read when: changing schema, queries, migrations, or data access.
Last verified: YYYY-MM-DD.

## Stores

Table: store, engine and version, what it holds, where it is configured.

## Entities

Table per entity or one table: entity, key, important columns, relations. Point to the schema file as the source of truth instead of copying every column.

## Invariants

Rules the data must always satisfy, and where each is enforced (constraint, code, or both).

## Indexes And Queries

Hot queries and the indexes that serve them.

## Migrations

How to create, apply, and roll back, exactly as run, and the rules (never edit an applied migration).

## Data Lifecycle

Seeding, retention, deletion, backups, personal data handling.
```

## DESIGN.md

```markdown
# Design

Purpose: how the UI looks and behaves. Read when: changing any user-facing UI.
Last verified: YYYY-MM-DD.

## Tokens

Palette with roles and light and dark values; type scale; spacing and grid; breakpoints.

## Components

Inventory with states, and the library each is built on.

## Patterns

Icons, motion rules, copy terminology, layout patterns, the signature idea.

## Decisions

`<decision>: <reason>`, with references and libraries reused.
```

## SECURITY.md

```markdown
# Security

Purpose: how this project is protected and what risk remains. Read when: touching authentication, input handling, secrets, dependencies, CI, or infrastructure.
Last verified: YYYY-MM-DD.

## Reporting

How to report a vulnerability.

## Threat Model

Assets, trust boundaries, entry points, main threats.

## Controls

Scanners, guardrails, and protections in place, and where each lives.

## Findings

Table: ID, severity, CWE, status, location, fix. No exploit details for unfixed findings.

## Residual Risks And Required Actions

What remains, and what the owner must do (rotate credentials, change settings).
```

## RESEARCH.md

One section per topic, newest information merged into the existing section rather than duplicated. Mark superseded findings.

```markdown
# Research

Purpose: dated evidence behind technology and design decisions. Read when: choosing or revisiting a library, service, model, dataset, or approach.

## <Topic> (YYYY-MM-DD)

**Brief:** the decision and its hard constraints.
**Scope:** what was searched, and when.
**Findings:** facts with sources; inferences marked.
**Decision:** Adopt, Adapt, Borrow, or Build, with the reason and alternatives considered.
**Sources:** grouped by type, opened links only.
```

## CONTRIBUTING.md

```markdown
# Contributing

Purpose: how outside contributors propose changes. Read when: preparing a contribution.
Last verified: YYYY-MM-DD.

## Setup

Link `README.md`; add only contributor-specific steps.

## Workflow

Branching, commit format, checks to run, pull request rules, review expectations.
```

## CHANGELOG.md

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format: an `Unreleased` section, then one section per version with date, grouped as Added, Changed, Deprecated, Removed, Fixed, Security.
