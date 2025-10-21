# AI Agent Environment Guide

**Key docs:** `docs/PROJECT_CONTEXT.md`, `README.md`, `docs/PRD.md`, `docs/PRODUCT_BACKLOG.md`, `docs/user-stories/`, `.x100/resources/references/TECHNICAL_GUIDELINE.md`

### Shared Tooling

- Docker compose services under `submodules/*/deploys/`
- Always ensure docs/ artifacts stay consistent (PRD → Backlog → Stories)

## Instructions for Agents

### Executing project tasks

Use this workflow only when user ask to implement US or Epic.

1. **Understand context**
   Read PRD, Technical Guideline, relevant docs, and codebase.
2. **Plan output**
   For code, outline steps vs. acceptance criteria. For docs, adhere to templates in `.x100/resources/doc-templates/`.
3. **Execute**
   Update relevant files; keep feedback loop short—commit small, complete units.
4. **Validate**
   Run lint/test commands for touched areas. Update docs & telemetry checklists when needed.
5. **Document**
   Update comments section in user story file to brief what was done technically.
   Update `docs/PRODUCT_BACKLOG.md` and relevant docs.
   Append change(s) to `docs/AGENT_CHANGELOG.md`

### Test

Use this workflow only when user requests testing.

1. **Understand context**
   Read PRD, Technical Guideline, relevant docs, and codebase.
2. Run unit/integration tests locally.
3. Identify untested areas in the codebase.
4. Suggest tests to cover gaps.

### Documentation

1. **Understand context**
   Read PRD, Technical Guideline, relevant docs, and codebase.
2. Identify outdated or missing documentation.
3. Suggest updates or new docs, adhering to templates in `.x100/resources/doc-templates/`.
4. Update `docs/AGENT_CHANGELOG.md` and relevant docs.
