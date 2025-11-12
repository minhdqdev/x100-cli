# Product Requirements Document — Startup Edition

> **Ultra-Lean Mode (<5 people):** Use sections 0-4 + 9 only. Skip 5-8 or write brief bullets.  
> **Standard Mode:** Fill all sections, but write `N/A` with rationale if not relevant.  
> **Tip:** Link to supporting docs (Figma, Loom, ADRs) instead of duplicating content.

## 0. Quick Snapshot
| Item | Details |
| --- | --- |
| DRI / Date |  |
| Team members involved |  |
| Problem statement (1–2 sentences) |  |
| Hypothesis / why now |  |
| Success signal (what we expect to happen) |  |

## 1. Customer Problem & Opportunity
- **Customer / segment:** who experiences the pain?  
- **Evidence:** key data points, research, user quotes, support volume, etc.  
- **Pain today:** what breaks, how big is the impact, frequency.  
- **Opportunity / business impact:** revenue, retention, cost, strategic bet.  
- **Assumptions to validate:** primary unknowns or leaps of faith.

## 2. Goals, Outcomes & Metrics
| Metric (KPI) | Baseline | Target | Measurement source & frequency |
| --- | --- | --- | --- |
| e.g., Activation rate | 32% | 45% within 2 months | Amplitude dashboard `#123` (weekly) |

> Include at least one leading metric (customer behavior) and one lagging metric (business impact). Define how success/failure is declared.

## 3. Users & Journeys
> **Small team tip:** If you're building for yourselves or know users intimately, brief bullets suffice. Skip formal personas.

- **Target users:** who they are, their goal, key motivation.  
- **Secondary users / blockers:** anyone who can veto or needs special consideration.  
- **Core journeys:** list 2–3 most important flows with happy path + acceptance criteria.

| Journey | Trigger & goal | Acceptance criteria | Notes |
| --- | --- | --- | --- |
|  |  |  |  |

## 4. Scope & Requirements
### Prioritized backlog (MoSCoW or RICE order)
| Priority | Description | Acceptance criteria / tests | DRI | Effort |
| --- | --- | --- | --- | --- |
| Must |  |  |  |  |
| Should |  |  |  |  |
| Could |  |  |  |  |

- **Non-goals / explicitly out of scope:** list to avoid scope creep.
- **Open questions:** call out unknowns blocking commitment.

## 5. Solution Outline
> **Ultra-lean:** Brief bullets or links only. Skip if obvious.

- **Product experience:** short narrative or bullets; link to wireframes, demos.  
- **System approach:** describe key approach, reference diagrams or sketches.  
- **Data impact:** new entities or changes; link to ERD if relevant.  
- **Alternatives considered:** why this option wins (optional for small teams).  
- **Impact radius:** feature flags, migrations, users affected.

## 6. Implementation & Quality Notes
> **Small team tip (<10 people):** Keep brief or skip. Write N/A for sections that don't apply yet.

- **Architecture highlights:** key components, APIs, infrastructure changes.  
- **Dependencies:** external services, 3rd parties, other features.  
- **Performance & cost:** any targets or constraints worth noting.  
- **Security & privacy:** sensitive data handling, auth changes, compliance (if relevant).  
- **Monitoring:** key metrics or alerts to add (skip detailed runbooks unless critical).

## 7. Testing & Rollout
> **Small team tip:** Merge with section 8 if you have simple release process.

- **Test approach:** unit, integration, manual testing plan; beta users if applicable.  
- **Test data / environments:** staging setup, feature flags, test accounts.  
- **Rollback plan:** what signals "stop" and how to revert quickly.

## 8. Launch Plan
> **Small team tip:** Simple timeline + communication plan is often enough.

| Milestone | DRI | Target date | Notes |
| --- | --- | --- | --- |
| MVP ready |  |  |  |
| Beta / internal testing |  |  |  |
| Public launch |  |  |  |

- **Release approach:** all-at-once, phased rollout, or feature flag.  
- **User communication:** who needs to know, how to announce, docs to update.  
- **Post-launch:** what to track, when to review results (1 week? 1 month?).

## 9. Risks, Mitigations & Decisions
- **Top risks:** list severity + mitigation / contingency.  
- **Critical assumptions:** how and when they will be validated.  
- **Key decisions & status:** maintain a mini-ADR table (link to `/docs/adrs/` if formal).

## 10. Appendices & Links
- Glossary, analytics dashboards, Figma boards, Looms, backlog link, experiment plan.  
- **Skipped sections:** Note which sections you skipped and why (e.g., "Skipped formal personas—we're building for ourselves").
