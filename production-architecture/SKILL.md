---
name: production-architecture
description: "Re-architect an entire repository to be production ready, scalable, fully modular, and free of all redundancy: whole-repo restructuring, removing every exact, near, and semantic duplicate, splitting monolithic files, classes, and functions, enforcing boundaries, and evolving the architecture as the repo grows. Use when the user asks to make a codebase production ready, scalable, modular, or maintainable, restructure or re-architect a repo, deduplicate or remove redundancy, split a monolith or god files, fix circular imports or spaghetti code, or organise a monorepo. Broad and structural, not surgical. Vulnerabilities belong to security-hardening."
---

# Production Architecture

Make the whole repository production ready, scalable, modular, and redundancy-free. The task's scope is the whole repository: moving, merging, splitting, renaming, and deleting anywhere in it are in scope. Intended behaviour must be preserved and proven. Every run re-evaluates whether the current architecture still fits the repo's size and growth, and migrates it if not.

## Workflow

1. Map the repo: manifests, entry points, runtime model, dependency graph, data stores, tests, CI, docs, and change hotspots (`git log --stat`).
2. Decide the architecture that fits now and at the next growth stage; list mismatches with file evidence.
3. Inventory duplicates, monoliths, cycles and boundary leaks, production gaps, scaling limits, and dead code, files, dependencies, and docs. Leave Git-ignored work areas such as `.agent-local/` alone.
4. Design the target: modules with one responsibility and a small public API, allowed dependency directions, and where new code goes. Keep the language and framework unless they are the problem.
5. Migrate in phases that each leave the repo green. Add characterisation tests before moving uncovered code.
6. Enforce boundaries with tooling: `dependency-cruiser` or `eslint-plugin-boundaries`, `import-linter`, ArchUnit, Nx boundaries, Go `internal`, and a clone detector in CI.
7. Write `ARCHITECTURE.md`: module map, dependency rules, where new code goes, decisions with reasons, allowed duplication exceptions, and growth signals that trigger the next pass. Update docs referencing moved paths.

## Zero Redundancy

Every piece of logic, data shape, and config has exactly one home. Run a clone detector (`jscpd`, PMD CPD, `pylint --enable=duplicate-code`) at a low threshold, then search manually for:

- Near clones with renames, reordering, or small variations.
- Semantic duplicates: different code doing the same job.
- The same type, schema, or model across layers or languages; derive from one source.
- Repeated literals, limits, messages, and regexes.
- Duplicated config, Dockerfiles, and CI jobs; use shared configs and reusable workflows.
- Repeated components, styles, test setup, fixtures, and mocks.
- Several libraries for one job, or several versions of one package.
- Docs repeating other docs or the code.

Merge into one named abstraction in the lowest module all callers may depend on, parameterise real variation, and delete the copies without leaving forwarding wrappers. Only allowed exceptions, each recorded in `ARCHITECTURE.md`: generated code (dedupe its input), applied migrations, vendored code, literal expected values in tests, separately versioned public contracts that cannot share a package or codegen, and code shared between Kaggle notebooks, which must stay self-contained (define shared code once per notebook, in an early cell).

## Modularity

- Every file, class, function, and module has one reason to change. Split anything mixing concerns or abstraction levels.
- Small explicit public API per module; internals private.
- Dependencies acyclic and pointing from volatile details (UI, transport, persistence, vendors) towards domain rules.
- Thin entry points; side effects (IO, network, time, env, globals) behind interfaces at the edges.
- No `utils`, `helpers`, `common`, or `misc` drawers; name shared code by responsibility.
- Organise feature-first, domain-first, layer-first, or as monorepo packages, whichever matches how changes flow.
- Notebooks: one job per cell. Move logic into `.py` modules only for non-Kaggle notebooks with a matching repository package.
- Modular code, not necessarily separate deployments: split into services only on evidence (independent scaling, ownership, fault isolation), but keep modules extractable.

## Production Readiness

- Config from environment, validated at startup, with an example file.
- Consistent error handling at boundaries; nothing swallowed; user messages separate from internals.
- Structured logs with correlation IDs; metrics, tracing, and health checks for services.
- Timeouts on external calls, retries with backoff only when idempotent, graceful shutdown, idempotent jobs.
- Versioned migrations, transactions for multi-step writes, indexes for real queries.
- Formatter, linter, type checker, tests, and build runnable with one command and enforced in CI.
- Pinned runtime, committed lockfile, reproducible build; README setup works from a clean clone.

## Scalability

Fix limits the code actually has; add no infrastructure the workload does not need.

- Stateless handlers; state in stores, not process memory.
- No N+1 or unbounded queries; paginate and batch.
- Slow or bursty work in background jobs where needed.
- Connection pooling, caching with explicit invalidation, back-pressure.
- Suitable algorithms on hot paths.
- Adding a feature means adding a module, not editing many files.

## Rules

- Move and rename with tooling; update every import, config, script, CI file, and doc.
- Delete superseded code in the same phase. Keep shims only for external consumers of a published API, marked deprecated.
- Change dependencies via the package manager, never by editing lockfiles.
- Never weaken or delete tests to pass; move tests with their code.
- Run all available checks after each phase; state what is unverified.
- Ask before changing published APIs, public URLs, live database schemas, or deployment topology.

## Output

- Current shape and what no longer fits, with file references.
- Target module map and dependency rules.
- Per phase: what moved, merged, split, and deleted, with before and after file and line counts.
- Duplicates removed and exceptions kept, with reasons.
- Checks run, results, and what is unverified.
