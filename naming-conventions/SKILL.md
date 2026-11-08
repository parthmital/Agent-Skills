---
name: naming-conventions
description: Sets, applies, and enforces one consistent, descriptive naming standard across a repository for directories, files, modules, types, functions, variables, constants, config keys, environment variables, database objects, branches, and tests, following each language's official style. Use when starting a project, adding a new kind of file or module, renaming anything, auditing or unifying names, or when the user mentions naming, casing, inconsistent or unclear names, or naming conventions.
---

# Naming Conventions

## Overview

A reader, human or agent, should predict a name's casing from its kind and its responsibility from its words. Each kind of identifier has exactly one convention in the repository, the language's official style comes first, the result is recorded once, and tooling enforces whatever it can.

## When to Use

- Setting conventions for a new repository, or auditing and unifying an existing one.
- Adding a kind of file, module, or identifier with no precedent in the repository.
- Any rename. Restructuring itself belongs to `production-architecture`, which uses this skill for the names.
- Not for prose style or Markdown headings of other repositories unless asked.

## Precedence

Follow the first source that decides the name:

1. External contracts: names a framework or tool requires (`page.tsx`, `Dockerfile`, `SKILL.md`, `__init__.py`, `pyproject.toml`), published APIs, URLs, database objects in production, and environment variables other systems read. Keep them; renaming one needs the user's approval.
2. The language's official style and its linter: PEP 8 (ruff `N` rules), Effective Go, Rust RFC 430, the Java and Kotlin conventions, and the established TypeScript style (`@typescript-eslint/naming-convention`).
3. The repository's recorded conventions in the `Conventions` section of its `AGENTS.md`.
4. The defaults below.

## Defaults

| Kind                                   | Convention                                                                        | Example                                   |
| -------------------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------- |
| Directories                            | kebab-case                                                                        | `payment-service/`                        |
| Docs, assets, and other non-code files | kebab-case; root docs UPPERCASE                                                   | `deploy-guide.md`, `ARCHITECTURE.md`      |
| Python modules, scripts, tests         | snake_case; single-purpose scripts start with a verb; tests `test_<module>.py`    | `parse_invoice.py`                        |
| JavaScript and TypeScript files        | kebab-case; PascalCase component files only where the framework or repo does this | `date-format.ts`, `UserCard.tsx`          |
| Go packages and files                  | short lowercase package, snake_case file                                          | `invoice/invoice_parser.go`               |
| Classes, types, interfaces, enums      | PascalCase noun                                                                   | `InvoiceParser`                           |
| Functions and methods                  | the language's case, verb phrase                                                  | `parse_invoice`, `fetchUser`              |
| Variables and parameters               | the language's case, noun phrase                                                  | `retry_count`, `activeUsers`              |
| Booleans                               | `is`, `has`, `can`, or `should` prefix, stated positively                         | `is_enabled`, `hasAccess`                 |
| Constants and environment variables    | UPPER_SNAKE_CASE; environment variables carry an app prefix                       | `MAX_RETRIES`, `BILLING_API_URL`          |
| JSON, YAML, and config keys            | the format's or API's existing convention, one per file                           | `camelCase` in a JSON API                 |
| Database tables and columns            | snake_case; table plurality as the repository already uses                        | `order_items.created_at`                  |
| CSS classes, CLI flags, URL paths      | kebab-case, or the repository's CSS methodology                                   | `card-header`, `--dry-run`, `/user-files` |
| Git branches                           | `<type>/<kebab-summary>`                                                          | `fix/login-timeout`                       |
| Test names                             | the behaviour under test                                                          | `test_rejects_expired_token`              |

## Semantic Rules

- Name by responsibility, what it is or does, never by where it lives or when it was written. Banned in durable names: `utils`, `helpers`, `common`, `misc`, `stuff`, `data2`, `new`, `old`, `v2`, `final`, `temp`, `tmp`.
- Full words over abbreviations, except universal ones (`id`, `url`, `http`, `db`, `config`). Acronym casing follows the language (`HttpClient` in TypeScript, `userID` in Go).
- Units and formats in the name when the type does not carry them: `timeout_seconds`, `price_cents`, `created_at_utc`.
- Plural for collections, singular for items, `<value>_by_<key>` for maps: `users`, `user`, `user_by_id`.
- One term per concept across code, files, docs, and UI: pick `customer` or `client`, `fetch` or `load`, and never mix them.
- Visible side effects: a function that writes is not called `get_*`.
- Length matches scope: a loop index may be `i`, a module-level name is fully descriptive.
- No type prefixes (`strName`), negated booleans (`is_not_ready`), or names that differ only in case or a number.

## Process

1. Detect: list each kind's current conventions with counts from `git ls-files`, linter config, and a sample of identifiers. The majority that agrees with the language style is the candidate.
2. Decide each kind by Precedence. Record only the kinds that occur, as a compact table in the target repository's `AGENTS.md` `Conventions` section (format owned by `project-docs`), with every exception and its reason.
3. Enforce what tools can: `ls-lint` for file and directory names, ruff `N`, `@typescript-eslint/naming-convention` or `eslint-plugin-check-file`, `golangci-lint`, `stylelint` `selector-class-pattern`. Add each to the repository's check command and CI.
4. Rename only what breaks a convention or a semantic rule, with language-aware tooling (IDE or LSP rename, `git mv`, codemods), and update every reference in the same change: imports, config, scripts, CI, docs, links, tests. For a case-only rename on Windows or macOS, go through a temporary name (`git mv a.py tmp.py`, then `git mv tmp.py A.py`).
5. Delegation: for a whole-repository pass, a `research-worker` inventories names per kind and `task-worker`s rename one kind or directory each, with disjoint file scopes. The orchestrator decides the conventions and runs the final checks (`subagent-delegation`).

## Examples

| Bad                                            | Good                         | Why                       |
| ---------------------------------------------- | ---------------------------- | ------------------------- |
| `utils/helpers.ts`                             | `date-format.ts`             | Names the responsibility  |
| `data2`, `tmp_list`                            | `unpaid_invoices`            | Says what it holds        |
| `process()`                                    | `send_reminder_emails()`     | Verb plus object          |
| `flag`, `archived_status`                      | `is_archived`                | Reads as a yes or no      |
| `timeout = 30`                                 | `timeout_seconds = 30`       | Unit in the name          |
| `getUser()` that inserts a row                 | `findOrCreateUser()`         | Side effect visible       |
| `UserService`, `user_srv`, `usersMgr` together | `UserService` everywhere     | One pattern per kind      |
| `Final_Report-v2.md`                           | `quarterly-sales-summary.md` | kebab-case, content named |

## Common Rationalisations

| Rationalisation                   | Reality                                                                                         |
| --------------------------------- | ----------------------------------------------------------------------------------------------- |
| "Renaming is cosmetic"            | Agents and people find code by name; inconsistent names hide code and breed duplicates.         |
| "The old name is used everywhere" | Rename with tooling and update every reference in one change, or record it as an exception.     |
| "A short name is quicker"         | Names are read far more often than typed.                                                       |
| "I prefer another style"          | The language style and the repository's record win over preference.                             |
| "Rename the API field too"        | Contract names break their consumers; ask first, and keep a compatibility path if one is asked. |

## Red Flags

- A new name whose casing differs from its kind's recorded convention.
- A banned drawer or version word in a durable name.
- A rename that leaves `git grep` hits of the old name.
- A public API, URL, production database object, or shared environment variable renamed without approval.

## Verification

- [ ] Conventions recorded once in the target repository's `AGENTS.md` and matching the code.
- [ ] Every enforceable convention has a configured linter, and it passes.
- [ ] `git grep -n <old-name>` shows no stale reference for any renamed item; tests and build pass.
- [ ] Contract names unchanged unless approved; each exception recorded with its reason.
