---
name: test-local-app-end-to-end
description: Run, inspect, and verify local web applications end to end with standalone Playwright in a disposable browser session. Use automatically when the user asks to launch or reuse a local dev server, open or test a local app in Chrome, exercise visible routes and controls, test uploads or multi-service flows, inspect browser console or network failures, correlate frontend and backend logs, fix reproducible UI defects, or retest repaired application behaviour.
---

# Test Local App End to End

Test the real application through standalone Playwright with a disposable browser profile, not only through HTTP requests or unit tests. Combine browser interaction with focused automated checks and log inspection, then report exactly what was exercised and what remains unverified.

## Workflow

### 1. Establish the running system

- Read repository instructions and package scripts before running commands.
- Inspect current listeners, relevant processes, health endpoints, and recent logs.
- Reuse an already healthy instance. Do not start duplicate frontend or backend servers on the same ports.
- When no healthy instance exists, run the repository's declared development command from its required working directory. Preserve separate visible terminals when the user asked for them or needs to control them.
- When starting a server, capture the local URL and give it to the user after implementation or verification.
- Treat shell process output and log files as the source for terminal diagnostics. Do not claim visual access to an OS terminal window unless an OS-control tool is actually available.

### 2. Prepare disposable Playwright automation

- Prefer the repository's existing Playwright installation, configuration, fixtures, and test conventions.
- If Playwright is absent and browser testing is requested, add the narrowest suitable development dependency and a minimal configuration. Install only the required disposable browser runtime.
- Use a fresh context or temporary user-data directory. Never attach to or inspect a personal browser profile, cookies, passwords, saved sessions, local storage, or unrelated tabs.
- Use the installed Chrome channel when compatible and requested; otherwise use Playwright Chromium. Keep the profile disposable in either case.
- Capture console errors, uncaught page errors, failed requests, unexpected HTTP responses, screenshots, and traces. Treat unexpected browser diagnostics as test failures.
- Keep durable end-to-end tests in the repository when they protect important workflows. Use temporary exploratory scripts only when repository tests would add no lasting value.

### 3. Build a coverage inventory

- Enumerate routes, navigation entries, buttons, links, forms, inputs, file pickers, menus, dialogs, tabs, filters, disclosures, keyboard interactions, exports, copy actions, themes, responsive navigation, empty states, error states, and data visualisations.
- Identify destructive actions before clicking. Exercise their dialog and cancellation path against user data. Test confirmed deletion only in an isolated database, schema, account, or disposable fixture.
- Select representative valid, duplicate, malformed, empty, and unsupported inputs when the product supports them.
- Include accessibility names, focus behaviour, loading states, and narrow and wide viewports where relevant.

### 4. Exercise complete flows

- Interact through Playwright as a user would, using roles, labels, accessible names, and visible text before CSS selectors. Use DOM-backed inspection only to understand visible or interactive state and to verify results.
- For uploads, verify selection, request transmission, parsing or OCR, ingestion, deduplication, persistence, embeddings, analysis, and visible UI feedback.
- For LLM flows, verify the outgoing request, successful structured response, parsing, persistence where applicable, citation or evidence linkage, and correct frontend rendering.
- For graphs and other visualisations, inspect the actual rendered view, node and edge presence, labels, selection, filtering, fit or reset controls, and empty states.
- After each major flow, inspect new console errors, failed requests, status codes, response payloads, and relevant application logs.
- Prefer temporary or already duplicated fixtures for physical UI tests. Keep user data intact unless the user explicitly authorises mutation or deletion.
- Match selectors to user intent. Prefer roles, labels, accessible names, and visible text because those failures usually reveal real usability defects.

### 5. Diagnose and repair

- Reproduce each defect before editing.
- Trace the smallest failing boundary: interaction, frontend state, request, API validation, storage, parser or OCR, embedding, LLM, or rendering.
- Make surgical changes that match repository conventions. Preserve unrelated user edits.
- Run the narrowest relevant automated test first, then the broader suite appropriate to the risk.
- Retest the exact Playwright path after the fix. A code change without browser confirmation does not close a UI defect.

### 6. Finish with evidence

- Summarise routes and workflows physically exercised, automated checks run, defects fixed, and data intentionally not mutated.
- Separate verified results from assumptions and blockers.
- Do not promise perfection. Claim production readiness only for the tested configuration and state remaining environmental gaps such as unavailable Docker, third-party services, browsers, credentials, or deployment infrastructure.
