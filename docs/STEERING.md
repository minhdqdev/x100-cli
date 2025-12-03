# AI Steering Files

Steering files provide AI assistants with persistent knowledge about your project through markdown files. This eliminates the need to repeatedly explain your conventions, patterns, and standards in every conversation.

## Overview

When you initialize a project with `x100 init`, the steering system is automatically set up in `.x100/steering/` with pre-configured files covering common development concerns.

## Included Steering Files

### Foundation Files (Always Included)

These files are automatically included in all AI interactions:

- **`product.md`** - Product vision, value proposition, target users, success metrics
- **`tech.md`** - Technology stack, frameworks, tools, infrastructure
- **`structure.md`** - Project directory layout and organization

### Strategy Files (Conditionally Included)

These files are automatically included when working with matching file patterns:

| File | Purpose | Included When |
|------|---------|---------------|
| `api-standards.md` | REST conventions, error handling, authentication | `**/*.{py,ts,js,go,java}` |
| `testing-standards.md` | Test patterns, coverage requirements | `**/*.test.*`, `**/*.spec.*`, `**/tests/**/*` |
| `code-conventions.md` | Naming conventions, function design | `**/*.{py,ts,tsx,js,jsx,go,java,rs}` |
| `security-policies.md` | Authentication, encryption, validation | `**/*.{py,ts,js,go,java,rs}` |
| `deployment-workflow.md` | Environment setup, deployment strategies | `**/*.{yml,yaml,sh,ps1,Dockerfile,*.tf}` |

## How It Works

### Conditional Inclusion

Strategy files use front matter to specify when they should be loaded:

```markdown
---
include: "**/*.tsx"
---

# React Component Standards

This content is only included when working with .tsx files.
```

### Always Included

Files without front matter (or with no `include` directive) are included in every AI interaction:

```markdown
# Product Overview

This will be included in all interactions.
```

### Manual Inclusion

Any steering file can be referenced on-demand by name:

```
# In your AI chat
Can you review this according to #security-policies?
```

## Getting Started

### 1. Initialize Project

When you run `x100 init`, steering files are automatically created in `.x100/steering/`:

```bash
x100 init my-project
cd my-project
```

### 2. Customize Foundation Files

Edit the three foundation files with your project details:

```bash
# Edit product overview
vi .x100/steering/product.md

# Edit technology stack
vi .x100/steering/tech.md

# Edit project structure
vi .x100/steering/structure.md
```

### 3. Refine Strategy Files

Update strategy files to match your team's conventions:

```bash
# Customize API standards
vi .x100/steering/api-standards.md

# Customize testing standards
vi .x100/steering/testing-standards.md

# Customize code conventions
vi .x100/steering/code-conventions.md

# Customize security policies
vi .x100/steering/security-policies.md

# Customize deployment workflow
vi .x100/steering/deployment-workflow.md
```

### 4. Create Custom Steering Files

Add project-specific steering files as needed:

```bash
# Example: React component patterns
cat > .x100/steering/component-patterns.md << 'EOF'
---
include: "**/*.tsx, **/*.jsx"
---

# Component Patterns

## Component Structure
- Use functional components with hooks
- Keep components under 200 lines
- Extract complex logic to custom hooks

## Naming Conventions
- PascalCase for component names
- camelCase for functions and variables
- Use descriptive names that reveal intent
EOF
```

## Best Practices

### Keep Files Focused

Each steering file should cover one domain:

✅ Good:
- `api-rest-conventions.md` - REST API standards
- `testing-unit-patterns.md` - Unit testing approaches
- `components-form-validation.md` - Form component standards

❌ Avoid:
- `everything.md` - All standards in one file

### Provide Context

Explain **why** decisions were made, not just **what** the standards are:

```markdown
## Error Handling

### Use Custom Error Classes

We use custom error classes to provide:
- Type-safe error handling
- Structured error information
- Consistent error responses

This approach was chosen because it allows...
```

### Include Examples

Use code snippets and before/after comparisons:

```markdown
## Function Design

### Keep Functions Small

❌ Bad - Too nested:
```typescript
function processUser(user) {
  if (user) {
    if (user.isActive) {
      if (user.email) {
        // deep nested logic
      }
    }
  }
}
```

✅ Good - Early returns:
```typescript
function processUser(user) {
  if (!user || !user.isActive || !user.email) {
    return null;
  }
  return processActiveUser(user);
}
```
```

### Security First

Never include sensitive data in steering files:

❌ Don't include:
- API keys or secrets
- Passwords or credentials
- Production URLs
- Internal service endpoints

✅ Use placeholders:
```markdown
## API Configuration

Database URL: `postgresql://user:password@host:5432/dbname`
API Key: `<stored in secret manager>`
```

### Maintain Regularly

- Review steering files during sprint planning
- Update when making architectural changes
- Test file references after project restructuring
- Treat steering changes like code changes - require reviews

## File References

Link to live workspace files to keep steering current:

```markdown
## API Specification

See the OpenAPI spec: #[[file:api/openapi.yaml]]

## Component Examples

Button component: #[[file:components/ui/button.tsx]]
Form component: #[[file:components/ui/form.tsx]]

## Configuration Templates

Environment variables: #[[file:.env.example]]
```

## Integration with AI Assistants

### Supported Assistants

Steering files work with all AI coding assistants supported by x100:

- Claude Code
- GitHub Copilot
- Cursor
- Gemini CLI
- Qwen Code
- And more...

### How AI Assistants Use Steering

1. **Foundation files** are loaded at the start of every conversation
2. **Strategy files** are automatically loaded based on the files you're editing
3. **Manual references** can be invoked with `#filename` syntax
4. AI assistants maintain context across the conversation

### Benefits

- **Consistency** - AI generates code following your standards
- **Efficiency** - No need to repeat conventions
- **Quality** - Adherence to best practices
- **Onboarding** - New team members get instant context

## AGENTS.md Integration

x100 also creates an `AGENTS.md` file in your project root following the [AGENTS.md standard](https://agents.md/). This file works alongside steering files:

- **AGENTS.md**: Task-specific guidance (workflows, commands, best practices)
- **Steering files**: Persistent project knowledge (conventions, standards, patterns)

Together, they provide comprehensive context for AI assistants without manual explanation.

## Inspiration

This steering system is inspired by [Kiro's steering feature](https://kiro.dev/docs/steering/), adapted for use with any AI coding assistant through the x100 CLI. The `AGENTS.md` file follows the [AGENTS.md standard](https://agents.md/) for cross-tool compatibility.

## Troubleshooting

### Steering Files Not Being Used

**Issue:** AI assistant doesn't seem to follow steering files

**Solutions:**
1. Verify files exist in `.x100/steering/`
2. Check file patterns in front matter match your files
3. Ensure AI assistant supports reading project files
4. Try explicitly referencing: "Please follow #api-standards"

### Files Not Conditionally Loading

**Issue:** Strategy files aren't loading when expected

**Solutions:**
1. Check front matter syntax (YAML format)
2. Verify file patterns use correct glob syntax
3. Test pattern with: `find . -path "**/*.tsx"`
4. Ensure no syntax errors in front matter

### Too Much Context

**Issue:** AI responses are too long or include irrelevant information

**Solutions:**
1. Use conditional inclusion more liberally
2. Split large steering files into focused files
3. Remove redundant information
4. Use manual inclusion for specialized guidance

## Further Reading

- [Kiro Steering Documentation](https://kiro.dev/docs/steering/) - Original inspiration
- [Spec-Driven Development](../spec-driven.md) - Development methodology
- [Workflow Guide](../resources/WORKFLOW.md) - x100 workflow automation

---

For questions or suggestions about steering files, please open an issue on GitHub.
