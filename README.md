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
- **Claude Code** (recommended) or other AI coding agents: [OpenAI Codex](https://openai.com/codex/), 
[GitHub Copilot](https://code.visualstudio.com/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), 
or [Cursor](https://cursor.sh/)
- **[uv](https://docs.astral.sh/uv/)** for Python package management - 
Install: `brew install uv` (macOS) or `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Git** installed
- Basic familiarity with Markdown and shell scripting

### Quick Start (5 minutes)

**First time using x100?** Start here:

```bash
# 1. Try it out in a test directory
mkdir x100-test && cd x100-test
git clone https://github.com/minhdqdev/x100-cli.git .x100
chmod +x .x100/x100
./.x100/x100 init

# 2. Setup Claude Code and enable workflow
./.x100/x100  # Select "Setup AI Agent" → "Claude Code"
./.x100/x100 workflow-enable

# 3. Test with example feature (in Claude Code)
/workflow docs/user-stories/US-001-example-feature.md
```

**Troubleshooting:**

- `uv not found`: `brew install uv` (macOS) or `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Commands not showing: `./x100 workflow-enable` and restart Claude Code
- Permission denied: `chmod +x .x100/x100`

### Setup Options for Your Project

Choose one of the following based on your needs:

#### Option 1: Bootstrap a new project

```bash
cd your-project-name

# Clone the template repository to .x100 (directory name is important)
git clone https://github.com/minhdqdev/x100-cli.git .x100
chmod +x .x100/scripts/*.sh
chmod +x .x100/x100
ln -s .x100/x100 x100  # optional symlink for easier access
bash .x100/x100 init
```

If your project uses Git, you may want to add this template as a submodule for your code:

```bash
git submodule add -b <branch_name> <repo_url> .x100
```

That's it! You can now start defining your project idea in `docs/IDEA.md` 
and use the AI agent commands to generate refined ideas, PRDs, implementation plans, code, and tests.

Read more in the [Use the template](#use-the-template) section below.

**Checkpoint**: You should now have a project structure similar to this:

```bash
your-project-name/
├── .git/
├── .vscode/
│   ├── settings.json
├── .copilot/  (if using GitHub Copilot)
├── .claude/   (if using Claude Code)
├── .gemini/   (if using Gemini CLI)
├── .cursor/   (if using Cursor)
├── .x100/
│   ├── resources/
│   ├── scripts/
│   ├── config.json
│   └── ...
├── src/
│   ├── frontend/
│   └── backend/
│   └── ...
├── docs/
└── ...
```

## Use the template

### Setup for Claude Code

After initializing the project, setup Claude Code integration:

```bash
# Run x100 setup tool
./x100

# Select "Setup AI Agent" → "Claude Code"
# This will copy commands and agents to .claude/ directory

# Enable workflow automation (recommended)
./x100 workflow-enable
```

Or use CLI commands directly:

```bash
# Setup Claude Code
./x100  # Select option 3 "Setup AI Agent" → "Claude Code"

# Enable workflow automation
./x100 workflow-enable
```

### Workflow Automation (Recommended)

x100 includes a complete workflow automation system. See [Workflow Quick Start](./resources/WORKFLOW_QUICKSTART.md).

**Quick Start:**

```bash
# Enable workflow
./x100 workflow-enable

# In Claude Code, run complete workflow
/workflow docs/user-stories/US-001-feature.md
```

**Available workflow commands:**

| Command     | Description                                |
| ----------- | ------------------------------------------ |
| `/start`    | Start feature development from user story  |
| `/spec`     | Create technical specification             |
| `/code`     | Implement code from spec                   |
| `/test`     | Create and run tests                       |
| `/review`   | Comprehensive code review                  |
| `/done`     | Complete feature and commit                |
| `/workflow` | **Full automation** - runs all steps above |

**Step-by-step workflow:**

```plain
/start US-001 → /code → /test → /review → /done
```

**Examples:**

```bash
# Full automation
/workflow docs/user-stories/US-002-your-feature.md

# Quick bug fix
/code "Fix authentication timeout bug"
/test
/review
/done "fix: resolve auth timeout issue"

# After manual coding
/review
/test
/done
```

For detailed workflow guide, see [resources/WORKFLOW.md](./resources/WORKFLOW.md)

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
# Basic analysis
x100 nextstep

# Detailed analysis with statistics
x100 nextstep --verbose

# JSON output for automation
x100 nextstep --format json

# With GitHub integration
x100 nextstep --github-repo owner/repo --github-token $GITHUB_TOKEN
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

### Traditional Approach (Idea → PRD → User Stories)

#### Refine your idea

1. Define your project idea in `docs/IDEA.md`.
2. Use AI agent command: `/refine-idea`
3. Review and edit the refined idea in `docs/REFINED_IDEA.md`

#### From refined idea to PRD

1. Use AI agent command: `/generate-prd`
2. Review and edit the generated PRD in `docs/PRD.md`

#### From PRD to product backlog

1. Use AI agent command: `/generate-product-backlog`
2. Review and edit the generated product backlog in `docs/PRODUCT_BACKLOG.md`

#### From product backlog to user stories

1. Use AI agent command: `/generate-user-stories`
2. Review and edit the generated user stories in `docs/user-stories/US-<ID>.md`

#### From user stories to code

Use the workflow automation (recommended) or manually implement:

1. Use `/workflow` for full automation
2. Or use step-by-step: `/start` → `/code` → `/test` → `/review` → `/done`

### Managing Commands & Agents

```bash
# List available commands and agents
./x100 command list
./x100 agent list

# Enable/disable specific items
./x100 command enable <name>
./x100 command disable <name>
./x100 agent enable <name>
./x100 agent disable <name>

# Interactive management
./x100  # Select "Manage Commands" or "Manage Agents"
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

If you have integrated this template into your project, please consider contributing back any improvements to 
the original [x100-cli](https://github.com/minhdqdev/x100-cli). We have provided a very convenient way to help you do so, just run:

```bash
./x100 contribute
```

You need to install `gh` CLI and authenticate it with your GitHub account first. 
This command will create a fork of the original repository, commit your changes to a new branch, 
and open a pull request for you.

Read more in the [Contributing Guide](./.github/CONTRIBUTING.md).

## 💬 Support

For support, please open a [GitHub issue](https://github.com/minhdqdev/x100-cli/issues/new). 
We welcome bug reports, feature requests, and questions about using the template.

## 📄 License

This project is licensed under the terms of the MIT open source license. 
Please refer to the [LICENSE](./.github/LICENSE) file for the full terms.
