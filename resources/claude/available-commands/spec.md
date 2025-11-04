---
description: Create or update technical specification from user story
---

You are creating/updating a technical specification. Follow these steps:

**Input**: $ARGUMENTS (user story ID or path)

**Process**:

1. **Read user story** from `docs/user-stories/` or provided path
2. **Read AGENTS.md** to understand project context and tech stack
3. **Launch spec-writer agent** to create detailed technical spec including:
   - Overview & objectives
   - Technical approach & architecture
   - Data models & API design
   - Implementation steps (breakdown into subtasks)
   - Testing strategy
   - Acceptance criteria

4. **Create spec file** at `docs/specs/SPEC-<US-ID>-<feature-name>.md`

5. **Present spec** to user for review and feedback

**Output**: Technical specification ready for implementation
