# x100 Setup Guide

Complete guide to setup x100 with Claude Code workflow automation.

## Prerequisites

### Required
- **macOS/Linux** (or WSL2 on Windows)
- **Claude Code** installed
- **Git** installed
- **uv** (Python package manager) - Install: `brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Optional
- Python 3.11+ (will be managed by uv)

## Installation Steps

### Step 1: Clone x100 Template

For a new project:

```bash
# Create project directory
mkdir your-project-name
cd your-project-name

# Clone x100 as .x100
git clone https://github.com/minhdqdev/x100-template.git .x100

# Make scripts executable
chmod +x .x100/scripts/*.sh
chmod +x .x100/x100

# Optional: Create symlink for easier access
ln -s .x100/x100 x100
```

For an existing project:

```bash
# Clone as submodule
git submodule add https://github.com/minhdqdev/x100-template.git .x100

# Make scripts executable
chmod +x .x100/scripts/*.sh
chmod +x .x100/x100

# Optional: Create symlink
ln -s .x100/x100 x100
```

### Step 2: Initialize Project

```bash
# Initialize project structure
./x100 init
```

This will:
- ✅ Create project directories (docs, submodules, tests, scripts)
- ✅ Initialize git repository (if not exists)
- ✅ Collect project metadata
- ✅ Create README.md and AGENTS.md
- ✅ Create CLI symlink

### Step 3: Setup Claude Code

```bash
# Run interactive setup
./x100

# Select option 3: "Setup AI Agent"
# Then select: "Claude Code"
```

Or directly:

```bash
# This will be available after implementing the command
# For now, use the interactive menu
```

**What this does:**
- Copies commands from `.x100/resources/claude/commands/` to `.claude/commands/`
- Copies agents from `.x100/resources/claude/agents/` to `.claude/agents/`
- Copies settings.json and statusline.sh
- Sets up Claude Code integration

**Result:**
- `.claude/` directory created in your project root
- Basic commands available: `/refine-idea`, `/generate-prd`, `/generate-user-stories`, etc.

### Step 4: Enable Workflow Automation (Recommended)

```bash
# Enable all workflow commands and agents
./x100 workflow-enable
```

**What this does:**
- ✅ Enables 7 workflow commands: `/start`, `/spec`, `/code`, `/review`, `/test`, `/done`, `/workflow`
- ✅ Enables 4 orchestrator agents: `spec-writer`, `code-implementer`, `test-writer`, `workflow-orchestrator`
- ✅ Copies them to `.claude/commands/` and `.claude/agents/`

**Alternative - Enable selectively:**

```bash
# List available commands
./x100 command list

# Enable specific commands
./x100 command enable start
./x100 command enable spec
./x100 command enable code

# List available agents
./x100 agent list

# Enable specific agents
./x100 agent enable spec-writer
./x100 agent enable code-implementer
```

## Verification

### Verify Installation

```bash
# Run verification
./x100 verify
```

This checks:
- ✅ Directory name is `.x100`
- ✅ Outer directory is a git repo
- ✅ Required directories exist (submodules, docs)
- ✅ Required files exist (README.md, AGENTS.md)

### Verify Claude Code Integration

1. **Open Claude Code** in your project directory

2. **Check commands are available:**
   - Type `/` in Claude Code
   - You should see available commands

3. **Test a command:**
   ```
   /workflow --help
   ```
   or
   ```
   /start --help
   ```

### Verify Workflow Commands

```bash
# List active commands
ls -la .claude/commands/

# Should include:
# - start.md
# - spec.md
# - code.md
# - test.md
# - review.md
# - done.md
# - workflow.md
```

### Verify Workflow Agents

```bash
# List active agents
ls -la .claude/agents/

# Should include:
# - spec-writer.md
# - code-implementer.md
# - test-writer.md
# - workflow-orchestrator.md
# - code-reviewer.md (existing)
```

## Project Structure

After setup, your project should look like:

```
your-project-name/
├── .git/                          # Git repository
├── .claude/                       # Claude Code configuration
│   ├── commands/                  # Active commands
│   │   ├── start.md
│   │   ├── spec.md
│   │   ├── code.md
│   │   ├── test.md
│   │   ├── review.md
│   │   ├── done.md
│   │   └── workflow.md
│   ├── agents/                    # Active agents
│   │   ├── spec-writer.md
│   │   ├── code-implementer.md
│   │   ├── test-writer.md
│   │   ├── workflow-orchestrator.md
│   │   └── code-reviewer.md
│   ├── settings.json
│   └── statusline.sh
├── .x100/                         # x100 template (submodule)
│   ├── resources/
│   │   ├── claude/
│   │   │   ├── available-commands/   # All available commands
│   │   │   ├── available-agents/     # All available agents
│   │   │   ├── commands/             # Default commands
│   │   │   └── agents/               # Default agents
│   │   ├── WORKFLOW.md               # Workflow documentation
│   │   └── WORKFLOW_QUICKSTART.md    # Quick start guide
│   ├── scripts/
│   ├── src/
│   │   └── main.py                   # x100 CLI tool
│   └── x100                          # CLI launcher
├── x100 -> .x100/x100             # Symlink to CLI
├── docs/                          # Project documentation
│   ├── specs/                     # Technical specifications
│   └── user-stories/              # User stories
├── submodules/                    # Git submodules (if any)
├── tests/                         # Test files
├── README.md
└── AGENTS.md
```

## Usage Examples

### Example 1: Complete Workflow

```bash
# In Claude Code
/workflow docs/user-stories/US-001-user-authentication.md
```

This will automatically:
1. Create technical specification
2. Implement the code
3. Write tests
4. Review code quality
5. Commit changes

### Example 2: Step-by-Step

```bash
# In Claude Code
/start US-001              # Create spec
# Review spec...

/code                      # Implement
# Review code...

/test                      # Create tests
# Check coverage...

/review                    # Code review
# Fix issues...

/done                      # Commit
```

### Example 3: Quick Review

```bash
# Made changes manually, now review and test
/review
/test
/done "feat: implement user profile page"
```

## Managing Workflow

### Enable/Disable Commands

```bash
# Interactive management
./x100
# Select "Manage Commands"

# Or via CLI
./x100 command list
./x100 command enable start
./x100 command disable start
```

### Enable/Disable Agents

```bash
# Interactive management
./x100
# Select "Manage Agents"

# Or via CLI
./x100 agent list
./x100 agent enable spec-writer
./x100 agent disable spec-writer
```

### Enable Everything

```bash
# Enable all workflow items at once
./x100 workflow-enable
```

## Customization

### Customize Commands

Edit command files in `.claude/commands/`:

```bash
# Edit a command
vim .claude/commands/start.md

# Changes take effect immediately in Claude Code
```

### Customize Agents

Edit agent files in `.claude/agents/`:

```bash
# Edit an agent
vim .claude/agents/spec-writer.md

# Changes take effect immediately in Claude Code
```

### Create Custom Commands

1. Create new file in `.x100/resources/claude/available-commands/`
2. Add frontmatter with description
3. Write command prompt
4. Enable: `./x100 command enable your-command`

### Create Custom Agents

1. Create new file in `.x100/resources/claude/available-agents/`
2. Add frontmatter with name and description
3. Write agent prompt
4. Enable: `./x100 agent enable your-agent`

## Troubleshooting

### "uv not found" Error

Install uv:

```bash
# macOS
brew install uv

# Linux/macOS/WSL
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Commands Not Showing in Claude Code

1. Check `.claude/commands/` directory exists
2. Verify command files are `.md` format
3. Restart Claude Code
4. Try: `./x100 workflow-enable` again

### Agents Not Working

1. Check `.claude/agents/` directory exists
2. Verify agent files are `.md` format with proper frontmatter
3. Verify frontmatter includes `name:` and `description:`
4. Try: `./x100 workflow-enable` again

### Permission Denied

```bash
# Make x100 executable
chmod +x .x100/x100
chmod +x .x100/scripts/*.sh

# Try again
./x100
```

### "Not a git repository" Error

```bash
# Initialize git
git init

# Then run setup again
./x100 init
```

## Getting Help

- **Workflow Guide**: [resources/WORKFLOW.md](./.x100/resources/WORKFLOW.md)
- **Quick Start**: [resources/WORKFLOW_QUICKSTART.md](./.x100/resources/WORKFLOW_QUICKSTART.md)
- **Issues**: https://github.com/minhdqdev/x100-template/issues
- **CLI Help**: `./x100 --help`

## Next Steps

After setup:

1. ✅ Read [Workflow Quick Start](./.x100/resources/WORKFLOW_QUICKSTART.md)
2. ✅ Create your first user story in `docs/user-stories/`
3. ✅ Run `/workflow <user-story-file>` in Claude Code
4. ✅ Iterate and customize to your needs

## Contributing

Found improvements? Contribute back:

```bash
./x100 contribute
```

This creates a PR with your changes to the x100 template.
