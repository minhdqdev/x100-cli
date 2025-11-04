---
description: Complete feature development (review, test, commit)
---

You are completing a feature development. Follow these steps:

**Input**: $ARGUMENTS (optional: commit message or feature name)

**Process**:

1. **Run final checks**:
   - Launch code-reviewer agent for final review
   - Run all tests
   - Check linting & type errors
   - Verify build succeeds

2. **If any issues found**:
   - Report to user
   - Ask if they want to fix now or proceed anyway
   - Fix critical issues if user agrees

3. **Prepare commit**:
   - Review all changes with git status & diff
   - Create meaningful commit message following project conventions
   - Include reference to user story/spec if applicable

4. **Commit changes**:
   - Stage all relevant files
   - Create commit with detailed message
   - Add co-author attribution

5. **Ask user** if they want to:
   - Push to remote
   - Create pull request
   - Continue with next task

**Output**: Feature completed and committed
