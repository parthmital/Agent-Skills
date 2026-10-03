---
name: internet-research
description: Researches current or source-dependent facts, prior art, comparable products, repositories, libraries, docs, issues, discussions, benchmarks, pricing, legal or regulatory details, and implementation examples, with cited, dated evidence. Use when the user asks to research, look up, verify, cite, benchmark, or compare, find similar projects, repos, or apps, assess current options, validate assumptions with sources, or make a decision that benefits from external evidence.
---

# Internet Research

## Overview

Use external evidence where it materially improves the answer, and tie every claim to its source quality, date, and scope.

## When to Use

- Claims that are current, niche, source-dependent, or likely to have changed.
- Decisions between libraries, products, or approaches.
- Not for facts the repository itself answers; read the code instead.

## Process

1. Brief: the decision, constraints, keywords, competitors, user segment, freshness, and evidence needed.
2. Search in layers: official docs and standards; repositories, registries, and examples; comparable products, pricing, launch posts, case studies; user discussions (Reddit, Hacker News, GitHub issues, Stack Overflow, forums); and, when recency matters, news, release notes, advisories, benchmarks, changelogs.
3. Open promising sources and verify details directly. Cite only sources you opened.
4. Extract repeated patterns, tradeoffs, warnings, maintenance and adoption signals, and implementation details.
5. Synthesise options around the user's decision, each with supporting and missing evidence.
6. Write or update root `RESEARCH.md`: one dated section per topic with brief, scope, findings, recommendation, and sources. Update a topic's section rather than duplicating it; mark superseded findings.

With no web tool, say so, answer from known information, and flag what may be outdated.

## Source Rules

- Primary sources first: official docs, repositories, release notes, standards, papers, changelogs, source code.
- Forums and issues are anecdotal; label them and look for repeated complaints and workarounds.
- Discard SEO pages, scraped summaries, and marketing unless the task is market positioning.
- Repositories: recent commits, releases, issues, docs, licence, tests, dependency health. Stars prove nothing.
- Products: separate marketing claims from observable features, pricing, docs, and user reports.
- Benchmarks: check hardware, dataset, workload, version, date, and fit with the user's context.
- Give absolute dates when recency matters. Separate fact, inference, and opinion.

## Output

Shortest format that supports the decision: scope searched and search date; strong signals; weak or anecdotal signals; recommendation with reasons and alternatives that win under other constraints; sources grouped by type. If evidence is thin, say so and what would raise confidence.

## Common Rationalizations

| Rationalization                              | Reality                                            |
| -------------------------------------------- | -------------------------------------------------- |
| "I already know this"                        | Training data goes stale; verify anything current. |
| "The snippet in the search result is enough" | Snippets lose context and dates. Open the source.  |
| "Lots of stars means it is maintained"       | Check commits, releases, and open issues.          |

## Red Flags

- Claiming to have searched "the whole internet".
- Citing a page that was never opened.
- A source dump with no recommendation.

## Verification

- [ ] Every claim has an opened, dated source or is marked as inference.
- [ ] Scope and search date stated.
- [ ] Recommendation tied to the user's decision.
- [ ] `RESEARCH.md` updated without duplicate topics.
