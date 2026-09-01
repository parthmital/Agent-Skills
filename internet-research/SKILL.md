---
name: internet-research
description: Research current or source-dependent facts, prior art, comparable products, repositories, libraries, docs, issues, discussions, benchmarks, pricing, legal or regulatory details, and implementation examples. Use automatically when the user asks to research, look up, verify, cite, benchmark, compare, find similar projects, find repos or apps, assess current options, validate assumptions with sources, or make a decision that benefits from external evidence.
---

# Internet Research

Use this skill when external context can materially improve the answer. Search broadly enough to avoid a narrow answer, but keep each claim tied to source quality, date, and scope.

## Rules

- Browse the internet before making claims that are current, niche, source-dependent, or likely to have changed.
- Prefer primary sources: official docs, repositories, release notes, standards, academic papers, vendor docs, changelogs, and source code.
- Use social sources such as Reddit, Hacker News, issues, Discord mirrors, and forums as anecdotal signals. Label them as anecdotal.
- Cite links for claims based on external sources. Do not cite a source that was not opened and checked.
- Do not claim to have searched the complete internet. State the practical search scope instead.
- Compare publication dates, release dates, and event dates. Mention absolute dates when recency matters.
- Discard SEO pages, scraped summaries, and low-signal marketing posts unless the task is about market positioning.
- Separate verified facts, informed inference, and opinion. Mark uncertainty instead of filling gaps.
- Use the user's decision as the frame. Do not return a source dump when a recommendation or tradeoff analysis is needed.

## Workflow

1. Convert the user request into a research brief: decision to make, constraints, keywords, competitors, user segment, freshness requirement, and evidence needed.
2. Search in layers:
   - Official documentation, standards, and vendor pages.
   - GitHub or GitLab repositories, package registries, examples, templates, and starter kits.
   - Comparable apps, products, competitors, pricing pages, launch posts, and case studies.
   - User discussions on Reddit, Hacker News, GitHub issues, Stack Overflow, forums, and community boards.
   - Recent news, release notes, advisories, benchmarks, and changelogs when current context matters.
3. Open promising sources and verify details directly.
4. Extract repeated patterns, tradeoffs, warnings, maintenance signals, adoption signals, and implementation details.
5. Synthesize into actionable options. Explain what evidence supports each option and what evidence is missing.

## Source Quality Checks

- For repositories, check recent commits, releases, issues, documentation, licence, tests, examples, and dependency health. Stars alone are not evidence.
- For libraries and frameworks, prefer official docs and source examples over tutorials.
- For products, distinguish marketing claims from observable features, pricing, screenshots, docs, and user reports.
- For Reddit and forums, look for repeated complaints, workarounds, and edge cases rather than treating comments as facts.
- For benchmarks, check hardware, dataset, workload, version, date, and whether the benchmark matches the user's context.

## Output

Use the shortest format that supports the decision:

- Research scope: what was searched and what was not.
- Strong signals: findings that appeared across reliable sources.
- Weak or anecdotal signals: social discussion, isolated reports, or unverified claims.
- Recommendation: the best current path and why.
- Alternatives: when another option is better under different constraints.
- Sources: links grouped by source type.

If the evidence is thin, say so directly and describe what would be needed to decide with higher confidence.
