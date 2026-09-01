---
name: codebase-architecture
description: "Analyse, plan, critique, document, harden, clean up, deduplicate, and improve codebase architecture using best practices for repository structure, folder layout, module boundaries, package boundaries, import direction, layering, feature organisation, shared code, dependency flow, naming, test structure, production readiness, refactor plans, and architecture decision records for code organisation. Use automatically when the user asks to review, redesign, clean up, harden, make production ready, bulletproof, restructure, modularise, split, merge, organise, simplify, deduplicate, remove dead code, document, diagram, or reason about a codebase, repo architecture, folder structure, module boundaries, dependency structure, circular imports, layering, monorepo packages, spaghetti code, or maintainability. Do not use for broad cloud, infrastructure, or distributed system architecture unless the request is explicitly about how that architecture is represented in the codebase."
---

# Codebase Architecture

Use this skill to make a repository easier to understand, change, test, and maintain. Focus on the architecture of the code itself: directories, modules, packages, imports, boundaries, naming, ownership, and tests.

Do not drift into broad infrastructure or product architecture unless it directly affects code organisation.

The goal is not to make the codebase look architected. The goal is to make common changes obvious, local, safe, reusable, minimal, and verifiable.

Treat "production ready" and "bulletproof" as engineering targets that require evidence. Do not claim perfection. Instead, drive the codebase as far as the repository context allows, verify aggressively, and report residual risks.

## Workflow

1. Establish the task: audit, explain, redesign, harden, clean up, deduplicate, document, or implement a codebase architecture change. Ask only when a wrong assumption would make the result unusable.
2. Inspect the repository before advising: file tree, package manifests, build config, framework conventions, routing, runtime entry points, generated files, tests, scripts, and existing docs.
3. Map the current shape:
   - top-level directories and their responsibilities
   - application entry points
   - feature, domain, layer, and shared modules
   - import aliases and dependency direction
   - public exports and private implementation files
   - data access, API clients, state management, side effects, and integration code
   - validation, error handling, configuration, and environment access
   - test layout and fixtures
4. Identify architecture problems with evidence: circular imports, unclear ownership, cross-layer calls, generic `utils` sprawl, duplicate abstractions, oversized modules, mixed concerns, hidden side effects, inconsistent naming, leaked framework details, brittle tests, unstable public APIs, or files that are hard to place.
5. Inventory cleanup opportunities: unused files, dead exports, unused dependencies, duplicate modules, duplicate types, duplicate schemas, repeated constants, redundant adapters, obsolete compatibility layers, stale docs, commented-out code, generated artifacts committed by mistake, and unreachable tests or scripts.
6. Choose the smallest useful target architecture. Prefer the repository's existing framework and conventions unless they are the source of the problem.
7. Define enforceable boundaries: allowed imports, public module APIs, folder responsibilities, naming rules, test placement, and where new code should go.
8. If implementation is requested, make changes in safe phases: prove current behaviour, clean obvious waste, deduplicate repeated logic, tighten boundaries, then run broad verification.
9. Document the decision only when it will help future contributors. Use a short ADR or architecture note rather than a long essay.

## Principles

- Optimise for code people can navigate quickly.
- Prefer boring, conventional repo structures over clever architecture.
- Make boundaries visible in paths, imports, public exports, tests, and names.
- Keep dependency flow simple and mostly one-directional.
- Prefer high cohesion and low coupling. Code that changes together should live together; code with different reasons to change should be separated.
- Make dependencies point towards stable policy and domain rules, not towards volatile UI, framework, transport, or persistence details.
- Keep public APIs small. Export only what other modules should use, and hide internal helpers near their caller.
- Prefer explicit composition over hidden globals, service locators, implicit singletons, and action-at-a-distance imports.
- Keep side effects at clear boundaries: entry points, adapters, controllers, jobs, command handlers, or infrastructure-facing modules.
- Keep entry points thin. Put business rules, data transforms, validation, and side effects in predictable modules.
- Keep shared code genuinely shared. Do not create a common module for code used once.
- Prefer maximum practical reuse with minimum code. Deduplicate repeated behaviour, schemas, mappers, validators, constants, components, API clients, test helpers, and configuration only when the shared abstraction has a clear name and stable responsibility.
- Avoid `utils`, `helpers`, and `lib` junk drawers. Name modules by responsibility.
- Prefer cohesive feature or domain folders when changes usually cut through UI, state, API, and tests together.
- Prefer layered folders when the framework or codebase already uses layers clearly and consistently.
- Avoid premature package splits, monorepo moves, service splits, plugin systems, or dependency-injection frameworks.
- Add abstraction only after there is repeated, meaningful pressure. Avoid abstractions that merely rename the underlying framework.
- Keep configuration, secrets access, IO, time, randomness, and network calls easy to mock or isolate in tests.
- Design for deletion. Dead modules, duplicate paths, obsolete compatibility exports, and temporary adapters should have a removal plan.
- Remove useless code, files, dependencies, docs, scripts, and tests only after verifying they are not referenced, required by tooling, used by runtime discovery, or intentionally kept as examples.
- Treat generated files, migrations, schemas, assets, and fixtures as architecture inputs, but do not mix them with hand-written domain code.
- Migrations should be reversible or easy to review in small steps.

## Boundary Patterns

Choose the pattern that matches the existing repo and change behaviour:

- Feature-first: use when most changes affect one product capability across UI, state, API calls, and tests.
- Domain-first: use when the project has strong business concepts that should stay independent of frameworks.
- Layer-first: use when the framework already separates routes, services, repositories, schemas, and views cleanly.
- Package-first: use in monorepos only when packages have clear ownership, versioning, reuse, or independent build needs.

Do not mix patterns casually. If a repo uses more than one pattern, define where each pattern applies.

## Production Hardening

When the user asks to make a codebase production ready, bulletproof, clean, minimal, or non-spaghetti, perform a full codebase hardening pass:

- Correctness: verify main workflows, edge cases, input validation, error handling, failure paths, and state transitions.
- Maintainability: reduce unnecessary files, duplicate logic, confusing names, mixed responsibilities, and hard-to-place code.
- Reliability: make side effects explicit, handle retries or fallbacks where the code already implies them, and avoid hidden global state.
- Security: check secret handling, unsafe defaults, injection risk, auth boundaries, dependency risk, and accidental exposure of tokens or personal data.
- Operability: verify logs, errors, config, environment handling, startup behaviour, and failure visibility at the code level.
- Performance: remove obvious inefficient duplication or hot-path waste when evidenced by code, tests, or profiling output.
- Tests: preserve or add focused tests around moved, merged, or cleaned code. Do not rely on "looks right" after architecture changes.
- Tooling: run format, lint, type, unit, integration, build, dependency, and dead-code checks where available.

## Cleanup And Deduplication

Use evidence before deleting or merging:

- Search references with `rg`, language-aware tooling, import graphs, package manager commands, and tests.
- Treat dynamic imports, reflection, framework file-system routing, migrations, generated code, config discovery, and plugin registration as possible hidden references.
- Prefer deleting dead code over moving it.
- Prefer merging near-duplicate modules when their behaviour and ownership are the same.
- Prefer keeping duplication when two similar blocks serve different domains, have different change reasons, or would require a vague abstraction.
- Replace repeated logic with a small shared function, type, schema, hook, component, fixture, or adapter only when its responsibility is obvious.
- Remove compatibility shims after imports are migrated and checks pass.
- Remove unused dependencies from manifests and lockfiles with the package manager, not by editing lockfiles manually.
- Remove stale docs and scripts when they describe flows that no longer exist. Update useful docs after structural changes.

## Quality Bar

A hardening pass is not complete until:

- The main code paths are understandable from entry point to side effect.
- Every important folder and shared module has a clear responsibility.
- Dead code and unused dependencies found during the pass are removed or explicitly justified.
- Meaningful duplication is deduplicated without creating vague catch-all abstractions.
- Public exports are intentional.
- New code has an obvious home.
- The smallest useful test suite passes, then broader checks pass where available.
- Remaining risks, unverified paths, and deferred cleanups are named directly.

## Review Checklist

Check:

- Can a new contributor find the right file for a change?
- Does each directory have one clear responsibility?
- Are imports flowing in an understandable direction?
- Are there circular dependencies or hidden runtime coupling?
- Are domain rules separated from transport, UI, storage, and framework glue where useful?
- Are volatile details depending on stable rules, rather than stable rules importing volatile details?
- Are public exports intentional and small?
- Is shared code actually reused and named by purpose?
- Are duplicate modules, types, schemas, constants, components, fixtures, and scripts merged or justified?
- Are dead files, unused exports, stale docs, and unused dependencies removed or justified?
- Are tests close enough to the code they protect?
- Are config, constants, types, schemas, fixtures, and generated files placed predictably?
- Are file moves worth the churn they create?
- Can boundaries be enforced with existing tooling, lint rules, tests, or simple review rules?
- Is there a clear place for the next likely feature, bug fix, API route, test, schema, and shared component?

## Output

For a codebase architecture review, lead with findings:

- Issue: concrete architecture problem with file or directory references.
- Impact: why it makes changes harder, riskier, slower, or less testable.
- Recommendation: the smallest practical fix.
- Scope: files or folders likely affected.
- Verification: check, test, lint rule, or review rule that would prove the issue is fixed.

For a redesign or refactor plan, provide:

- Current shape summary.
- Target structure.
- Boundary rules.
- Migration steps in a safe order.
- Tests and checks to run after each phase.
- Compatibility plan for public imports, generated code, routes, and external callers.
- Cleanup plan for dead code, duplicate logic, unused dependencies, stale docs, and obsolete scripts.
- Risks, tradeoffs, and what not to change.

For a production-readiness hardening pass, provide:

- What was cleaned up.
- What was deduplicated or merged.
- What was deliberately left duplicated and why.
- What checks passed.
- What could not be verified.
- Remaining production risks and the next concrete fix.

For an ADR, use:

```markdown
# ADR: Codebase Architecture Decision

## Context

## Decision

## Folder And Module Rules

## Consequences

## Alternatives Considered

## Migration

## Validation
```

## Implementation Rules

- Inspect before editing. Do not restructure based only on names.
- Move files only when the new location makes future changes clearer.
- Preserve public imports where possible. Add compatibility exports temporarily if needed.
- Update imports mechanically and then review the result semantically.
- Keep each phase behaviour-preserving unless the user requested a behaviour change.
- Prefer automated import updates, type checks, dependency graph tools, and tests over manual confidence.
- Use deletion as a first-class refactor, but never delete user work, generated inputs, migrations, assets, fixtures, or dynamic entry points without evidence.
- Keep the final codebase smaller when possible. If line count or file count increases, the added structure must clearly reduce risk or complexity.
- Keep unrelated formatting and refactors out of the change.
- Run available type checks, lint, tests, build, or targeted dependency checks.
- If checks cannot run, state exactly what remains unverified.
