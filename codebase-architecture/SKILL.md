---
name: codebase-architecture
description: "Review, plan, restructure, harden, and clean up codebase architecture: folder layout, module and package boundaries, import direction, layering, shared code, duplication, dead code, test structure, and architecture decision records. Use when the user asks to review or redesign repo structure, modularise or split code, fix circular imports or spaghetti code, deduplicate or remove dead code across modules, organise a monorepo, or make a codebase production ready or maintainable. Not for single-file edits, or for cloud, infrastructure, or distributed system architecture unless it concerns how the code represents it."
---

# Codebase Architecture

The goal is to make common changes obvious, local, safe, and verifiable, not to make the code look architected. Scope is the code itself: directories, modules, imports, boundaries, naming, and tests. Touch infrastructure or product architecture only where it affects code organisation. Treat "production ready" or "bulletproof" as targets that need evidence: verify, and report residual risk instead of claiming perfection.

## Workflow

1. Classify the task: audit, explain, redesign, harden, clean up, deduplicate, document, or implement. Ask only if a wrong guess would make the result unusable.
2. Inspect before advising: file tree, manifests, build config, framework conventions, routing, entry points, generated files, tests, scripts, and docs.
3. Map the current shape: directory responsibilities, entry points, feature, domain, layer, and shared modules, import aliases and direction, public exports versus internals, data access, API clients, state, side effects, integrations, validation, error handling, config and environment access, and test layout.
4. Find problems with file-level evidence: circular imports, unclear ownership, cross-layer calls, `utils` sprawl, duplicate abstractions, oversized modules, mixed concerns, hidden side effects, inconsistent naming, leaked framework details, brittle tests, unstable public APIs, and hard-to-place files.
5. Inventory cleanup: unused files, dead exports, unused dependencies, duplicate modules, types, schemas, and constants, redundant adapters, obsolete compatibility layers, stale docs, commented-out code, committed generated artefacts, and unreachable tests or scripts.
6. Choose the smallest useful target architecture. Keep the existing framework and conventions unless they are the problem.
7. Define enforceable boundaries: allowed imports, public module APIs, folder responsibilities, naming, test placement, and where new code goes.
8. If implementing, work in behaviour-preserving phases: prove current behaviour, remove obvious waste, deduplicate, tighten boundaries, then verify broadly.
9. Write a short ADR only when it will help future contributors.

## Principles

- Optimise for how fast people can navigate. Prefer boring, conventional structure.
- Make boundaries visible in paths, imports, exports, tests, and names.
- Keep dependency flow mostly one-directional, pointing towards stable domain rules and away from volatile UI, framework, transport, or persistence details.
- Code that changes together lives together; code with different reasons to change is separated.
- Keep public APIs small and internal helpers next to their caller.
- Prefer explicit composition over hidden globals, service locators, implicit singletons, and import side effects.
- Keep entry points thin and side effects at clear boundaries: entry points, adapters, controllers, jobs, and handlers. Isolate config, secrets, IO, time, randomness, and network calls so tests can mock them.
- Shared code must be genuinely shared and named by responsibility. No `utils`, `helpers`, or `lib` junk drawers, and no common module for single-use code.
- Deduplicate behaviour, schemas, mappers, validators, constants, components, clients, test helpers, and config only when the shared abstraction has a clear name and stable responsibility. Keep duplication when the copies serve different domains or change for different reasons.
- Add abstraction only under repeated pressure, never one that just renames the framework. Avoid premature package, monorepo, service, plugin, or dependency-injection splits.
- Keep generated files, migrations, schemas, assets, and fixtures apart from hand-written domain code. Keep migrations small, reviewable, or reversible.
- Design for deletion: dead modules, shims, and temporary adapters need a removal plan.

## Boundary Patterns

Match the repository and how its changes flow. If several patterns are used, define where each applies.

- Feature-first: most changes cut across UI, state, API, and tests for one capability.
- Domain-first: strong business concepts that should stay framework-independent.
- Layer-first: the framework already separates routes, services, repositories, schemas, and views cleanly.
- Package-first: monorepos only, when packages have clear ownership, versioning, reuse, or separate builds.

## Cleanup And Deletion

Deletion is a first-class refactor, but it needs evidence.

- Search references with `rg`, language tooling, import graphs, package manager commands, and tests. Dynamic imports, reflection, file-system routing, migrations, generated code, config discovery, and plugin registration can hide references.
- Never delete user work, generated inputs, migrations, assets, fixtures, dynamic entry points, or intentional examples without proof they are unused.
- Delete dead code rather than moving it. Merge near-duplicates that share behaviour and owner.
- Remove unused dependencies with the package manager, never by hand-editing lockfiles.
- Remove compatibility shims once imports are migrated and checks pass.
- Remove stale docs and scripts, and update useful docs after structural changes.

## Production Hardening

When asked for production ready, bulletproof, clean, minimal, or non-spaghetti code, cover:

- Correctness: main workflows, edge cases, validation, error and failure paths, and state transitions.
- Maintainability: fewer files, less duplication, clearer names and responsibilities.
- Reliability: explicit side effects, retries or fallbacks where the code already implies them, and no hidden global state.
- Security: secret handling, unsafe defaults, injection, auth boundaries, dependency risk, and exposed tokens or personal data.
- Operability: logs, errors, config, environment handling, startup, and failure visibility.
- Performance: only hot-path waste shown by code, tests, or profiling.
- Tests: focused tests around moved, merged, or cleaned code.
- Tooling: format, lint, type, unit, integration, build, dependency, and dead-code checks where available.

The pass is done when main paths can be traced from entry point to side effect, every important folder and shared module has one clear responsibility, dead code and duplication found are removed or justified, public exports are intentional, new code has an obvious home, and checks pass (smallest suite first, then broader ones).

## Implementation Rules

- Move a file only when the new location makes future changes clearer and is worth the churn. Never restructure based on names alone.
- Preserve public imports, adding temporary compatibility exports if needed.
- Update imports with tooling, then review the result semantically.
- Keep behaviour unchanged unless the user asked otherwise, and keep unrelated formatting and refactors out.
- Aim for a smaller codebase. Added files or lines must clearly reduce risk or complexity.
- Run available type checks, lint, tests, build, and dependency checks. If checks cannot run, state exactly what is unverified.

## Review Questions

- Can a new contributor find the right file for a change?
- Where would the next feature, bug fix, route, test, schema, or shared component go?
- Are tests close to the code they protect, and are config, constants, types, schemas, fixtures, and generated files placed predictably?
- Can the boundaries be enforced with existing tooling, lint rules, tests, or review rules?

## Output

- Review: one entry per finding with Issue (file or directory references), Impact, Recommendation (smallest practical fix), Scope, and Verification (the check that proves it fixed).
- Redesign or refactor plan: current shape, target structure, boundary rules, migration steps in safe order with checks after each phase, compatibility plan for public imports, generated code, routes, and external callers, cleanup plan, risks, tradeoffs, and what not to change.
- Hardening pass: what was cleaned up, what was merged, what was deliberately left duplicated and why, checks passed, what is unverified, and remaining risks with the next concrete fix.
- ADR headings: Context, Decision, Folder And Module Rules, Consequences, Alternatives Considered, Migration, Validation.
