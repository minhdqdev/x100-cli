---
description: Implement code from technical specification
---

You are implementing code from a technical specification. Follow these steps:

**Input**: $ARGUMENTS (spec file path or feature name)

**Process**:

1. **Read the technical spec** from `docs/specs/` or provided path
2. **Read AGENTS.md** to understand project structure and conventions
3. **Launch code-implementer agent** to:
   - Implement code following the spec
   - Follow project coding standards and conventions
   - Create/update necessary files
   - Add appropriate error handling
   - Add code comments where needed

4. **Run linting & type checking** if applicable

5. **Present changes** summary to user

**Note**: This only implements code, does NOT create tests. Use `/test` command for that.
