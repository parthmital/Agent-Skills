---
name: production-architecture
description: "Re-architects a whole repository to be production ready, scalable, modular, and free of redundancy: restructuring, removing exact, near, and semantic duplicates, splitting monoliths, enforcing boundaries, and a one-command `npm run dev` launcher. Use when the user asks to make a codebase production ready, scalable, modular, or maintainable, restructure or re-architect a repo, deduplicate, split god files, fix circular imports or spaghetti code, organise a monorepo, or set up, fix, or change how the app starts locally. Broad and structural, not surgical; vulnerabilities belong to `security-hardening`."
---

# Production Architecture

## Overview

The scope is the whole repository: moving, merging, splitting, renaming, and deleting anywhere is in scope, but intended behaviour must be preserved and proven. Every run re-checks whether the architecture still fits the repo's size and growth, and migrates it if not.

## When to Use

- Whole-repo restructuring, deduplication, modularisation, or production readiness.
- Setting up or fixing local launch (`npm run dev`, start scripts, first-run setup).
- Not for single-file fixes or security audits (`security-hardening`).

## Process

1. Map: manifests, entry points, runtime model, dependency graph, data stores, tests, CI, docs, change hotspots (`git log --stat`).
2. Decide the architecture that fits now and at the next growth stage; list mismatches with file evidence.
3. Inventory duplicates, monoliths, cycles, boundary leaks, production gaps, scaling limits, and dead code, files, dependencies, and docs. Leave Git-ignored work areas such as `.agent-local/` alone.
4. Design the target: single-responsibility modules with small public APIs, allowed dependency directions, and where new code goes. Keep the language and framework unless they are the problem.
5. Migrate in phases that each leave the repo green. Add characterisation tests before moving uncovered code.
6. Enforce boundaries with tooling (`dependency-cruiser` or `eslint-plugin-boundaries`, `import-linter`, ArchUnit, Nx, Go `internal`) and a clone detector in CI.
7. Write `ARCHITECTURE.md`: module map, dependency rules, where new code goes, decisions with reasons, allowed duplication exceptions, and growth signals for the next pass. Update docs referencing moved paths.

## Zero Redundancy

Every piece of logic, data shape, and config has one home. Run a clone detector (`jscpd`, PMD CPD, `pylint --enable=duplicate-code`) at a low threshold, then search manually for near clones, semantic duplicates (different code, same job), types or schemas repeated across layers or languages (derive from one source), repeated literals, limits, messages, and regexes, duplicated config, Dockerfiles, and CI jobs, repeated components, styles, test setup, and fixtures, several libraries or versions for one job, and docs repeating other docs or code.

Merge into one named abstraction in the lowest module all callers may depend on, parameterise real variation, and delete the copies without forwarding wrappers. Allowed exceptions, each recorded in `ARCHITECTURE.md`: generated code (dedupe its input), applied migrations, vendored code, literal expected values in tests, separately versioned public contracts that cannot share a package or codegen, and Kaggle notebooks, which stay self-contained (shared code defined once per notebook, early).

## Modularity

- One reason to change per file, class, function, and module; split mixed concerns or abstraction levels.
- Small explicit public API per module; internals private.
- Acyclic dependencies pointing from volatile details (UI, transport, persistence, vendors) towards domain rules.
- Thin entry points; side effects (IO, network, time, env, globals) behind interfaces at the edges.
- No `utils`, `helpers`, `common`, or `misc` drawers; name shared code by responsibility.
- Organise feature-first, domain-first, layer-first, or as packages, whichever matches how changes flow.
- Notebooks: one job per cell; move logic into `.py` modules only for non-Kaggle notebooks with a matching package.
- Split into services only on evidence (independent scaling, ownership, fault isolation), but keep modules extractable.

## Production Readiness And Scale

- Config from environment, validated at startup, with an example file.
- Errors handled consistently at boundaries, nothing swallowed, user messages separate from internals.
- Structured logs with correlation IDs; metrics, tracing, and health checks for services.
- Timeouts on external calls, retries with backoff only when idempotent, graceful shutdown, idempotent jobs.
- Versioned migrations, transactions for multi-step writes, indexes for real queries.
- Formatter, linter, type checker, tests, and build runnable with one command and enforced in CI. Pinned runtime, committed lockfile, README setup works from a clean clone.
- Fix only limits the code actually has: stateless handlers, no N+1 or unbounded queries, pagination and batching, background jobs for slow or bursty work, pooling, caching with explicit invalidation, back-pressure, suitable algorithms on hot paths. Adding a feature means adding a module, not editing many files.

## Local Launch

`npm run dev` at the root is the only launcher, cross-platform, via one Node script; delete `start.ps1`, `start.sh`, and similar.

- First run installs everything (Node deps, `.venv` with Python deps, `.env` from the example). Later runs skip setup unless a lockfile hash (Git-ignored stamp) changed or an environment is broken.
- Run Python via the `.venv` interpreter, no activation.
- One titled terminal window per long-running process (frontend, backend, services, workers), else prefixed output in the main terminal.
- The main terminal shows status, URLs, and crashes; Ctrl+C kills every process tree and window.
- Clean logs: summarise install noise, never hide errors. Fail fast on missing runtimes or busy ports.
- Open the browser once the frontend responds, except in CI.

## Rules

- Move and rename with tooling; update every import, config, script, CI file, and doc.
- Delete superseded code in the same phase. Shims only for external consumers of a published API, marked deprecated.
- Change dependencies via the package manager, never by editing lockfiles.
- Never weaken or delete tests to pass; move tests with their code.
- Ask before changing published APIs, public URLs, live database schemas, or deployment topology.

## Common Rationalizations

| Rationalization                                                   | Reality                                               |
| ----------------------------------------------------------------- | ----------------------------------------------------- |
| "These two functions differ slightly, so they are not duplicates" | Parameterise the variation; near clones drift apart.  |
| "I'll keep the old path as a wrapper"                             | Forwarding wrappers are duplication with extra steps. |
| "A `utils` file is fine for now"                                  | Drawers grow into the next monolith.                  |
| "We should split into microservices"                              | Only on evidence; modular code is enough until then.  |

## Red Flags

- A phase that leaves the build or tests red.
- Code moved without characterisation tests.
- Clone detector findings left without a recorded exception.

## Verification

- [ ] All available checks run after each phase; results and anything unverified stated.
- [ ] Report: current shape and misfits with file references, target module map and rules, per-phase moves, merges, splits, and deletions with before and after file and line counts, duplicates removed and exceptions kept.
- [ ] `npm run dev` verified on a fresh and a repeat run, with no leftover processes or ports, and the OS stated.
- [ ] `ARCHITECTURE.md` matches the code.
