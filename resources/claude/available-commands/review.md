---
description: Review recent code changes for quality and best practices
---

You are reviewing recent code changes. Follow these steps:

**Input**: $ARGUMENTS (optional: specific files or directories to review)

**Process**:

1. **Identify changes** using git diff or specified files
2. **Launch code-reviewer agent** to perform comprehensive review:
   - Code quality assessment
   - Security vulnerabilities
   - Performance issues
   - Type safety & linting
   - Best practices adherence
   - Alignment with project standards

3. **Present review report** with prioritized findings:
   - Critical issues (must fix)
   - High priority improvements
   - Medium priority suggestions
   - Positive observations

4. **Ask user** if they want to fix any issues now

**Output**: Comprehensive code review report
