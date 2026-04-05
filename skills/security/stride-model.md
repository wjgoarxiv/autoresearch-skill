# STRIDE Threat Model Reference

Six categories of threats, originally defined by Microsoft. Used in Phase 3 of the `autoresearch:security` audit. For each entry point and trust boundary identified in Phase 2, apply every category systematically.

---

## S — Spoofing

**Definition:** An attacker impersonates a legitimate user, service, or component to gain unauthorized access or trust.

**What it threatens:** Authentication — the system's ability to verify "who are you?"

**Example attacks:**
- Forging a JWT token with a weak or exposed secret
- ARP spoofing to intercept traffic between services
- DNS spoofing to redirect requests to a malicious server
- Session fixation — forcing a user to use an attacker-controlled session ID
- Replaying captured authentication tokens after they should have expired

**Detection methods:**
- Check: Is authentication enforced at every entry point?
- Check: Are tokens/sessions signed and validated server-side?
- Check: Is there token expiry and rotation?
- Check: Does the system verify the identity of downstream services it calls?

**Standard mitigations:**
- Enforce strong authentication (MFA where risk warrants)
- Use short-lived, signed tokens (JWT with RS256, not HS256 with shared secret)
- Implement mutual TLS (mTLS) for service-to-service calls
- Validate token audience (`aud` claim) to prevent token reuse across services
- Use anti-replay mechanisms (nonce, timestamp validation)

---

## T — Tampering

**Definition:** An attacker modifies data in transit or at rest without authorization.

**What it threatens:** Integrity — the system's guarantee that data has not been altered.

**Example attacks:**
- SQL injection to modify database records
- Man-in-the-middle attack to alter HTTP requests/responses
- Modifying a signed URL or cookie without detection (if signing is weak)
- Path traversal to overwrite files outside the intended directory
- Prototype pollution in JavaScript to modify shared objects

**Detection methods:**
- Check: Is all input validated before use in queries or file operations?
- Check: Are sensitive objects immutable or signed?
- Check: Is TLS enforced for all data in transit?
- Check: Are database writes access-controlled (least privilege)?

**Standard mitigations:**
- Parameterized queries / prepared statements for all database access
- Input validation: allowlist over blocklist, validate type + length + format
- HMAC or digital signatures for any data the client can modify and send back
- Enforce TLS 1.2+ with HSTS; reject downgrades
- Immutable audit logs with append-only access controls

---

## R — Repudiation

**Definition:** An attacker performs an action and then credibly denies having done it, because the system cannot prove it happened.

**What it threatens:** Non-repudiation — the system's ability to prove who did what.

**Example attacks:**
- Deleting or altering log files after performing a malicious action
- Using a shared account so the action cannot be attributed to a specific user
- Exploiting a system with no audit trail to perform unauthorized operations
- Uploading malicious content and claiming it came from another user

**Detection methods:**
- Check: Are all sensitive actions (auth, data modification, privilege changes) logged?
- Check: Are logs tamper-resistant (append-only, off-host)?
- Check: Do logs include sufficient attribution (user ID, IP, timestamp, action)?
- Check: Are shared accounts or anonymous operations permitted where they shouldn't be?

**Standard mitigations:**
- Append-only audit logs written to a separate, access-controlled store
- Log all authentication events, authorization decisions, and data modifications
- Include: timestamp (UTC), actor identity, action, target resource, outcome
- Digital signatures on critical log entries
- Ship logs to external SIEM — do not rely solely on local log files

---

## I — Information Disclosure

**Definition:** An attacker gains access to information they are not authorized to see.

**What it threatens:** Confidentiality — the system's ability to keep data private.

**Example attacks:**
- Verbose error messages that expose stack traces, database schemas, or internal paths
- Insecure direct object reference (IDOR) — accessing another user's data by changing an ID
- Sensitive data stored in plaintext (credentials in config files, PII in logs)
- Overly broad API responses that return fields the caller doesn't need
- Directory listing enabled on a web server exposing file structure

**Detection methods:**
- Check: Do error responses expose internal implementation details?
- Check: Is authorization checked before returning user-specific resources?
- Check: Are secrets and PII excluded from logs?
- Check: Are API responses filtered to the minimum required fields?
- Check: Is sensitive data encrypted at rest?

**Standard mitigations:**
- Generic error messages to users; detailed errors to logs only
- Authorization checks on every resource access (not just authentication)
- Secrets management: environment variables, secret vaults (not hardcoded)
- Encrypt sensitive fields at rest (AES-256 minimum)
- Principle of least privilege: APIs return only what the caller is authorized to see
- TLS for all data in transit; HSTS to prevent downgrade

---

## D — Denial of Service

**Definition:** An attacker degrades or eliminates the availability of the system for legitimate users.

**What it threatens:** Availability — the system's ability to serve legitimate users.

**Example attacks:**
- Flooding endpoints with requests (volumetric DDoS)
- ReDoS (Regular Expression Denial of Service) — crafted input causes catastrophic regex backtracking
- Resource exhaustion: uploading huge files, creating deeply nested JSON, long strings
- Slowloris: holding connections open without completing requests
- Hash collision attacks in poorly-designed hash maps

**Detection methods:**
- Check: Are there rate limits on public endpoints?
- Check: Are file upload sizes bounded?
- Check: Are request body sizes bounded?
- Check: Are regex patterns tested against adversarial inputs?
- Check: Are expensive operations (DB queries, external calls) protected against amplification?

**Standard mitigations:**
- Rate limiting per IP and per authenticated user
- Request body size limits (enforce at ingress, not just application layer)
- Timeouts on all external calls and database queries
- Circuit breakers for downstream dependencies
- Avoid complex regex on untrusted input; use linear-time alternatives
- CDN + WAF for volumetric DDoS at the edge

---

## E — Elevation of Privilege

**Definition:** An attacker gains permissions or capabilities beyond what they are authorized for.

**What it threatens:** Authorization — the system's ability to enforce what authenticated users are allowed to do.

**Example attacks:**
- Horizontal privilege escalation: accessing another user's resources at the same privilege level
- Vertical privilege escalation: a regular user gaining admin capabilities
- Mass assignment: sending extra fields in a request that the server applies without checking
- SSRF (Server-Side Request Forgery): using the server as a proxy to reach internal services
- JWT algorithm confusion: changing `alg: RS256` to `alg: none` to bypass signature verification

**Detection methods:**
- Check: Is authorization checked for every action, not just at login?
- Check: Are admin functions protected by role checks, not just login state?
- Check: Is mass assignment prevented (allowlist of writable fields)?
- Check: Are outbound requests from the server restricted to expected destinations?
- Check: Is JWT algorithm explicitly enforced server-side?

**Standard mitigations:**
- Role-based or attribute-based access control (RBAC/ABAC) enforced server-side
- Never trust client-supplied role or permission claims without re-verification
- Allowlist writable fields in update operations (block mass assignment)
- Restrict server-side outbound requests: allowlist of permitted destinations
- Enforce JWT algorithm: reject tokens where `alg` is not the expected value
- Principle of least privilege: every component operates with minimum required permissions

---

## STRIDE Quick Reference

| Letter | Threat | Property Violated | Key Question |
|--------|--------|------------------|--------------|
| S | Spoofing | Authentication | Can the system verify who is calling? |
| T | Tampering | Integrity | Can the system detect unauthorized data modification? |
| R | Repudiation | Non-repudiation | Can the system prove who did what? |
| I | Information Disclosure | Confidentiality | Can the system prevent unauthorized data access? |
| D | Denial of Service | Availability | Can the system resist resource exhaustion? |
| E | Elevation of Privilege | Authorization | Can the system enforce what callers are allowed to do? |
