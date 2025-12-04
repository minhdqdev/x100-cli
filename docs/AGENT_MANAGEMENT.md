# Agent Management

This document describes how to manage AI agents in x100 projects, including default agent configuration and switching between agents.

## Overview

Starting with version 0.1.1, x100 automatically persists your selected AI agent during project initialization and provides commands to manage your default agent configuration.

## Default Agent Persistence

### During Project Initialization

When you run `x100 init`, the selected AI agent is automatically saved to `.x100/config.json`:

```bash
# Initialize with Claude
x100 init my-project --ai claude

# Initialize with GitHub Copilot  
x100 init --here --ai copilot

# Initialize with Gemini CLI
x100 init my-project --ai gemini
```

After initialization, your project's `.x100/config.json` will contain:

```json
{
  "default_agent": "claude"
}
```

### Benefits

- **Persistence**: Your agent choice is saved and can be referenced by tools and scripts
- **Team Consistency**: Team members can see which agent the project was initialized with
- **Automation**: Scripts and CI/CD pipelines can read the default agent configuration

## Switching Default Agent

### Interactive Mode

Use the `x100 agent switch-default` command to interactively change your default AI agent:

```bash
cd my-project
x100 agent switch-default
```

This will:
1. Display your current default agent
2. Show a list of all available agents
3. Allow you to select a new agent using arrow keys
4. Update `.x100/config.json` with your selection
5. Provide feedback on the agent folder location

### Command Output Example

```
Current default agent: claude

Choose new default AI assistant:
▶ copilot (GitHub Copilot)
  claude (Claude Code)
  gemini (Gemini CLI)
  cursor-agent (Cursor)
  ...

✓ Default agent changed from claude to copilot

Agent files location: .github/

Note: Agent folder does not exist yet. You may need to set up 
the agent configuration manually or re-initialize the project.
```

## Viewing Current Configuration

To see your current default agent without changing it:

```bash
cat .x100/config.json
```

Or use the `x100 agent list` command (if you have registered agents).

## Configuration File Structure

The `.x100/config.json` file stores project-level configuration:

```json
{
  "default_agent": "claude",
  "project_name": "my-project",
  "other_config": "..."
}
```

### Fields

- `default_agent`: The key of the default AI agent (e.g., "claude", "copilot", "gemini")
- Other fields may be added by various x100 commands and features

## Supported Agents

x100 supports the following AI agents:

| Agent Key | Display Name | Folder | CLI Tool Required |
|-----------|-------------|--------|-------------------|
| `copilot` | GitHub Copilot | `.github/` | No (IDE-based) |
| `claude` | Claude Code | `.claude/` | Yes |
| `gemini` | Gemini CLI | `.gemini/` | Yes |
| `cursor-agent` | Cursor | `.cursor/` | No (IDE-based) |
| `qwen` | Qwen Code | `.qwen/` | Yes |
| `opencode` | opencode | `.opencode/` | Yes |
| `codex` | Codex CLI | `.codex/` | Yes |
| `windsurf` | Windsurf | `.windsurf/` | No (IDE-based) |
| `kilocode` | Kilo Code | `.kilocode/` | No (IDE-based) |
| `auggie` | Auggie CLI | `.augment/` | Yes |
| `codebuddy` | CodeBuddy | `.codebuddy/` | Yes |
| `roo` | Roo Code | `.roo/` | No (IDE-based) |
| `q` | Amazon Q Developer CLI | `.amazonq/` | Yes |
| `amp` | Amp | `.agents/` | Yes |
| `shai` | SHAI | `.shai/` | Yes |
| `bob` | IBM Bob | `.bob/` | No (IDE-based) |

## Integration with Other Commands

### nextstep Command

The `x100 nextstep` command automatically uses your project's default agent for analysis:

```bash
# Initialize project with an agent
x100 init my-project --ai copilot

# Later, nextstep will use copilot for analysis
x100 nextstep

# Output shows:
# Analysis by: GitHub Copilot
# ...
```

The nextstep command:
- Reads the default agent from `.x100/config.json`
- Uses that agent's name in the analysis display
- Falls back to "claude" if no default agent is configured
- Can be overridden via `.x100/nextstep.json` configuration

## Use Cases

### 1. Team Projects

Save the default agent in version control to communicate which agent the team is using:

```bash
# Initialize with your team's standard agent
x100 init team-project --ai copilot

# Commit the config
git add .x100/config.json
git commit -m "Set default agent to GitHub Copilot"
```

### 2. Switching Agents Mid-Project

If you want to try a different agent:

```bash
# Switch to a different agent
x100 agent switch-default

# The agent folder structure may need to be set up manually
# or you can re-run init in place:
x100 init --here --ai <new-agent> --force
```

### 3. CI/CD Integration

Scripts can read the default agent to provide agent-specific behaviors:

```bash
# Read default agent in shell script
DEFAULT_AGENT=$(jq -r '.default_agent' .x100/config.json)
echo "Project uses: $DEFAULT_AGENT"
```

## Troubleshooting

### Config file doesn't exist

If `.x100/config.json` doesn't exist, you may be:
- Not in an x100 project directory
- In a project initialized with an older version of x100

**Solution**: Re-run `x100 init --here --force` to update the project structure.

### Agent switch doesn't create agent folder

The `switch-default` command only updates the configuration. To set up the actual agent files, either:
- Manually copy agent files from templates
- Re-run `x100 init --here --ai <agent> --force` to merge in the new agent structure

### Can't switch to certain agents

Some agents may require CLI tools to be installed. Use `x100 check` to verify required tools are available, or use `--ignore-agent-tools` during init.

## API Reference

### Core Functions

```python
from x100_cli.core import save_config, load_config, AGENT_CONFIG

# Save configuration
config = {"default_agent": "claude"}
save_config(config, config_path)

# Load configuration  
config = load_config()

# Access agent metadata
agent_info = AGENT_CONFIG["claude"]
# Returns: {'name': 'Claude Code', 'folder': '.claude/', ...}
```

## See Also

- [AGENTS.md](../AGENTS.md) - Guidelines for adding new agent support
- [README.md](../README.md) - General x100 documentation
- [CHANGELOG.md](../CHANGELOG.md) - Version history
