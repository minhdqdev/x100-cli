# AI Agent Environment Guide

## Project Snapshot

- **Name:** [PROJECT_NAME]
- **Stack:** [TECH_STACK]
- **Key docs:** `README.md`, `docs/PRD.md`, `docs/PRODUCT_BACKLOG.md`, `docs/user-stories/`, `.x100/steering/`

### Shared Tooling

- Project automation scripts under `.x100/scripts/`
- AI steering files under `.x100/steering/` provide persistent project knowledge
- Always ensure docs/ artifacts stay consistent (PRD → Backlog → Stories)

## AI Steering Files

This project uses AI steering files located in `.x100/steering/` to provide persistent knowledge about:

- **Foundation files** (always included):
  - `product.md` - Product vision and goals
  - `tech.md` - Technology stack
  - `structure.md` - Project organization

- **Strategy files** (conditionally included):
  - `api-standards.md` - REST conventions, authentication
  - `testing-standards.md` - Test patterns and coverage
  - `code-conventions.md` - Naming and style guides
  - `security-policies.md` - Security best practices
  - `deployment-workflow.md` - Deployment procedures

These files are automatically loaded based on context. You can also reference them explicitly with `#filename` syntax (e.g., `#api-standards`).

## Instructions for Agents

### Executing project tasks

Use this workflow for coding, bug fixes, and documentation tasks.

1. **Understand context**
   - Read PRD, Technical Guideline, relevant docs, and codebase
   - Review steering files for project conventions (`.x100/steering/`)
   - Check user story acceptance criteria

2. **Plan output**
   - For code, outline steps vs. acceptance criteria
   - For docs, adhere to templates in `.x100/resources/doc-templates/`
   - Follow conventions from steering files

3. **Execute**
   - Update relevant files; keep feedback loop short—commit small, complete units
   - Apply patterns from `code-conventions.md` and `api-standards.md`
   - Follow security guidelines from `security-policies.md`

4. **Validate**
   - Run lint/test commands for touched areas
   - Follow testing standards from `testing-standards.md`
   - Update docs & telemetry checklists when needed

5. **Document**
   - Update comments section in user story file to brief what was done technically
   - Update `docs/CHANGELOG.md`, `docs/PRODUCT_BACKLOG.md`
   - Keep steering files updated if conventions change

### Test

Use this workflow when user requests testing.

1. **Understand context**
   - Read PRD, Technical Guideline, relevant docs, and codebase
   - Review `testing-standards.md` for test patterns and coverage requirements

2. **Run tests**
   - Run unit/integration tests locally
   - Follow test structure from `testing-standards.md` (AAA pattern)

3. **Identify gaps**
   - Identify untested areas in the codebase
   - Check against coverage requirements (>80% overall, >90% business logic)

4. **Suggest improvements**
   - Suggest tests to cover gaps
   - Ensure tests follow project conventions

### Documentation

Use this workflow for documentation tasks.

1. **Understand context**
   - Read PRD, Technical Guideline, relevant docs, and codebase
   - Review steering files for documentation standards

2. **Identify needs**
   - Identify outdated or missing documentation
   - Check if steering files need updates

3. **Create/update docs**
   - Suggest updates or new docs, adhering to templates in `.x100/resources/doc-templates/`
   - Update steering files if project conventions have changed
   - Ensure documentation matches actual implementation

4. **Maintain consistency**
   - Update `docs/CHANGELOG.md` and relevant docs
   - Keep docs/ artifacts consistent (PRD → Backlog → Stories)

### Code Review

Use this workflow when reviewing code or pull requests.

1. **Review against standards**
   - Check code follows `code-conventions.md`
   - Verify API implementations match `api-standards.md`
   - Ensure security practices from `security-policies.md` are followed
   - Confirm tests meet `testing-standards.md` requirements

2. **Check documentation**
   - Verify documentation is updated
   - Ensure steering files reflect any new conventions

3. **Provide feedback**
   - Reference specific steering files in feedback (e.g., "See `api-standards.md` section on error handling")
   - Suggest improvements aligned with project conventions

## Workflow Automation

This project includes workflow automation commands. Use:

- `/workflow` - Complete feature workflow (start → spec → code → test → review → done)
- `/start` - Start feature development from user story
- `/spec` - Create technical specification
- `/code` - Implement code from spec
- `/test` - Create and run tests
- `/review` - Comprehensive code review
- `/done` - Complete feature and commit

For detailed workflow guide, see `.x100/resources/WORKFLOW.md`

## Best Practices

1. **Always reference steering files** - They contain the source of truth for project conventions
2. **Keep context manageable** - Focus on relevant files and sections
3. **Update as you go** - If conventions change, update steering files
4. **Explain reasoning** - When deviating from conventions, document why
5. **Test thoroughly** - Follow testing standards for all code changes
6. **Document decisions** - Use ADRs (Architecture Decision Records) for significant choices

## Common Commands

```bash
# Enable workflow automation
.x100/x100 workflow-enable

# View available commands
.x100/x100 command list

# View available agents
.x100/x100 agent list

# Run full feature workflow
/workflow docs/user-stories/US-XXX-feature.md

# Quick bug fix workflow
/code "Fix issue description"
/test
/review
/done "fix: description"
```

## References

- [Steering Files Guide](.x100/steering/README.md) - Learn about AI steering files
- [Workflow Guide](.x100/resources/WORKFLOW.md) - Detailed workflow documentation
- [Technical Guidelines](.x100/resources/references/TECHNICAL_GUIDELINE.md) - Technical standards
- [Spec-Driven Development](spec-driven.md) - Development methodology (if exists)

---

*This file provides guidance for AI agents working on this project. Update it as the project evolves.*
