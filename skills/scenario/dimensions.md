# Scenario Dimensions

Reference for `autoresearch:scenario`. Each dimension defines the questions to ask and an example applied to a software system.

---

## Dimension 1: Best Case

**Description:** All assumptions hold, all collaborators perform optimally, and every external condition is favorable. The ceiling of what success looks like.

**Questions to ask:**
- What does complete success look like in concrete terms?
- Which conditions, if all true simultaneously, would produce the best outcome?
- What capabilities or value would be unlocked that currently seem out of reach?
- How quickly could the ideal state be achieved?

**Example (software system):** All services scale elastically with zero downtime, the team ships on the roadmap schedule, adoption exceeds projections by 2×, and no security incidents occur in year one.

---

## Dimension 2: Worst Case

**Description:** Every assumption fails, every risk materializes, and every external factor is adversarial. The floor — not likely, but possible.

**Questions to ask:**
- What is the single most catastrophic outcome?
- Which combination of failures would be unrecoverable?
- What would force a full shutdown or pivot?
- Which dependencies, if lost, would collapse the entire system?

**Example (software system):** A zero-day exploit exposes all user data, the primary cloud provider suffers a week-long outage, and the lead engineer leaves mid-sprint — simultaneously. The product is taken offline for 14 days.

---

## Dimension 3: Most Likely

**Description:** The realistic base case given current knowledge, trends, and historical analogues. Not optimistic, not pessimistic.

**Questions to ask:**
- What does "normal" execution actually look like?
- Which risks are almost certain to materialize in some form?
- Where do timelines typically slip in comparable projects?
- What does the median outcome look like at the 6-month and 1-year mark?

**Example (software system):** Launch is 3 weeks late, one major feature is deferred to v1.1, initial adoption is 60% of projections, and one P1 bug requires a hotfix within the first two weeks.

---

## Dimension 4: Edge Case

**Description:** Boundary conditions and rare-but-valid inputs that reveal hidden assumptions in the design. Not failure — just behavior at the limits.

**Questions to ask:**
- What happens at the extreme ends of the input range (0, max, negative, empty)?
- Which user behaviors violate implicit assumptions in the design?
- What race conditions or concurrency issues emerge under boundary conditions?
- What breaks when two normally-separate components interact at the same moment?

**Example (software system):** A user submits a form with a 10,000-character name. An API is called with an empty array. Two users edit the same record within the same millisecond. The system receives requests at exactly midnight UTC during a time-zone rollover.

---

## Dimension 5: Cascade Failure

**Description:** A single failure triggers a chain of dependent failures, producing an outage larger than any individual component could cause alone.

**Questions to ask:**
- Which single component failure would propagate furthest?
- Where are the shared dependencies that multiple systems rely on?
- Which retry/backoff configurations could amplify load under failure?
- What is the critical path through the system, and what happens if it breaks?

**Example (software system):** The authentication service becomes slow (not down). Every other service starts waiting for auth tokens. Queues fill. CPU spikes. The database connection pool exhausts. The entire system becomes unavailable even though auth itself never fully died.

---

## Dimension 6: Adversarial

**Description:** A motivated, intelligent actor actively tries to break, exploit, manipulate, or abuse the system. Not random failure — intentional attack.

**Questions to ask:**
- What is the highest-value target in this system for an attacker?
- Which trust boundaries can be violated with the least effort?
- What social engineering vectors exist against users or operators?
- If you were the attacker, where would you start?

**Example (software system):** An attacker crafts a request that bypasses input validation, injects SQL into a log aggregation pipeline, and uses the resulting data access to exfiltrate user PII — exploiting a component that was never considered part of the attack surface.

---

## Dimension 7: Time-Compressed

**Description:** Normal timelines are radically shortened by external pressure (regulatory deadline, competitor launch, incident response). Quality-vs-speed tradeoffs become acute.

**Questions to ask:**
- If the timeline were cut in half, what would be cut and what are the consequences?
- Which shortcuts taken under time pressure create long-term technical debt?
- What safety checks would be bypassed under extreme deadline pressure?
- How does team performance degrade under sustained crunch?

**Example (software system):** The product must ship in 2 weeks instead of 8. Code review is eliminated, automated tests are skipped for "non-critical" paths, and the security audit is deferred. Six months later, three of those "non-critical" paths have production bugs.

---

## Dimension 8: Resource-Constrained

**Description:** Key resources — budget, compute, people, time, bandwidth — are cut by 50–90%. What survives? What breaks? What gets creative?

**Questions to ask:**
- Which features require full resources vs. working with minimal resources?
- What degrades gracefully and what collapses under resource reduction?
- Which resource is the true bottleneck, and what happens if it disappears entirely?
- How does the system behave when operating at 10% of expected capacity?

**Example (software system):** Cloud budget is cut 70% mid-quarter. The team must reduce compute by shutting down staging environments, consolidating microservices, and disabling background jobs — discovering that two "separate" services are actually tightly coupled and cannot be co-located.

---

## Dimension 9: Stakeholder Conflict

**Description:** Different stakeholders (users, operators, management, regulators, investors) have mutually incompatible goals, and the system or project must navigate the conflict.

**Questions to ask:**
- Which stakeholders have opposing success criteria?
- Where does optimizing for one group actively harm another?
- What happens when two stakeholders escalate their conflict to a decision-maker?
- Which unspoken political dynamics could derail the project?

**Example (software system):** The security team requires all data to be encrypted at rest, which adds 40ms latency. The product team's SLA requires <100ms response time. Engineering is caught between two mandates with no budget to resolve both. The conflict stalls the roadmap for 6 weeks.

---

## Dimension 10: Regulatory/Compliance

**Description:** Existing or new rules, standards, or enforcement actions constrain what the system can do, how data must be handled, or where it can operate.

**Questions to ask:**
- Which regulations currently apply, and how strictly are they enforced?
- What new regulations are likely in the next 1–3 years in this domain?
- What would a compliance audit find if conducted today?
- Which features would need to be removed or redesigned for a different jurisdiction?

**Example (software system):** GDPR enforcement ramps up. The system's logging infrastructure has been retaining full request bodies (including PII) for 90 days. The team must implement retroactive data minimization and a right-to-deletion pipeline under a 30-day regulatory deadline.

---

## Dimension 11: Long-Term Drift

**Description:** Gradual degradation over 1–5 years as the system ages, the team turns over, dependencies decay, and the original design assumptions become obsolete.

**Questions to ask:**
- What will be unmaintainable 2 years from now if no action is taken?
- Which tribal knowledge, if lost with team turnover, would create critical gaps?
- Which external dependencies are likely to be deprecated or abandoned?
- How does accumulated technical debt compound, and what triggers a reckoning?

**Example (software system):** Three years after launch, the original architect has left. Two key libraries are unmaintained. The test suite is 60% flaky so most developers skip it. A major Node.js version upgrade is required, but no one fully understands the build pipeline. Routine changes take 3× longer than in year one.

---

## Dimension 12: Recovery/Resilience

**Description:** After a failure (any kind), how does the system return to normal? How fast, how completely, and with what residual damage?

**Questions to ask:**
- What is the recovery time objective (RTO) and is the system actually designed to meet it?
- Which failure modes have no documented recovery procedure?
- How is data integrity verified after recovery?
- What lessons from a recovery event are actually captured and acted on?

**Example (software system):** After a database corruption event, the team discovers that the most recent valid backup is 18 hours old (backups were silently failing for a week). Recovery takes 14 hours, and 12 hours of user data is permanently lost. The incident reveals no runbook existed for this failure mode.
