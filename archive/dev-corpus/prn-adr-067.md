---
id: prn-adr-067
type: principle
kind: decision
title: ADR D-67 — React Router advisories GHSA-wrjc-x8rr-h8h6 / GHSA-337j-9hxr-rhxg are not reachable in this app — the breaking v7 upgrade is deferred
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-67
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

React Router advisories GHSA-wrjc-x8rr-h8h6 / GHSA-337j-9hxr-rhxg are not reachable in this app — the breaking v7 upgrade is deferred.

## Rationale

`npm audit` in frontend/ reports 2 moderate vulnerabilities against react-router (we pin react-router-dom ^6.30.4; the affected range is 6.0.0–7.17.0), surfaced when the v4 line was first installed on a second machine. Both were assessed rather than auto-remediated. (1) The SSR-hydration advisory (arbitrary constructor injection via deserializeErrors) requires server-side rendering / hydration; this frontend is a pure Vite client build — a repo-wide grep for hydrateRoot / renderToString / StaticRouter / deserializeErrors across frontend/src returns nothing, so the vulnerable code path is never executed. (2) The open-redirect advisory (backslash bypass, CVE-2025-68470 bypass) targets react-router's own `<Link>` and useNavigate. Every redirect sink in this app is a native browser navigation, not router navigation: components/layout/Sidebar.tsx (logout), api/client.ts (401 bounce) and pages/Login.tsx (post-auth return) all call window.location.assign. Because the *class* of attack still applies to this app's own open-redirect control regardless of react-router, that control was attacked empirically rather than reasoned about: pages/Login.tsx's resolveNext() guard (honour `next` only when it startsWith '/app') was driven against the running app with 10 bypass payloads — protocol-relative (//host), backslash (/\host), double-backslash, URL-encoded backslash (%5C), path traversal, tab injection (%09) and an absolute https:// URL. 0 of 10 escaped the origin; every payload landed back on localhost:8501.

## Consequence

No dependency change this cycle. The advisories' only offered remediation is react-router-dom@7.18.1 — a breaking v6→v7 major — which would trade real regression risk across every route, loader and Link in the SPA for no reduction in actual exposure. Practical effects: `npm ci` will keep printing '2 moderate severity vulnerabilities' on every machine; that output is now an expected, assessed condition, not a fresh signal, and should not be treated as a release blocker. Re-open this decision if any of the following changes: SSR or hydration is introduced; any redirect sink migrates from window.location.assign to useNavigate/`<Link>`; resolveNext's prefix-check guard is modified; or a react-router v7 upgrade is scheduled for unrelated reasons. In each case re-run the probe before relying on this entry.

> [!note] Provenance
> Architecture decision **D-67** in the DQ Studio decision registry, decided 2026-07-28, registry status *active*.
