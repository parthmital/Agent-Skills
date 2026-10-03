---
name: security-hardening
description: "Scans a whole repository and its Git history for every class of vulnerability, then fixes and verifies them: code, dependencies, secrets, auth, injection, web and API flaws, crypto, files, business logic, CI/CD, containers, infrastructure, and LLM features. Use when the user asks for a security audit, vulnerability or secret scan, dependency audit, threat model, OWASP review, or to secure, harden, or make a codebase bulletproof. Whole repository, not just pending changes."
---

# Security Hardening

## Overview

Find, fix, and prove fixes for every exploitable weakness. No code is provably attack-proof: "bulletproof" means every checklist category was checked, every confirmed issue is fixed and tested, and the rest is reported as residual risk.

## When to Use

- Whole-repo security audits, scans, threat models, or hardening.
- Fixes are in scope, including central ones such as a validation or auth layer. Flag fixes that change behaviour.
- Ask before rewriting Git history, rotating real credentials, breaking a published API, or changing live infrastructure.

## Process

1. Map the attack surface: entry points, trust boundaries, roles, sensitive assets, data stores, integrations. Write a short threat model.
2. Run fitting scanners, installed inside the repo; treat output as leads. If one cannot run, cover its category manually.
   - Secrets and history: `gitleaks`, `trufflehog`.
   - Dependencies: `osv-scanner` plus the native auditor (`npm audit`, `pip-audit`, `cargo audit`, `govulncheck`).
   - Static: `semgrep`, plus `bandit`, `gosec`, `brakeman`, or CodeQL.
   - Infrastructure and CI: `trivy`, `checkov`, `hadolint`, `zizmor`.
3. Review every checklist category by hand, tracing untrusted input from source to sink. Scanners miss logic and authorisation flaws.
4. Confirm each finding with a concrete attack path; drop false positives. Rate Critical, High, Medium, or Low and tag the CWE.
5. Fix highest severity first; add a regression test reproducing each attack.
6. Re-scan until nothing new appears.
7. Add guardrails: secret-scanning pre-commit hook, Dependabot or Renovate, CI security scans, SHA-pinned least-privilege actions.
8. Write or update root `SECURITY.md`: reporting policy, threat model, scanners and guardrails, checklist status, fixed findings by ID and severity (no exploit details for unfixed ones), residual risks, required user actions. Never secrets.

## Checklist

- **Secrets:** in code, config, tests, notebooks, images, CI, docs, history; never logged, returned, or bundled client-side.
- **Authentication:** Argon2id, scrypt, or bcrypt; brute-force limits; reset and email-change flows; session fixation, expiry, revocation; cookie flags; JWT algorithm, expiry, audience, issuer; OAuth `state`, PKCE, redirect URIs.
- **Authorisation:** server-side, deny by default; IDOR, function-level, tenant isolation; mass assignment; exposed admin or debug routes.
- **Injection:** SQL, NoSQL, raw ORM, OS command, `eval`, template, LDAP, XPath, GraphQL, CRLF, log, CSV formula.
- **Web client:** XSS and unsafe HTML sinks, CSP, CSRF, clickjacking, open redirects, `postMessage` origins, prototype pollution, SRI.
- **Server parsing:** SSRF (including metadata endpoints), XXE, unsafe deserialisation, ReDoS, zip slip, decompression bombs.
- **Files:** path traversal, upload type and size, storage outside web root, content type, symlinks.
- **API:** schema validation, excess data exposure, rate limits, pagination caps, GraphQL depth, CORS, webhook signatures and replay, idempotency.
- **Logic and concurrency:** races, TOCTOU, double spend, negative or overflowing values, skipped steps, trusted client prices or roles.
- **Crypto:** no custom crypto or MD5/SHA-1 for security; authenticated encryption; secure randomness; constant-time comparison; TLS verification on.
- **Errors and privacy:** no internals in responses; security events logged without secrets or PII; PII minimised.
- **Supply chain:** CVEs, typosquats, dependency confusion, lockfiles, install scripts, unpinned versions.
- **CI/CD:** `pull_request_target` misuse, script injection from event fields, secrets exposed to forks, broad `GITHUB_TOKEN`, unpinned actions.
- **Containers and infrastructure:** root users, unpinned images, secrets in layers, public buckets, open ports, broad IAM, unencrypted storage, privileged pods.
- **Config:** debug off in production, secure defaults, HSTS, CSP, `X-Content-Type-Options`, `Referrer-Policy`, startup validation.
- **DoS:** unbounded bodies, queries, recursion, memory; outbound timeouts.
- **LLM and agents:** prompt injection, over-privileged tools, model output reaching shell, SQL, HTML, or paths, cross-user leakage.
- **Mobile and extensions:** insecure storage, exported components, deep links, broad permissions.

## Fix Rules

- Fix once, centrally (validator, auth guard, query layer, encoder), not per call site.
- Prefer framework protections; allowlist input at boundaries, encode output by context, least privilege.
- A committed secret is compromised: move it to config and tell the user to rotate it.
- Upgrade dependencies via the package manager after checking changelogs; otherwise mitigate or replace and record why.
- Never silence scanners or weaken tests; each suppression names its rule and reason inline.

## Common Rationalizations

| Rationalization                | Reality                                                       |
| ------------------------------ | ------------------------------------------------------------- |
| "The scanners came back clean" | Scanners miss authorisation and logic flaws; review by hand.  |
| "That endpoint is internal"    | Internal services get reached through SSRF and stolen tokens. |
| "The secret is gitignored now" | It is still in history; it must be rotated.                   |
| "Fixed it, no need for a test" | Without a regression test, the hole reopens silently.         |

## Red Flags

- A finding marked fixed with no reproducing test.
- Checklist categories with no recorded status.
- Suppressions without a stated reason.

## Verification

- [ ] Report scope, tools run and not run, and counts by severity (found, fixed, remaining).
- [ ] Per finding: ID, severity, CWE, location, attack scenario, fix, proving test.
- [ ] Every checklist category marked fixed, clean, not applicable, or unverified.
- [ ] User actions listed (credentials to rotate, platform settings); residual risks with next steps.
- [ ] `SECURITY.md` updated with no secrets or unfixed exploit details.
