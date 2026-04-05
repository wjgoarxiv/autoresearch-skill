# OWASP Top 10 (2021) Checklist

Reference for Phase 4 of the `autoresearch:security` audit. For each category, verify all check items by reading code or reviewing architecture. Mark each category PASS / FAIL / PARTIAL / N/A.

A category is **PASS** only if all applicable check items are verified.
A category is **PARTIAL** if some checks pass and others cannot be verified.
A category is **N/A** only if the category is structurally inapplicable (document why).

---

## A01 — Broken Access Control

**What it is:** The application fails to enforce what authenticated users are allowed to do. Users can access data or functions beyond their intended permissions.

**Check items:**
1. Every API endpoint that returns user-specific data performs an authorization check — not just an authentication check. Verify that ownership/role is validated before returning resources (look for patterns like `if resource.owner_id != current_user.id`).
2. Admin-only endpoints (user management, configuration, bulk operations) are protected by explicit role checks, not merely by being "hidden" from the UI.
3. CORS policy is restrictive: `Access-Control-Allow-Origin` is not set to `*` for authenticated endpoints. Allowed origins are an explicit allowlist.
4. Directory listing is disabled on all web-accessible paths. Static file servers do not expose `.git`, `.env`, or backup files.
5. JWT tokens and session tokens cannot be reused after logout. Server-side token invalidation exists.

---

## A02 — Cryptographic Failures

**What it is:** Sensitive data is exposed due to weak or absent encryption — in transit, at rest, or in processing.

**Check items:**
1. All data in transit uses TLS 1.2 or higher. HTTP-only endpoints do not exist for authenticated or sensitive routes. HSTS header is present.
2. Passwords are hashed with a modern adaptive algorithm: bcrypt, scrypt, Argon2, or PBKDF2. MD5, SHA-1, and plain SHA-256 are not used for password storage.
3. Sensitive fields at rest (PII, payment data, credentials, tokens) are encrypted. Encryption uses AES-256 or equivalent; keys are not stored in the same location as encrypted data.
4. Cryptographic keys and secrets are not hardcoded in source code, config files, or version control. Secret management (environment variables, vault) is used.
5. Random values used for security purposes (tokens, session IDs, nonces) are generated with a cryptographically secure RNG, not `Math.random()` or `random.random()`.

---

## A03 — Injection

**What it is:** Untrusted data is sent to an interpreter (SQL, shell, LDAP, XML, etc.) as part of a command or query, causing unintended execution.

**Check items:**
1. All database queries use parameterized queries or prepared statements. String concatenation to build SQL queries does not exist (search for `f"SELECT`, `"SELECT " +`, `query.format(`, `% user_input`).
2. Shell commands constructed from user input use argument arrays, not string interpolation (e.g., `subprocess(["cmd", arg])` not `subprocess(f"cmd {arg}", shell=True)`).
3. Template engines are used in auto-escaping mode. User input is never passed directly to `eval()`, `exec()`, or equivalent dynamic code execution functions.
4. XML parsers have external entity processing (XXE) disabled. DTD processing is disabled or the parser is explicitly configured to reject external entities.
5. ORM-level raw query escape hatches (`raw()`, `execute()`, `query()`) are audited — each use is reviewed to confirm input is parameterized or sanitized.

---

## A04 — Insecure Design

**What it is:** Fundamental design flaws that cannot be fixed by correct implementation alone — the architecture itself lacks security controls.

**Check items:**
1. Rate limiting exists for authentication endpoints (login, password reset, OTP verification). Brute-force attacks are not feasible at current limits.
2. Password reset flows use time-limited, single-use tokens sent to verified channels. They do not rely on security questions or predictable tokens.
3. Business logic enforces server-side invariants that cannot be violated by manipulating client-sent data (e.g., price validation, quantity limits, balance checks happen on the server).
4. Sensitive workflows (account deletion, large transfers, privilege changes) require re-authentication or a secondary confirmation step.
5. The system has a documented threat model. Security requirements were considered at design time, not only during implementation.

---

## A05 — Security Misconfiguration

**What it is:** Insecure default settings, incomplete configurations, open cloud storage, unnecessary features, or misconfigured security headers.

**Check items:**
1. Security headers are present on all HTTP responses: `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`.
2. Default credentials are changed. Frameworks and services are not deployed with factory passwords, default admin accounts, or sample applications.
3. Error responses do not expose stack traces, internal paths, database names, framework versions, or server software to external clients.
4. Unnecessary features, services, and ports are disabled. The attack surface is minimized (no debug endpoints in production, no admin UIs on public ports).
5. Dependencies are up to date. No known-vulnerable versions of frameworks, libraries, or runtimes are in use. Dependency scanning runs in CI.

---

## A06 — Vulnerable and Outdated Components

**What it is:** Using components (libraries, frameworks, runtime) with known vulnerabilities, or failing to track component versions.

**Check items:**
1. A software bill of materials (SBOM) or dependency manifest exists and is version-pinned (`package-lock.json`, `poetry.lock`, `go.sum`, `Cargo.lock`).
2. Automated vulnerability scanning runs in CI (e.g., `npm audit`, `pip-audit`, `trivy`, `snyk`, `dependabot`). Known critical/high vulnerabilities in direct dependencies are resolved.
3. Components are updated on a regular cadence. No dependency is more than 2 major versions behind its current release.
4. Unused dependencies are removed. The dependency tree does not contain packages that serve no active purpose.
5. Container base images are scanned for OS-level CVEs. Images are not based on `latest` tags — they pin specific versions.

---

## A07 — Identification and Authentication Failures

**What it is:** Weaknesses in authentication allow attackers to compromise passwords, keys, session tokens, or to assume other users' identities.

**Check items:**
1. Passwords must meet minimum complexity requirements. Common passwords are rejected (check against a blocklist). Maximum length is not set too low (allow >= 64 characters).
2. Multi-factor authentication (MFA) is available and enforced for privileged accounts. Admin interfaces require MFA.
3. Session tokens are sufficiently random (>= 128 bits of entropy), rotated after login, invalidated on logout, and expire after a reasonable idle timeout.
4. Login failures do not reveal whether the username or the password was incorrect (generic "invalid credentials" message for both cases).
5. The application is not vulnerable to credential stuffing: account lockout or progressive delay exists after N failed attempts, and/or CAPTCHA is used for automated abuse prevention.

---

## A08 — Software and Data Integrity Failures

**What it is:** Code and infrastructure that does not protect against integrity violations — unsigned updates, insecure deserialization, CI/CD pipeline tampering.

**Check items:**
1. Dependencies are fetched from trusted registries with integrity verification (checksums, SRI hashes). `npm install --ignore-scripts` or equivalent prevents malicious postinstall scripts.
2. Serialized objects from untrusted sources (cookies, API inputs) are not deserialized into live objects without type-safe validation. Languages with unsafe deserialization (Java, Python pickle, PHP unserialize) are audited.
3. CI/CD pipelines are protected: secrets are injected via environment, not baked into images; pipeline configs are version-controlled and protected from unauthorized modification.
4. Software updates use signed artifacts. If the application auto-updates components, it verifies signatures before applying.
5. Critical data received from clients is re-validated server-side. The server does not trust the client's representation of computed values (prices, totals, checksums).

---

## A09 — Security Logging and Monitoring Failures

**What it is:** Insufficient logging, monitoring, and alerting allows attackers to operate undetected for extended periods.

**Check items:**
1. Authentication events are logged: successful logins, failed logins, logouts, password resets. Each event includes: timestamp (UTC), user identifier, source IP, user agent, outcome.
2. Authorization failures are logged: access denied events, attempts to reach unauthorized resources. These are monitored for anomalies (repeated failures = potential enumeration or escalation attempt).
3. Sensitive data operations are logged: creation, modification, and deletion of sensitive records. The audit trail is append-only and cannot be modified by application-level users.
4. Logs are shipped to a centralized system (SIEM, log aggregator) that is separate from the application servers. An attacker who compromises the application cannot delete the logs.
5. Alerting exists for critical security events: multiple failed logins, impossible travel, bulk data export, new admin account creation. Alerts have defined response procedures.

---

## A10 — Server-Side Request Forgery (SSRF)

**What it is:** The application fetches a remote resource using a URL supplied by an attacker, allowing the attacker to reach internal services, metadata endpoints, or other restricted destinations.

**Check items:**
1. User-supplied URLs are validated against an allowlist of permitted schemes (`https` only) and hostnames before the server makes any outbound request.
2. Internal network ranges are blocked from user-controlled URL targets: `169.254.0.0/16` (cloud metadata), `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`, `::1`.
3. Cloud provider metadata endpoints are not reachable via user-controlled URLs. AWS `169.254.169.254`, GCP `metadata.google.internal`, Azure `169.254.169.254` are explicitly blocked.
4. DNS rebinding mitigations exist: the IP address is resolved once and validated before the connection is made; re-resolution is not allowed after validation.
5. Outbound HTTP clients are configured with explicit allowlists or egress firewall rules. The application cannot make arbitrary outbound requests to unchecked destinations.

---

## OWASP Quick Reference Table

| ID | Category | Core Risk | CWE References |
|----|----------|-----------|----------------|
| A01 | Broken Access Control | Authorization bypass | CWE-200, CWE-284, CWE-285 |
| A02 | Cryptographic Failures | Data exposure | CWE-261, CWE-296, CWE-310 |
| A03 | Injection | Command execution | CWE-77, CWE-78, CWE-89 |
| A04 | Insecure Design | Architectural flaws | CWE-657, CWE-840 |
| A05 | Security Misconfiguration | Default/open settings | CWE-2, CWE-16 |
| A06 | Vulnerable Components | Known CVEs | CWE-1035, CWE-1104 |
| A07 | Auth Failures | Account compromise | CWE-287, CWE-306 |
| A08 | Integrity Failures | Tampered artifacts | CWE-345, CWE-502 |
| A09 | Logging Failures | Undetected attacks | CWE-117, CWE-223 |
| A10 | SSRF | Internal access | CWE-918 |
