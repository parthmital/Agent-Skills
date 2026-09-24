---
name: linkedin-project-description
description: Turn a project README or project write-up into a concise LinkedIn project description of at most 1000 characters, grounded only in the source. Use automatically when the user asks for a LinkedIn project description, LinkedIn project summary, LinkedIn post about a project, or to convert a README for LinkedIn.
---

# LinkedIn Project Description

Turn a project README (or similar write-up) into a polished LinkedIn project description.

If the user has not given the source, ask for it. If they point at a repository, read its `README.md`, plus any linked docs that hold the metrics.

## Before Writing

Identify internally, without printing it:

1. Purpose and users.
2. The 3 to 5 main technical contributions.
3. The strongest supported metrics.
4. Clear user, business, or operational impact.
5. Details to omit.

## Requirements

- At most 1000 characters, including spaces and punctuation. Count before replying.
- Output only the final description in one code block. No title, intro, explanation, or citations.
- Start with one simple sentence saying what was built and why.
- Follow with 3 to 5 concise bullets that start with `•`.
- Order: what was built, then how, then measurable impact.
- Include technologies, systems, scale, workflows, and metrics only when the source supports them. Do not turn it into a tech-stack list.
- Preserve metrics and units exactly. Never invent, estimate, infer, or exaggerate.
- Combine related features. Focus on substantial engineering work and clear outcomes.
- Use simple, direct language that recruiters and engineers both understand. Avoid buzzwords such as "cutting-edge", "innovative", "seamless", "scalable", and "revolutionary".
- Use strong verbs such as Built, Designed, Engineered, Automated, Implemented, and Developed.
- If the source conflicts with itself, use the most specific or most current information without guessing.

Write the shortest natural version that keeps the most important technical and measurable information.
