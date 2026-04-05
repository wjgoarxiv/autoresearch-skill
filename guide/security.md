# autoresearch:security — Iterative Security Audit Engine

## Purpose

`security` performs a structured, iterative security audit using STRIDE threat modeling, OWASP Top-10 checks, and attack surface mapping. It works through 7 phases — scope definition, asset inventory, STRIDE analysis across all 6 categories, OWASP checks across all 10 categories, attack surface synthesis, mitigation proposals, and coverage scoring — then re-audits until the coverage target is reached or the iteration budget is exhausted. Every finding is given a threat ID, severity, likelihood, and a priority level from a severity × likelihood matrix. Every mitigation is tracked with implementation effort and status. Output lives in a `security/` folder with three structured files.

## When to Use

- You want a formal threat model before shipping a new API, service, or feature.
- You need to verify OWASP Top-10 compliance for an audit, certification, or security review.
- You want to find attack surface gaps in a codebase you didn't write.
- You are reviewing an architecture and want to know what a motivated attacker could exploit.
- You want ongoing security posture tracking with `--diff` re-audits on each code change.

## When NOT to Use

- You want to fix known security bugs — use `fix` for systematic error elimination after threats are identified.
- You need a penetration test with actual exploit execution (this is a threat modeling and code audit tool, not an active pen test).
- You want a one-line answer about whether a specific snippet is safe.

## Usage

```
/autoresearch:security
```

You will be asked:
1. What is the target? (codebase path, system description, or architecture diagram)
2. What is the coverage target? (default: 80%)
3. Is this a re-audit with `--diff`? If so, provide the previous `security/` folder.

For re-audits: `--diff` mode skips unchanged components and only re-checks what changed since the last audit, then recalculates coverage.

## Output

| File | Content |
|------|---------|
| `security/threats.md` | All identified threats: STRIDE findings (T-S-001 format) + OWASP results with evidence and priority matrix ratings |
| `security/mitigations.md` | Per-threat mitigation proposals with effort estimates and status (proposed / in-progress / implemented / accepted-risk / wont-fix) |
| `security/coverage-report.md` | Coverage score, gap analysis, addressed vs. unaddressed threat table, accepted risks |

## Example

**Domain:** A Node.js REST API with JWT authentication and a PostgreSQL backend.

- Asset inventory finds: 4 authenticated endpoints, 1 unauthenticated health check, 1 file upload endpoint, JWT secret in environment variable.
- STRIDE surfaces: T-S-001 (spoofing — JWT secret rotated but old tokens not invalidated, High/Medium → P1), T-T-002 (tampering — file upload lacks MIME type validation, High/High → P0).
- OWASP: A01 Broken Access Control — PARTIAL (role checks on 3/4 endpoints), A03 Injection — PASS.
- Attack chain identified: unauthenticated health endpoint leaks version → known CVE for that version → RCE path.
- Phase 6 mitigations: M-T-S-001 (add token revocation list, effort: Medium), M-T-T-002 (MIME validation + file size cap, effort: Low).
- Coverage after iteration 1: 78%. Re-audit pass 1 reaches 85% — target met.

## Tips

- P0 and P1 threats always get mitigations in Phase 6. P2+ are proposed but can be deferred — the coverage score still counts them as addressed if status is `accepted-risk` with justification.
- If STRIDE coverage feels thin, look at the Asset Inventory first. Missed entry points in Phase 2 cascade into missed threats in Phase 3.
- For teams that ship weekly, run `--diff` on every PR rather than a full audit. The incremental mode is fast and keeps `security/threats.md` current without redundant re-checking of stable components.
