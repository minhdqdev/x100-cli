# Product Requirements Document (Lean)

**Product / Project:**  
**Doc Owner:**  
**Status:** Draft | In Review | Approved  
**Last Updated:** <!-- auto-update via CI if possible -->

---

## 0. TL;DR (≤3 bullets)

- Problem & who it hurts:
- What we’re shipping (MVP-in-one-line):
- How we’ll know it worked (North Star + target by date):

---

## 1. Problem / JTBD

- **User / Persona:**
- **Moment / Context:**
- **Job To Be Done (JTBD):**
- **Top pains today:**

**Value Prop (why now / why us):**

<!-- Your unique edge: speed, data, distribution, insight, cost -->

---

## 2. Hypotheses (falsifiable)

- **H1:** If we **\_\_\_**, then **\_\_\_** will increase from _baseline_ to _target_ by _date_.
- **H2:** …
- **Kill Criteria:** Pivot/stop if **\_\_\_** (e.g., activation < 30% after 2 sprints).

---

## 3. MVP Scope (Now / Next / Later)

**Now (MVP, 2–4 bullets):**

-
- **Next (post-MVP):**

- **Later (nice-to-have):**

- **Explicit Non-Goals:**

- ***

## 4. Metrics & Instrumentation

**North Star:**

- Definition:
- Target & date:

**Input Metrics (3):**

- Activation %: baseline → target (rule to act)
- WAU/Retention D7: baseline → target (rule)
- Time-to-Aha / p95 latency / cost per active: baseline → target (rule)

**Event Taxonomy (5–8 events)**
| Event | When it fires | Properties | Owner |
|---|---|---|---|
| app_install | first run | source, version | Analytics |
| signup_success | account created | method, cohort | Growth |
| aha_reached | user achieves core action | feature, time_to_aha | PM |
| … | … | … | … |

---

## 5. Release & Rollout

- **Envs:** dev → staging → prod
- **Feature Flag:** key: `feature.xyz`
- **Canary:** start 5–10% → 50% → 100% (health gates below)
- **Health Gates / Alerts:** error rate < X%, p95 < Y ms, crash < Z%
- **Rollback Path:** flag off + revert `vX.Y` (owner on call)

---

## 6. Non-Functional Budgets (SLOs)

- **Availability:** 99.9% monthly; **Error budget:** 43m
- **Perf:** p95 API < 300 ms
- **Privacy/Security:** least data; OWASP baseline; secrets in vault; SAST/DAST pass
- **Data:** retention table below; residency: **\_\_\_**

**Data Table (collect only what you need)**
| Field | Purpose | Lawful basis | Retention | Notes |
|---|---|---|---|---|
| email | login | contract | 24 mo | hashed at rest |
| … | … | … | … | … |

---

## 7. Risks & Mitigations

| Risk             | Type | Mitigation                     | Owner | Date      |
| ---------------- | ---- | ------------------------------ | ----- | --------- |
| Data correctness | Tech | contract tests + canary shadow | TL    | 2025-\_\_ |
| …                | …    | …                              | …     | …         |

**Risk review cadence:** Weekly in standup (Fri).

---

## 8. Cost Guardrails (FinOps)

- **Ceiling:** ≤ $\_\_\_\_ / mo (run rate)
- **Tagging:** `product=xyz, env, owner`
- **Cost per active user (target):** $\_\_\_\_

---

## 9. Open Questions

- Q1: **\_\_** → **Owner:** **\_ **Due:** \_**
- Q2: **\_\_** → **Owner:** **\_ **Due:** \_**

---

## Links & Appendices (keep separate docs, link here)

- ADRs: `docs/adr/`
- API/UI Specs: `docs/specs/`
- Diagrams (C4): `docs/diagrams/`
- Timeline/Roadmap: `docs/roadmap.md`
- DoR / DoD: `docs/process/dor_dod.md`
- Security checklist/DPIA: `docs/security/`

---

## Changelog

- 2025-09-21: v0.1 initial lean PRD scaffold.
