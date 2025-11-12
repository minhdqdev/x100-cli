---
description: Run complete automated workflow (spec → code → test → review → done)
---

You are running a complete automated development workflow. Follow these steps:

**Input**: $ARGUMENTS (user story ID or path)

**Workflow**:

1. **START Phase**:
   - Read user story
   - Launch spec-writer agent
   - Create technical specification
   - Get user approval on spec

2. **CODE Phase**:
   - Launch code-implementer agent
   - Implement code following spec
   - Run linting & type checking

3. **TEST Phase**:
   - Launch test-writer agent
   - Create comprehensive tests
   - Run tests and verify all pass
   - Fix any failing tests

4. **REVIEW Phase**:
   - Launch code-reviewer agent
   - Get comprehensive code review
   - Fix critical and high-priority issues
   - Re-run tests after fixes

5. **DONE Phase**:
   - Final verification (tests, linting, build)
   - Create commit with meaningful message
   - Ask user about push/PR

**Note**: This is a fully automated workflow. User will be prompted at key decision points.

**Output**: Feature fully implemented, tested, reviewed, and committed
