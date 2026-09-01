---
name: readme-generator
description: Generate, rewrite, audit, or update a repository README.md by inspecting the codebase and documenting verified setup, scripts, APIs, environment variables, testing, deployment, architecture, troubleshooting, security notes, and maintenance guidance. Use automatically when the user asks to create, generate, write, rewrite, improve, refresh, fix, audit, or update a project README, repository documentation, setup guide, developer onboarding guide, or README quality review for a software project.
---

# README Generator

Create or update the repository root `README.md` for the current project.

Use only Indian English. Use only ASCII characters. Do not use em dashes, en dashes, smart quotes, emojis, icons, or any other non-ASCII character.

## Core Requirements

Write the README so it is:

- Written in very simple, beginner-friendly language
- Technical, accurate, formal, and complete
- Structured using valid Markdown
- Clear enough for a new developer to understand the project without additional help
- Detailed from installation to deployment and maintenance
- Based only on facts available in the repository
- Free from invented features, commands, metrics, URLs, credentials, or configuration values

If a `README.md` already exists, update or replace it as needed while preserving accurate project-specific information that remains useful. Remove stale, unverifiable, duplicated, or misleading claims.

## Repository Inspection

First, inspect the repository before drafting the README. Build a fact ledger from files and command output so claims can be traced back to evidence. Review:

- Source code
- Configuration files
- Package and dependency files
- Scripts and command definitions
- Environment variable usage
- Tests
- Existing documentation
- API routes
- Database files, schemas, migrations, and seed files
- Deployment files
- CI or CD workflows
- Docker, compose, server, and hosting files

Use this analysis to ensure that the README accurately represents the current project.

## Candidate Sections

Include the following sections where they are relevant and supported by repository evidence:

1. Project title
2. Table of contents
3. Quick start
4. Project overview
5. Problem statement
6. Project goals
7. Key features
8. Supported use cases
9. System architecture
10. Application workflow
11. Technology stack
12. Repository structure
13. Prerequisites
14. Local installation
15. Dependency installation
16. Environment configuration
17. Database setup
18. Running the application
19. Available scripts and commands
20. API documentation
21. Authentication and authorisation
22. Input validation
23. Error handling
24. Logging
25. Testing
26. Code quality checks
27. Build process
28. Production deployment
29. CI or CD process
30. Security considerations
31. Performance considerations
32. Monitoring and maintenance
33. Troubleshooting
34. Known limitations
35. Contribution guidelines
36. Coding standards
37. Licence
38. Support and contact information

Do not include a section merely to satisfy this list. If a section is not applicable, omit it unless the absence itself is useful to readers.

## Quick Start

Add a quick-start section near the beginning. It must contain the minimum verified steps needed to install and run the project locally.

For every installation or execution step:

- Provide the exact command
- Explain what the command does
- Explain where the command must be run
- Explain the expected result
- Mention common errors and their solutions
- Keep commands compatible with the actual repository

Do not execute destructive commands, deployment commands, database reset commands, migration commands, seed commands, or commands requiring secrets unless the user explicitly asks. If a command cannot be safely executed, verify it from repository files and state that it was not executed.

## Technology Stack

For each technology in the technology stack, explain:

- Its name
- Its version, when available
- Its purpose in the project
- Where it is used
- Why it is needed
- How it interacts with other parts of the system

## Environment Variables

For environment variables, provide a Markdown table containing:

- Variable name
- Whether it is required or optional
- Purpose
- Expected format
- Safe example value
- Default value, when one exists
- Security notes

Never expose real passwords, tokens, secrets, private keys, connection strings, or personal information.

## API Documentation

Include API details only when API endpoints are present in the repository.

For each available endpoint, document:

- HTTP method
- Route
- Purpose
- Authentication requirement
- Request headers
- Path parameters
- Query parameters
- Request body
- Validation rules
- Success response
- Error responses
- Status codes
- Example request
- Example response

Use only routes, payloads, status codes, and validation rules that can be verified from the repository.

## Repository Metrics

Quantify values that help readers understand the repository and can be verified from files or commands. This may include:

- Number of features
- Number of modules
- Number of pages
- Number of components
- Number of API endpoints
- Number of database models
- Number of environment variables
- Number of scripts
- Number of test files
- Number of test cases
- Test coverage percentage
- Build time
- Bundle size
- Supported runtime versions
- Default ports
- Timeout values
- Retry limits
- Pagination limits
- File size limits
- Rate limits

Do not estimate or invent metrics. If a requested or important metric cannot be verified, state exactly:

```text
Not measured in the current repository.
```

When presenting repository metrics, include:

- Metric name
- Verified value
- Source file or command used for verification
- Notes or limitations

## Repository Structure

Add a repository structure section using an ASCII tree. Explain the purpose of every important directory and file shown in the tree.

## Diagrams

Add Mermaid diagrams only if the repository clearly contains enough information to create an accurate diagram. Keep all text inside Mermaid diagrams limited to ASCII characters.

Include diagrams for the following when relevant:

- High-level system architecture
- Request and response flow
- Authentication flow
- Database relationships
- Deployment flow

## Troubleshooting

Add a troubleshooting table containing:

- Problem
- Likely cause
- Diagnostic command
- Resolution

## Markdown Rules

Use proper Markdown formatting:

- Clear heading hierarchy
- Short paragraphs
- Ordered steps for procedures
- Bullet lists for related items
- Tables for structured information
- Code blocks with correct language identifiers
- Relative repository links where possible
- A table of contents with working anchor links

Avoid vague statements such as:

- Fast
- Scalable
- Secure
- Lightweight
- Production-ready
- Highly available
- Optimised
- Easy to use

Use these terms only when they are supported by measurable evidence in the repository. Explain the evidence and provide the verified metric.

Do not include badges unless their URLs and values can be verified from the repository or its existing configuration.

## Final Validation

Before finalising the README:

1. Verify every command against the repository.
2. Verify every file path.
3. Verify every port and environment variable.
4. Verify every API route.
5. Verify every dependency and version.
6. Verify every metric.
7. Confirm that no secret data is exposed.
8. Confirm that all characters are ASCII.
9. Confirm that no em dash or en dash is present.
10. Confirm that the Markdown structure is valid.
11. Confirm that the document uses simple Indian English.
12. Confirm that no unsupported claim has been added.

Write the final output directly to the repository root as:

```text
README.md
```
