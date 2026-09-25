---
name: linkedin-project-description
description: Turn a project README or project write-up into a concise LinkedIn project description of at most 1000 characters, grounded only in the source. Use when the user asks for a LinkedIn project description, LinkedIn project summary, LinkedIn post about a project, or to convert a README for LinkedIn.
---

# LinkedIn Project Description

Turn a project README or similar write-up into a LinkedIn project description. If no source is given, ask for it. If the user points at a repository, read its `README.md` and any linked docs that hold the metrics.

Before writing, silently identify: purpose and users, the 3 to 5 main technical contributions, the strongest supported metrics, clear user, business, or operational impact, and what to leave out.

## Requirements

- At most 1000 characters including spaces and punctuation. Count before replying.
- Output only the description, in one code block, with no title, intro, explanation, or citations.
- Open with one simple sentence on what was built and why, then 3 to 5 concise bullets starting with `•`.
- Order: what was built, then how, then measurable impact.
- Mention technologies, systems, scale, workflows, and metrics only when the source supports them, and do not turn it into a tech-stack list.
- Keep metrics and units exactly as in the source. Never invent, estimate, infer, or exaggerate.
- Combine related features and focus on substantial engineering work and clear outcomes.
- Use simple, direct language for recruiters and engineers alike, with strong verbs such as Built, Designed, Engineered, Automated, Implemented, and Developed. Avoid buzzwords such as "cutting-edge", "innovative", "seamless", "scalable", and "revolutionary".
- If the source contradicts itself, use the most specific or most current information without guessing.

Write the shortest natural version that keeps the most important technical and measurable information.
