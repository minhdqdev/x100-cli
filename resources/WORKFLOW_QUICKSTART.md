# x100 Workflow Quick Start

Get started with x100 workflow automation in 5 minutes.

## Setup (One-time)

```bash
# Enable workflow automation
./x100 workflow-enable
```

This activates:
- ✅ 7 workflow commands
- ✅ 4 orchestrator agents

## Basic Usage

### Full Automation

```bash
# In Claude Code
/workflow docs/user-stories/US-001-feature.md
```

This automatically:
1. 📝 Creates technical spec
2. 💻 Implements code
3. ✅ Writes tests
4. 🔍 Reviews code
5. ✨ Commits changes

### Step-by-Step

```bash
/start US-001    # Create spec
/code            # Implement
/test            # Test
/review          # Review
/done            # Commit
```

## Commands Cheat Sheet

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/start` | Begin feature | New feature, need spec first |
| `/spec` | Create technical spec | Plan before coding |
| `/code` | Implement code | Have spec, ready to code |
| `/test` | Create & run tests | Code done, need tests |
| `/review` | Code review | Check quality & security |
| `/done` | Commit feature | Ready to commit |
| `/workflow` | Full automation | Want hands-off development |

## Examples

### New Feature
```bash
/workflow US-005-payment-integration
```

### Bug Fix
```bash
/code "Fix authentication timeout bug"
/test
/done "fix: resolve auth timeout issue"
```

### Quick Review
```bash
/review
/test
/done
```

## Management

```bash
# List available commands
./x100 command list

# Enable specific command
./x100 command enable spec

# Interactive menu
./x100
```

## Need Help?

- **Full Guide**: See `resources/WORKFLOW.md`
- **Commands**: `./x100 command list`
- **Agents**: `./x100 agent list`

## Workflow Overview

```
┌─────────────┐
│ User Story  │
└──────┬──────┘
       │
       ▼
┌─────────────┐     /start or /spec
│    SPEC     │────────────────────▶ Technical Specification
└──────┬──────┘
       │
       ▼
┌─────────────┐     /code
│    CODE     │────────────────────▶ Implementation
└──────┬──────┘
       │
       ▼
┌─────────────┐     /test
│    TEST     │────────────────────▶ Test Suite
└──────┬──────┘
       │
       ▼
┌─────────────┐     /review
│   REVIEW    │────────────────────▶ Quality Check
└──────┬──────┘
       │
       ▼
┌─────────────┐     /done
│    DONE     │────────────────────▶ Committed Feature
└─────────────┘
```

## Tips

✅ **DO:**
- Review specs before coding
- Let workflow fix failing tests
- Use `/workflow` for routine features
- Use step-by-step for complex features

❌ **DON'T:**
- Skip spec creation for complex features
- Ignore code review findings
- Commit with failing tests
- Rush through checkpoints

---

**Ready to start?**

```bash
./x100 workflow-enable
```

Then in Claude Code:
```
/workflow your-first-user-story.md
```
