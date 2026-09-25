---
name: security-hardening
description: "Scan an entire repository and its Git history for every class of vulnerability, then fix and verify them: code, dependencies, secrets, auth, injection, web and API flaws, crypto, files, business logic, CI/CD, containers, infrastructure, and LLM features. Use when the user asks for a security audit, vulnerability or secret scan, dependency audit, threat model, OWASP review, or to secure, harden, or make a codebase bulletproof. Whole repository, not just pending changes."
---

# Security Hardening

Find, fix, and prove fixes for every exploitable weakness in the repository. No code is provably attack-proof: "bulletproof" means every checklist category was checked, every confirmed issue is fixed and tested, and anything left is reported as residual risk.

Fixes are in scope, including broad ones such as a central validation or auth layer. Flag any fix that changes behaviour. Ask before rewriting Git history, rotating real credentials, breaking a published API, or changing live infrastructure. Install scanners inside the repository.

## Workflow

1. Map the attack surface: entry points, trust boundaries, roles, sensitive assets, data stores, integrations. Write a short threat model.
2. Run scanners that fit the stack; treat output as leads. If one cannot run, cover its category manually.
   - Secrets and history: `gitleaks`, `trufflehog`.
   - Dependencies: `osv-scanner` and the native auditor (`npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, etc.).
   - Static analysis: `semgrep`, plus `bandit`, `gosec`, `brakeman`, or CodeQL as applicable.
   - Infrastructure and CI: `trivy`, `checkov`, `hadolint`, `zizmor`.
3. Review every checklist category manually, tracing untrusted input from source to sink. Scanners miss logic and authorisation flaws.
4. Confirm each finding with a concrete attack path; drop false positives. Rate Critical, High, Medium, or Low and tag the CWE.
5. Fix highest severity first, then add a regression test that reproduces each attack.
6. Re-scan until nothing new appears.
7. Add guardrails that fit: secret-scanning pre-commit hook, Dependabot or Renovate, security scans in CI, SHA-pinned least-privilege CI actions, `SECURITY.md` for public repos.

## Checklist

- **Secrets:** in code, config, tests, notebooks, images, CI, docs, and history; never logged, returned, or bundled client-side.
- **Authentication:** Argon2id, scrypt, or bcrypt; brute-force limits; reset and email-change flows; session fixation, expiry, revocation; cookie flags; JWT algorithm, expiry, audience, issuer; OAuth `state`, PKCE, redirect URIs.
- **Authorisation:** server-side, deny by default; object-level (IDOR), function-level, tenant isolation; mass assignment; exposed admin or debug routes.
- **Injection:** SQL, NoSQL, raw ORM, OS command, `eval`, template, LDAP, XPath, GraphQL, CRLF, log, CSV formula.
- **Web client:** XSS and unsafe HTML sinks, CSP, CSRF, clickjacking, open redirects, `postMessage` origins, prototype pollution, SRI.
- **Server parsing:** SSRF (including metadata endpoints), XXE, unsafe deserialisation, ReDoS, zip slip, decompression bombs.
- **Files:** path traversal, upload type and size checks, storage outside web root, content type, symlinks.
- **API:** schema validation, excess data exposure, rate limits, pagination caps, GraphQL depth limits, CORS, webhook signatures and replay, idempotency.
- **Logic and concurrency:** races, TOCTOU, double spend, negative or overflowing values, skipped steps, trusted client prices or roles.
- **Crypto:** no custom crypto, MD5, or SHA-1 for security; authenticated encryption; secure randomness; constant-time comparison; TLS verification on.
- **Errors and privacy:** no internals in responses; security events logged without secrets or PII; PII minimised.
- **Supply chain:** CVEs, typosquats, dependency confusion, lockfiles, install scripts, unpinned versions.
- **CI/CD:** `pull_request_target` misuse, script injection from event fields, secrets exposed to forks, broad `GITHUB_TOKEN`, unpinned actions.
- **Containers and infrastructure:** root users, unpinned images, secrets in layers, public buckets, open ports, broad IAM, unencrypted storage, privileged pods.
- **Config:** debug off in production, secure defaults, HSTS, CSP, `X-Content-Type-Options`, `Referrer-Policy`, startup validation.
- **DoS:** unbounded bodies, queries, recursion, memory; timeouts on outbound calls.
- **LLM and agents:** prompt injection, over-privileged tools, model output reaching shell, SQL, HTML, or paths, cross-user leakage.
- **Mobile and extensions:** insecure storage, exported components, deep links, broad permissions.

## Fix Rules

- Fix once, centrally (validator, auth guard, query layer, encoder), not per call site.
- Prefer framework protections; allowlist input at boundaries, encode output by context, apply least privilege.
- A committed secret is compromised: move it to config and tell the user to rotate it.
- Upgrade dependencies via the package manager and check changelogs; otherwise mitigate or replace and record why.
- Never silence scanners or weaken tests; any suppression names the rule and reason inline.

## Output

- Scope, tools run, tools that could not run, and counts by severity (found, fixed, remaining).
- Per finding: ID, severity, CWE, location, attack scenario, fix, proving test.
- Checklist status per category: fixed, clean, not applicable, or unverified.
- User actions: credentials to rotate, platform settings to enable.
- Residual risk and the next step for each.
