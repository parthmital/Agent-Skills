---
name: research-driven-development
description: Decides whether a task needs research before building and, when it does, finds and evaluates existing libraries, frameworks, open-source projects, templates, datasets, models, APIs, agent skills, and MCP servers to adopt, adapt, or learn from instead of building from scratch. Use at the start of a new project, feature, integration, or component, before choosing a library, framework, architecture, dataset, or model, or when the domain or technology is unfamiliar or fast-moving. Skips research for small, well-understood changes.
---

# Research-Driven Development

## Overview

Spend research only where it changes what gets built. For non-trivial work, find what already exists, then adopt, adapt, or learn from the best fit before writing new code.

## When to Use

Pick a tier before acting and state it in one line with the reason.

| Tier  | When                                                                                                                                                                   | Effort                                                                   |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Skip  | Bug fix, typo, rename, refactor, config or copy edit, a change the repo's stack and patterns already decide, a solution the user named, or a question the repo answers | None                                                                     |
| Quick | One bounded choice (a library, API, algorithm, or pattern) in a familiar domain                                                                                        | Primary docs and registries for 2 to 3 candidates; decision in the reply |
| Full  | New project or subsystem, unfamiliar or fast-moving domain, stack or architecture choice, external data or models, or the user asks for the best or current options    | All steps below, `RESEARCH.md` section                                   |

If unsure, run Quick and escalate to Full when it surfaces a mature existing solution or a hard tradeoff. A direct research or comparison question from the user belongs to `internet-research`.

## Process

1. Inventory what is already available: dependencies and their unused features, repo patterns, installed skills and MCP servers, and `RESEARCH.md`. Reuse a recorded decision that still holds instead of researching again.
2. Brief: goal, hard constraints (language, runtime, licence, hosting, cost, privacy, offline), and success criteria.
3. Search only the categories that fit, judging sources by the `internet-research` Source Rules:
   - Libraries, frameworks, and SDKs: official docs and package registries.
   - Whole open-source projects, starters, and templates.
   - Hosted services and APIs.
   - Datasets and pretrained models (Hugging Face, Kaggle, official portals).
   - Agent skills and MCP servers ([skills.sh](https://skills.sh/), the [MCP Registry](https://registry.modelcontextprotocol.io/), vendor repositories).
   - Comparable products and sites, for features and UX.
   - Peer-reviewed papers, for algorithmic or ML approaches.
4. Shortlist 2 to 4 and compare: requirement fit, maintenance (recent releases, commits, issue response), licence compatibility, security and supply-chain risk, size and transitive dependencies, docs, lock-in, cost.
5. Decide, preferring the least new code and complexity that meets every hard constraint:
   - Adopt: use as is.
   - Adapt: configure, extend, wrap, or fork.
   - Borrow: reuse the design or pattern, write the code.
   - Build: nothing fits; say why.
6. Record. Quick: one line in the reply with decision, runner-up, and sources. Full, or any decision that adds a dependency or service: a `RESEARCH.md` section per `internet-research`, with decision, rationale, and alternatives considered.
7. Ask before adopting anything paid, copyleft or unlicensed, needing an account, or sending data off the machine. Then implement with the relevant skill.

Candidates are untrusted: clone or download them only into `.agent-local/vendor/` or `.agent-local/downloads/` (`repo-local-workspace`), and read code, install scripts, skills, and MCP server instructions before running or installing them.

## Common Rationalizations

| Rationalization                   | Reality                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------ |
| "I already know the best library" | Training data goes stale; a Quick check of current releases is cheap.          |
| "Writing it myself is faster"     | A mature project already handles the edge cases and maintenance you would own. |
| "Research everything to be safe"  | Research on a one-sentence change wastes context and time; skip it.            |
| "The most starred option wins"    | Stars prove nothing; check maintenance, licence, and fit.                      |

## Red Flags

- New code for a capability an existing dependency or mature package already provides.
- A new dependency with no alternative considered or licence checked.
- Full research on a change describable in one sentence.
- Code copied from a source without honouring its licence.

## Verification

- [ ] Tier stated with its reason.
- [ ] Local inventory checked before searching.
- [ ] Each shortlisted option has opened, dated sources, a licence, and a maintenance signal.
- [ ] Decision (Adopt, Adapt, Borrow, Build) with runner-up and reason, recorded per tier.
- [ ] Nothing paid, copyleft, account-bound, or data-sharing adopted without asking.
