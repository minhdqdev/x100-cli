<div align="right">
  <details>
    <summary >🌐 Language</summary>
    <div>
      <div align="center">
        <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=en">English</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=zh-CN">简体中文</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=zh-TW">繁體中文</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=ja">日本語</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=ko">한국어</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=hi">हिन्दी</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=th">ไทย</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=fr">Français</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=de">Deutsch</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=es">Español</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=it">Italiano</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=ru">Русский</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=pt">Português</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=nl">Nederlands</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=pl">Polski</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=ar">العربية</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=fa">فارسی</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=tr">Türkçe</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=vi">Tiếng Việt</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=id">Bahasa Indonesia</a>
        | <a href="https://openaitx.github.io/view.html?user=minhdqdev&project=x100-cli&lang=as">অসমীয়া</
      </div>
    </div>
  </details>
</div>

<div align="center">
    <img src="media/x100-cli-logo.webp"/>
    <h1>⚡️ x100-cli ⚡️</h1>
    <h3><em>Create high-grade software at speed with AI agent</em></h3>
</div>

A starter blueprint for new and existing projects, built to speed up dev workflows—especially when wiring up AI agents 
with spec-driven development.

## ⚡️ Get started

### 🔧 Prerequisites

- **Linux/macOS** (or WSL2 on Windows)
- **[uv](https://docs.astral.sh/uv/)** for Python package management - 
Install: `brew install uv` (macOS) or `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Git** installed
- **AI Assistant** - Choose from: GitHub Copilot, Claude Code, Gemini CLI, Cursor, Windsurf, Amazon Q Developer, or others (see supported agents below)
- Basic familiarity with Markdown and shell scripting

### Quick Start (5 minutes)

**First time using x100?** Start here:

```bash
# 1. Install x100 CLI
pip install x100-cli

# Or use uvx (no installation needed)
uvx x100-cli init my-project

# 2. Initialize a new project with your preferred AI assistant
x100 init my-project --ai copilot  # or claude, gemini, cursor-agent, etc.

# 3. Start building with AI commands
cd my-project
# Use /x100.specify, /x100.plan, /x100.implement commands in your AI assistant
```

**Troubleshooting:**

- `x100 not found`: Install with `pip install x100-cli` or use `uvx x100-cli`
- Permission errors: Run `chmod +x scripts/*.sh` in the project directory
- Git errors: Ensure git is installed and configured

### Setup Options for Your Project

Choose one of the following based on your needs:

#### Option 1: Bootstrap a new project

```bash
# Using pip (recommended)
pip install x100-cli
x100 init my-project --ai copilot  # Choose your AI assistant

# Or using uvx (no installation)
uvx x100-cli init my-project --ai claude

# Or initialize in current directory
x100 init --here --ai gemini
```

Available AI assistants: `copilot`, `claude`, `gemini`, `cursor-agent`, `qwen`, `opencode`, `codex`, `windsurf`, `kilocode`, `auggie`, `codebuddy`, `roo`, `q`, `amp`, `shai`, `bob`

That's it! You can now start using the AI agent commands to build your project with spec-driven development.

**Checkpoint**: You should now have a project structure similar to this:

```bash
my-project/
├── .git/
├── .vscode/
│   └── settings.json
├── .github/      (if using GitHub Copilot)
├── .claude/      (if using Claude Code)
├── .gemini/      (if using Gemini CLI)
├── .cursor/      (if using Cursor)
├── .windsurf/    (if using Windsurf)
├── .amazonq/     (if using Amazon Q)
├── .x100/
│   ├── steering/     # AI context files
│   ├── scripts/
│   └── config.json
├── src/
├── docs/
├── AGENTS.md         # AI agent configuration
└── README.md
```

## Use the template

### Supported AI Agents

x100 CLI supports the following AI assistants:

| Agent | Type | CLI Tool | Installation |
|-------|------|----------|--------------|
| **GitHub Copilot** | IDE | - | Built into VS Code |
| **Claude Code** | CLI | `claude` | [Setup Guide](https://docs.anthropic.com/en/docs/claude-code/setup) |
| **Gemini CLI** | CLI | `gemini` | [GitHub](https://github.com/google-gemini/gemini-cli) |
| **Cursor** | IDE | - | [cursor.sh](https://cursor.sh/) |
| **Windsurf** | IDE | - | [windsurf.com](https://windsurf.com/) |
| **Amazon Q Developer** | CLI | `q` | [AWS Q CLI](https://aws.amazon.com/developer/learning/q-developer-cli/) |
| **Qwen Code** | CLI | `qwen` | [GitHub](https://github.com/QwenLM/qwen-code) |
| **opencode** | CLI | `opencode` | [opencode.ai](https://opencode.ai) |
| **Codex CLI** | CLI | `codex` | [GitHub](https://github.com/openai/codex) |
| **Kilo Code** | IDE | - | IDE-based |
| **Auggie CLI** | CLI | `auggie` | [Docs](https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli) |
| **CodeBuddy** | CLI | `codebuddy` | [codebuddy.ai](https://www.codebuddy.ai/cli) |
| **Roo Code** | IDE | - | IDE-based |
| **Amp** | CLI | `amp` | [Manual](https://ampcode.com/manual#install) |
| **SHAI** | CLI | `shai` | [GitHub](https://github.com/ovh/shai) |
| **IBM Bob** | IDE | - | IDE-based |

### Basic Workflow

The spec-driven development workflow with x100:

**Step-by-step approach:**

```bash
# 1. Create project constitution (principles and constraints)
Use AI command: /x100.constitution

# 2. Write baseline specification
Use AI command: /x100.specify

# 3. Create implementation plan
Use AI command: /x100.plan

# 4. Generate actionable tasks
Use AI command: /x100.tasks

# 5. Implement features
Use AI command: /x100.implement
```

**Optional enhancement commands:**

- `/x100.clarify` - Ask structured questions before planning
- `/x100.analyze` - Cross-artifact consistency check
- `/x100.checklist` - Generate quality validation checklists

### AI Steering Files

x100 includes a steering system that gives AI assistants persistent knowledge about your project. Instead of explaining conventions in every chat, steering files ensure AI consistently follows your patterns and standards.

**Included steering files:**

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

**Location:** `.x100/steering/`

**How to use:**

```bash
# 1. Customize foundation files with your project details
vi .x100/steering/product.md
vi .x100/steering/tech.md
vi .x100/steering/structure.md

# 2. Refine strategy files to match your team's conventions
vi .x100/steering/api-standards.md
vi .x100/steering/testing-standards.md

# 3. AI assistants will automatically reference these files
# No need to re-explain your conventions!
```

Strategy files use conditional inclusion - they're automatically loaded when working with relevant file types. For example, `api-standards.md` is included when editing Python, TypeScript, or Go files.

**Learn more:**
- [Full Steering Documentation](./docs/STEERING.md)
- See `.x100/steering/README.md` after initialization
- Inspired by [Kiro's steering feature](https://kiro.dev/docs/steering/)

### AGENTS.md Support

x100 automatically creates an `AGENTS.md` file in your project root following the [AGENTS.md standard](https://agents.md/). This file provides AI agents with:

- Project snapshot and key documentation locations
- Reference to steering files for persistent knowledge
- Workflow guidance for common tasks (coding, testing, documentation, code review)
- Best practices and automation commands

The `AGENTS.md` file is recognized by many AI coding assistants and complements the steering files by providing task-specific guidance.

### Project Health Analysis

Use `x100 nextstep` to get AI-powered project analysis and recommendations:

```bash
# First time setup (optional)
x100 nextstep-setup

# Basic analysis
x100 nextstep

# Detailed analysis with statistics
x100 nextstep --verbose

# Save report as Markdown
x100 nextstep --format markdown --save

# JSON output for automation
x100 nextstep --format json --verbose --save --output report.json

# With GitHub integration
x100 nextstep --github-repo owner/repo --github-token $GITHUB_TOKEN

# Use configuration file
x100 nextstep --config .x100/nextstep.json
```

**The command analyzes:**
- 📊 Codebase health (files, lines, TODOs, FIXMEs)
- 📝 Git activity and velocity
- 🧪 Test coverage
- 📋 GitHub issues and PRs (optional)

**It provides:**
- 📈 Project health score (0-100)
- 🔴 Blockers and risks
- 🔍 Gaps and inconsistencies
- 💡 Prioritized next steps

**Example output:**
```
📈 Project Health: 72/100 (Good)

🔴 Blockers & Risks
  • Low test coverage (45%)
  
🔍 Gaps Detected
  ⚠  Quality Gap: payment_processor.py: No tests (high risk)

💡 Recommended Next Steps

🎯 NOW:
  1. Increase test coverage to >60%
     • Rationale: Current coverage is critically low
     • Impact: Reduces production risk
     • Effort: 4-8 hours
```

See [docs/NEXTSTEP_FEATURE_PLAN.md](./docs/NEXTSTEP_FEATURE_PLAN.md) for complete documentation.

### CLI Commands

x100 provides several commands to manage your project:

```bash
# Initialize a new project
x100 init my-project --ai copilot

# Initialize in current directory
x100 init --here --ai claude

# Check project health and get next steps
x100 nextstep
x100 nextstep --verbose
x100 nextstep --github-repo owner/repo --github-token $GITHUB_TOKEN

# Manage AI agents
x100 agent list                    # List registered agents
x100 agent switch-default          # Change default AI agent (interactive)

# Check tool installation
x100 check

# View project status
x100 status

# Show version information
x100 version
```

### Additional Options

```bash
# Skip git initialization
x100 init my-project --ai copilot --no-git

# Skip agent tool checks
x100 init my-project --ai claude --ignore-agent-tools

# Force merge when using --here in non-empty directory
x100 init --here --ai gemini --force

# Specify script type (sh or ps)
x100 init my-project --ai cursor-agent --script ps

# Debug mode
x100 init my-project --ai windsurf --debug

# Use GitHub token for API requests
x100 init my-project --ai q --github-token $GITHUB_TOKEN
```

## 📚 Core philosophy

- **Context engineering is king**: detailed specs, constraints, and guidelines to guide AI agents

- **Intent-driven development** where specifications define the "*what*" before the "*how*"
- **Heavy reliance** on advanced AI model capabilities for specification interpretation

- **Human-in-the-loop** for critical thinking, creativity, and oversight

- **Agile methodologies** adapted for AI-augmented workflows: epics, user stories, tasks

- Use `AGENTS.md` for all agents used in the project

  - Read more in [here](https://agents.md)

-

## 👥 Contributors

Owner:

- Minh Dang Quang ([@minhdqdev](https://github.com/minhdqdev))

Contributors:

- Dang Hai Loc ([@hailoc12](https://github.com/hailoc12))

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](./.github/CONTRIBUTING.md) for details on:

- How to submit bug reports and feature requests
- Setting up your development environment
- Code style and testing requirements
- Pull request process

For questions or support, open a [GitHub issue](https://github.com/minhdqdev/x100-cli/issues/new).

## 💬 Support

For support, please open a [GitHub issue](https://github.com/minhdqdev/x100-cli/issues/new). 
We welcome bug reports, feature requests, and questions about using the template.

## 📄 License

This project is licensed under the terms of the MIT open source license. 
Please refer to the [LICENSE](./.github/LICENSE) file for the full terms.
