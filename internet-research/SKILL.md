---
name: internet-research
description: Research current or source-dependent facts, prior art, comparable products, repositories, libraries, docs, issues, discussions, benchmarks, pricing, legal or regulatory details, and implementation examples. Use when the user asks to research, look up, verify, cite, benchmark, compare, find similar projects, repos, or apps, assess current options, validate assumptions with sources, or make a decision that benefits from external evidence.
---

# Internet Research

Use external evidence where it materially improves the answer. Search broadly, but tie every claim to its source quality, date, and scope.

## Rules

- Search before making claims that are current, niche, source-dependent, or likely to have changed. With no web tool, say so, answer from known information, and flag claims that may be outdated.
- Prefer primary sources: official docs, repositories, release notes, standards, papers, vendor docs, changelogs, and source code.
- Treat Reddit, Hacker News, issues, Discord mirrors, and forums as anecdotal, and label them so. Look for repeated complaints, workarounds, and edge cases rather than taking comments as fact.
- Cite only sources you opened and checked.
- State the practical search scope. Never claim to have searched the whole internet.
- Compare publication, release, and event dates, and give absolute dates when recency matters.
- Discard SEO pages, scraped summaries, and marketing posts unless the task is about market positioning.
- Separate verified fact, inference, and opinion. Mark uncertainty instead of filling gaps.
- Frame findings around the user's decision. Do not dump sources when a recommendation or tradeoff analysis is needed.

## Workflow

1. Write a brief: the decision, constraints, keywords, competitors, user segment, freshness needed, and evidence needed.
2. Search in layers: official docs and standards; repositories, package registries, examples, and starters; comparable products, competitors, pricing, launch posts, and case studies; user discussions on Reddit, Hacker News, GitHub issues, Stack Overflow, and forums; and, when current context matters, news, release notes, advisories, benchmarks, and changelogs.
3. Open promising sources and verify details directly.
4. Extract repeated patterns, tradeoffs, warnings, maintenance and adoption signals, and implementation details.
5. Synthesise into actionable options, each with its supporting and missing evidence.

## Source Checks

- Repositories: recent commits, releases, issues, docs, licence, tests, examples, and dependency health. Stars alone prove nothing.
- Libraries and frameworks: official docs and source examples over tutorials.
- Products: separate marketing claims from observable features, pricing, screenshots, docs, and user reports.
- Benchmarks: hardware, dataset, workload, version, date, and fit with the user's context.

## Output

Use the shortest format that supports the decision:

- Scope: what was and was not searched, and the search date.
- Strong signals: findings repeated across reliable sources.
- Weak or anecdotal signals.
- Recommendation and why, plus alternatives that win under other constraints.
- Sources, grouped by type.

If the evidence is thin, say so and describe what would raise confidence.
