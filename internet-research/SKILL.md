---
name: internet-research
description: Researches current or source-dependent facts, products, repositories, libraries, docs, discussions, benchmarks, pricing, and legal or regulatory details, with cited, dated evidence. Use when the user asks to research, look up, verify, fact-check, cite, benchmark, or compare, find similar projects or apps, assess current options, or validate assumptions with sources. For choosing what to reuse before building, use `research-driven-development`.
---

# Internet Research

## Overview

Establish what is actually true. Use external evidence where it materially improves the answer, and tie every claim to its evidence quality, date, and scope.

## When to Use

- Claims that are current, niche, source-dependent, or likely to have changed.
- Decisions between libraries, products, or approaches.
- Not for facts the repository itself answers; read the code instead.
- Deciding what to reuse before building: `research-driven-development`, which applies the Source Rules below.

## Process

1. Brief: the decision, constraints, keywords, competitors, user segment, freshness, and evidence needed.
2. Search every layer that fits, none ranked above another by who publishes it. Layers: official docs and standards, papers, repositories, registries, and examples, comparable products, pricing, launch posts, and case studies, community and independent sources (Reddit, Hacker News, GitHub issues, Stack Overflow, forums, user- or student-run trackers and datasets), and, when recency matters, news, release notes, advisories, benchmarks, and changelogs.
3. Open promising sources and extract their full content, never stopping at search snippets: fetch pages, use Playwright or other browser automation for JavaScript-rendered pages, dashboards, and pagination, and download and extract PDFs, tables, and datasets (installs per `repo-local-workspace`). Stay technically and legally permissible: no bypassing paywalls, logins, CAPTCHAs, or access controls, and respect site terms and rate limits. Cite only sources you opened.
4. Extract repeated patterns, tradeoffs, warnings, maintenance and adoption signals, and implementation details.
5. Synthesise options around the user's decision, each with supporting and missing evidence.
6. Write or update root `RESEARCH.md` from the `project-docs` template: one dated section per topic, updated rather than duplicated, with superseded findings marked.

With no web tool, say so, answer from known information, and flag what may be outdated.

## Source Rules

- Judge each source by its evidence, never its status: transparency of method and data, verifiability (raw data, named sources, reproducibility), independence and incentives, recency, and relevance. Official does not mean reliable, and unofficial does not mean unreliable.
- First-party sources are authoritative for what their owner defines (an API, a policy text, a version history) but are interested parties on their own outcomes and reputation (placement rates, benchmarks, user counts, safety records). Check such claims against independent evidence.
- Independent and community sources (forums, issues, user- or student-run trackers, crowdsourced data) are often the best record of ground reality. Weigh them like any source: sample size, raw data, consistency across independent reports, and signs of brigading or astroturfing. A single anecdote is labelled as one.
- When sources conflict, report each side with the evidence behind it and say which is stronger and why. Never settle a conflict by authority alone.
- Discard SEO pages, scraped summaries, and evidence-free marketing.
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
| "It is the official site, so it is true"     | Owners are interested parties about themselves.    |
| "It is only Reddit, so it does not count"    | Weigh its data and consistency, not its venue.     |

## Red Flags

- Claiming to have searched "the whole internet".
- Citing a page that was never opened.
- Ranking or dismissing a source by who published it rather than what evidence it shows.
- An owner's claim about its own outcomes reported as fact without independent checks.
- A source dump with no recommendation.

## Verification

- [ ] Every claim has an opened, dated source or is marked as inference.
- [ ] Sources weighed on evidence quality, and conflicts between official and independent sources reported, not settled by authority.
- [ ] Scope and search date stated.
- [ ] Recommendation tied to the user's decision.
- [ ] `RESEARCH.md` updated without duplicate topics.
