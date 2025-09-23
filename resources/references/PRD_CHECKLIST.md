# PRD Quality Checklist (Lean PRD)
Use this checklist to review PRDs based on `.x100/resources/doc-templates/PRD.md` (Lean). Keep it measurable, falsifiable, and rollout-ready.

## Meta
- [ ] `Product / Project` named and scoped
- [ ] `Doc Owner` identified and reachable
- [ ] `Status` set (Draft/In Review/Approved)
- [ ] `Last Updated` filled and current

## 0. TL;DR (≤3 bullets)
- [ ] Problem + who it hurts summarized in one line
- [ ] MVP-in-one-line states the shipped value, not the activity
- [ ] North Star + numeric target + date included

## 1. Problem / JTBD
- [ ] Persona clear with source (research, analytics, interviews)
- [ ] Moment/Context describes when the pain occurs
- [ ] JTBD phrased as progress sought by user
- [ ] Top pains listed and evidenced (qual/quant)
- [ ] Value Prop explains “why now / why us” with differentiators

## 2. Hypotheses (falsifiable)
- [ ] H1 includes intervention, metric, baseline → target, and date
- [ ] Additional hypotheses (H2/H3) optional but falsifiable
- [ ] Kill Criteria defined and action-linked (when to pivot/stop)

## 3. MVP Scope (Now / Next / Later)
- [ ] Now (2–4 bullets) capture smallest end-to-end value
- [ ] Next lists post-MVP increments
- [ ] Later lists nice-to-haves; not needed for approval
- [ ] Explicit Non-Goals listed to prevent scope creep

## 4. Metrics & Instrumentation
- [ ] North Star definition, baseline, target, and date
- [ ] 3 input metrics with baselines → targets and “rule to act”
- [ ] Event Taxonomy table has 5–8 events with owners and properties
- [ ] Feasibility checked: events available Day 1 (or stubbed)
- [ ] Dashboard/query ownership noted for each key metric

## 5. Release & Rollout
- [ ] Environments listed (dev → staging → prod)
- [ ] Feature flag key named (e.g., `feature.xyz`)
- [ ] Canary plan defined (5–10% → 50% → 100%) with criteria
- [ ] Health gates/alerts thresholds set (error rate, p95, crash rate)
- [ ] Rollback path explicit: flag off + revert version + on-call owner

## 6. Non-Functional Budgets (SLOs)
- [ ] Availability target and error budget present (e.g., 99.9%, 43m)
- [ ] Performance budget stated (e.g., p95 API < 300 ms)
- [ ] Privacy/Security baseline: least data, OWASP, secrets in vault, SAST/DAST pass
- [ ] Data residency stated and Data Table filled (purpose, basis, retention)

## 7. Risks & Mitigations
- [ ] Risk table includes Type, Mitigation, Owner, Date
- [ ] Mix of product, tech, delivery, compliance risks
- [ ] Risk review cadence specified (e.g., weekly)

## 8. Cost Guardrails (FinOps)
- [ ] Monthly ceiling set with rationale
- [ ] Tagging standard defined (`product=xyz, env, owner`)
- [ ] Cost per active user target stated (if applicable)

## 9. Open Questions
- [ ] Each question has an Owner and Due date
- [ ] Blockers highlighted if decision needed for MVP

## Links & Appendices
- [ ] ADRs linked (`docs/adr/`) for decisions emerging from PRD
- [ ] API/UI specs linked (`docs/specs/`) or ticketed
- [ ] Diagrams (C4/Mermaid) linked (`docs/diagrams/`)
- [ ] Roadmap/timeline linked (`docs/roadmap.md`)
- [ ] DoR/DoD process doc linked (`docs/process/dor_dod.md`)
- [ ] Security artifacts (checklist/DPIA) linked (`docs/security/`)

## Consistency & Traceability
- [ ] PRD saved at `docs/PRD.md` and matches lean template sections
- [ ] Backlog updated at `docs/PRODUCT_BACKLOG.md` and references PRD
- [ ] User stories in `docs/user-stories/` align to “Now” scope; acceptance criteria reflect metrics
- [ ] Interfaces/NFRs align with `.x100/resources/references/SA_CHECKLIST.md`
- [ ] Links resolve; no placeholder “…” remain where decisions exist

## Review & Sign-off
- [ ] PO self-review complete; ambiguities resolved or tracked in Open Questions
- [ ] Tech Lead review complete; feasibility and instrumentation confirmed
- [ ] Stakeholder review captured (with comment links)
- [ ] Status updated to Approved when sign-offs recorded (with dates)

## Delivery Readiness
- [ ] Feature-flag rollout plan and owners on-call documented
- [ ] Rollback tested in staging or dry-run procedure exists
- [ ] Telemetry implemented or ticketed before enabling canary
- [ ] Launch plan: comms, support runbook owner, release notes owner

## Quality Gates
- [ ] Baselines and targets are numeric and time-bound
- [ ] SLOs and health gates are actionable (wired to alerts)
- [ ] Scope is sliceable to fit into planned sprints
- [ ] Changelog updated; Last Updated refreshed

---

### Quick Triage (Minimum Bar)
- [ ] TL;DR filled with 3 bullets
- [ ] H1 with baseline → target by date
- [ ] “Now” scope lists 2–4 bullets + Non-Goals
- [ ] North Star + 3 input metrics with targets
- [ ] Feature flag, canary plan, health gates, rollback path
- [ ] SLO budgets present; Data Table started
- [ ] Top 3 risks with owners/mitigations and cadence
