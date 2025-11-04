# x100 Workflow Automation Guide

This guide explains how to use x100's workflow automation system to streamline your development process from user story to production-ready code.

## Overview

x100 provides a complete automated workflow system that orchestrates the entire development lifecycle:

```
User Story → Spec → Code → Test → Review → Done
```

## Quick Start

### 1. Enable Workflow

First, enable all workflow commands and agents:

```bash
./x100 workflow-enable
```

This will activate:
- **Commands**: `/start`, `/spec`, `/code`, `/review`, `/test`, `/done`, `/workflow`
- **Agents**: `spec-writer`, `code-implementer`, `test-writer`, `workflow-orchestrator`

### 2. Run Your First Workflow

```bash
# In Claude Code, use the /workflow command
/workflow docs/user-stories/US-001-user-authentication.md
```

The workflow will automatically:
1. Create technical specification
2. Implement the code
3. Write comprehensive tests
4. Review code quality
5. Commit changes

## Workflow Commands

### `/start` - Start Feature Development

Begins feature development from a user story. Creates a technical specification and optionally starts implementation.

**Usage:**
```
/start docs/user-stories/US-001-feature.md
```

**What it does:**
1. Reads the user story
2. Launches spec-writer agent to create technical spec
3. Presents spec for your review
4. Asks if you want to continue with implementation

**When to use:**
- Starting a new feature
- Need to create a technical spec first
- Want to review specs before coding

---

### `/spec` - Create Technical Specification

Creates or updates a detailed technical specification from a user story.

**Usage:**
```
/spec US-001
/spec docs/user-stories/US-001-feature.md
```

**What it does:**
1. Reads the user story
2. Analyzes requirements and acceptance criteria
3. Creates detailed technical spec including:
   - Technical approach & architecture
   - Data models & API design
   - Implementation steps
   - Testing strategy
4. Saves to `docs/specs/SPEC-<US-ID>-<feature-name>.md`

**Output:**
- Comprehensive technical specification
- Ready for implementation

---

### `/code` - Implement Code

Implements code from a technical specification.

**Usage:**
```
/code docs/specs/SPEC-001-user-authentication.md
/code user-authentication
```

**What it does:**
1. Reads the technical specification
2. Launches code-implementer agent
3. Implements code following the spec and project conventions
4. Runs linting and type checking
5. Reports implementation summary

**Note:** This only implements code, does NOT create tests.

---

### `/test` - Create and Run Tests

Creates comprehensive tests for implemented code.

**Usage:**
```
/test
/test src/features/auth/
/test user-authentication
```

**What it does:**
1. Identifies code to test (from recent changes or specified files)
2. Launches test-writer agent
3. Creates unit and integration tests
4. Runs tests and verifies they pass
5. Fixes any failing tests
6. Reports test coverage

**Output:**
- Comprehensive test suite
- Test coverage report
- All tests passing

---

### `/review` - Code Review

Performs comprehensive code review of recent changes.

**Usage:**
```
/review
/review src/features/auth/
```

**What it does:**
1. Identifies changes using git diff or specified files
2. Launches code-reviewer agent
3. Performs comprehensive review:
   - Code quality assessment
   - Security vulnerabilities
   - Performance issues
   - Type safety & linting
   - Best practices adherence
4. Presents prioritized findings
5. Asks if you want to fix issues

**Output:**
- Detailed code review report
- Prioritized issues (Critical → High → Medium → Low)
- Recommendations and fixes

---

### `/done` - Complete Feature

Completes feature development with final checks, review, and commit.

**Usage:**
```
/done
/done "feat: implement user authentication"
```

**What it does:**
1. Runs final checks:
   - Code review
   - All tests
   - Linting & type checking
   - Build verification
2. Fixes critical issues if found
3. Creates meaningful commit with:
   - Descriptive message
   - Reference to user story/spec
   - Co-author attribution
4. Commits changes
5. Asks about push/PR

**Output:**
- Feature committed and ready for push
- All quality gates passed

---

### `/workflow` - Complete Automated Workflow

Runs the complete automated development workflow from user story to done.

**Usage:**
```
/workflow docs/user-stories/US-001-feature.md
/workflow US-001
```

**What it does:**
Orchestrates the complete workflow:

1. **START Phase**:
   - Read user story
   - Create technical specification
   - Get user approval

2. **CODE Phase**:
   - Implement code following spec
   - Run linting & type checking

3. **TEST Phase**:
   - Create comprehensive tests
   - Run tests and verify all pass

4. **REVIEW Phase**:
   - Comprehensive code review
   - Fix critical and high-priority issues

5. **DONE Phase**:
   - Final verification
   - Create commit
   - Ask about push/PR

**When to use:**
- Full automation from start to finish
- Processing multiple user stories
- Want hands-off development

**Output:**
- Feature fully implemented, tested, reviewed, and committed
- Complete workflow report with metrics

---

## Workflow Agents

### spec-writer

Creates detailed technical specifications from user stories.

**Responsibilities:**
- Analyze user stories and extract requirements
- Design technical solution architecture
- Create data models and API designs
- Break down into implementation steps
- Define testing strategy

**Output:** `docs/specs/SPEC-<US-ID>-<feature-name>.md`

---

### code-implementer

Implements production-ready code from technical specifications.

**Responsibilities:**
- Implement code following specifications
- Follow project conventions and patterns
- Add proper error handling
- Run linting and type checking
- Integrate with existing codebase

**Focus:**
- Clean, maintainable code
- Security best practices
- Performance considerations

---

### test-writer

Creates comprehensive test suites for implemented code.

**Responsibilities:**
- Create unit and integration tests
- Test happy paths and error cases
- Ensure good test coverage (70%+)
- Follow project testing conventions
- Run tests and fix failures

**Output:**
- Comprehensive test suite
- All tests passing
- Coverage report

---

### workflow-orchestrator

Orchestrates the complete development workflow.

**Responsibilities:**
- Coordinate all workflow phases
- Manage agent execution
- Handle errors and retries
- Report progress to user
- Make informed decisions at checkpoints

**Features:**
- Automatic quality gates
- Error recovery
- Progress tracking
- User checkpoints at key stages

---

### code-reviewer

Performs comprehensive code quality assessment.

**Responsibilities:**
- Review code quality and standards
- Identify security vulnerabilities
- Check performance issues
- Verify type safety
- Assess best practices adherence

**Output:**
- Detailed review report
- Prioritized findings
- Actionable recommendations

---

## CLI Commands

### List Available Items

```bash
# List all available commands
./x100 command list

# List all available agents
./x100 agent list
```

### Enable/Disable Commands

```bash
# Enable a specific command
./x100 command enable start
./x100 command enable spec

# Disable a command
./x100 command disable start

# Interactive management
./x100 command
```

### Enable/Disable Agents

```bash
# Enable a specific agent
./x100 agent enable spec-writer
./x100 agent enable code-implementer

# Disable an agent
./x100 agent disable spec-writer

# Interactive management
./x100 agent
```

### Enable Complete Workflow

```bash
# Enable all workflow commands and agents at once
./x100 workflow-enable
```

---

## Best Practices

### 1. Start with Good User Stories

Ensure your user stories are clear and complete:
- Well-defined acceptance criteria
- Clear business value
- Testable requirements

### 2. Review Specs Before Coding

Always review the generated technical spec:
- Verify technical approach
- Check data models and API design
- Confirm implementation steps

### 3. Use Checkpoints

The workflow has built-in checkpoints:
- After spec creation
- After code implementation
- After test creation
- Before final commit

Use these to review and provide feedback.

### 4. Iterative Refinement

Don't expect perfection on first run:
- Review generated code
- Run additional reviews if needed
- Iterate on tests and implementation

### 5. Customize for Your Project

Adapt the workflow to your needs:
- Enable only the commands you need
- Customize agent prompts (in `.claude/agents/`)
- Adjust workflow steps

---

## Workflow Examples

### Example 1: Simple Feature

```bash
# User story: US-001 - Add user profile page

# Run complete workflow
/workflow US-001

# Workflow will:
# 1. Create spec with profile page design
# 2. Implement React component
# 3. Create unit and integration tests
# 4. Review for quality and security
# 5. Commit with descriptive message
```

### Example 2: API Endpoint

```bash
# User story: US-002 - Create user authentication API

# Step by step approach
/start US-002         # Create spec first
# Review spec...

/code                 # Implement code
# Review implementation...

/test                 # Create tests
# Check test coverage...

/review               # Code review
# Fix any issues...

/done                 # Complete and commit
```

### Example 3: Bug Fix

```bash
# For bug fixes, you might skip spec creation

/code "Fix authentication bug in login endpoint"
/test                 # Ensure tests cover the bug
/review               # Security check
/done "fix: resolve auth token expiration bug"
```

---

## Troubleshooting

### Workflow Stuck at Checkpoint

**Issue:** Workflow waiting for user input

**Solution:** Respond to the checkpoint question (yes/no)

### Tests Failing

**Issue:** Tests fail during workflow

**Solution:**
- Workflow will attempt to fix automatically
- Review test failures
- Use `/test` to re-run after manual fixes

### Code Review Finds Critical Issues

**Issue:** Critical security or quality issues found

**Solution:**
- Workflow will fix automatically
- Review fixes before proceeding
- Re-run `/review` if needed

### Agent Not Found

**Issue:** "Agent not found" error

**Solution:**
```bash
# Enable the required agent
./x100 agent enable spec-writer
./x100 agent enable code-implementer
./x100 agent enable test-writer

# Or enable all workflow agents
./x100 workflow-enable
```

---

## Comparison with BMAD and SpecKit

### x100 Advantages

✅ **Less Overhead**
- Simpler directory structure
- Fewer configuration files
- Faster setup

✅ **Flexible Workflow**
- Use full workflow or individual commands
- Easy to customize
- Enable only what you need

✅ **Built-in Automation**
- Commands and agents work together
- Automatic quality gates
- Error recovery

### Key Differences

| Feature | x100 | BMAD | SpecKit |
|---------|------|------|---------|
| Setup Complexity | Low | Medium | High |
| Workflow Automation | Yes | Yes | Limited |
| Custom Commands | Yes | Yes | Yes |
| Agent System | Yes | Yes | Partial |
| CLI Management | Yes | No | No |

---

## Advanced Usage

### Custom Workflows

Create your own workflow by combining commands:

```bash
# Quick review workflow
/review → /test → /done

# Documentation-first workflow
/spec → review spec manually → /code → /test → /done

# TDD workflow
/spec → /test → /code → /done
```

### Batch Processing

Process multiple user stories:

```bash
# Enable workflow for batch processing
/workflow US-001
/workflow US-002
/workflow US-003
```

### Integration with CI/CD

The workflow commands can be used in CI/CD:

```bash
# In CI pipeline
claude-code "/test && /review"
```

---

## Getting Help

- **Documentation**: Read this guide and command descriptions
- **List Commands**: `./x100 command list`
- **List Agents**: `./x100 agent list`
- **Issues**: https://github.com/minhdqdev/x100-template/issues

---

## Contributing

Found ways to improve the workflow? Contribute back:

```bash
./x100 contribute
```

This will create a pull request with your improvements to the x100 template.
