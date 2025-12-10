# Steering Files

Steering files give AI assistants persistent knowledge about your workspace through markdown files. Instead of explaining conventions in every chat, steering files ensure AI consistently follows your patterns, libraries, and standards.

## Included Files

### Foundational Files (Always Included)

These files are automatically included in all AI interactions:

- **`product.md`** - Product vision, value proposition, target users, and success metrics
- **`tech.md`** - Technology stack, frameworks, tools, and infrastructure
- **structure.md`** - Project directory layout and organization

### Conditional Strategy Files

These files are automatically included when working with matching file patterns:

- **`api-standards.md`** - REST conventions, error handling, authentication patterns
  - Included when: `**/*.{py,ts,js,go,java}`
  
- **`testing-standards.md`** - Testing philosophy, test types, coverage requirements
  - Included when: `**/*.test.*`, `**/*.spec.*`, `**/tests/**/*`
  
- **`code-conventions.md`** - Naming conventions, function design, error handling
  - Included when: `**/*.{py,ts,tsx,js,jsx,go,java,rs}`
  
- **`security-policies.md`** - Authentication, encryption, input validation
  - Included when: `**/*.{py,ts,js,go,java,rs}`
  
- **`deployment-workflow.md`** - Environment setup, deployment strategies, rollback procedures
  - Included when: `**/*.{yml,yaml,sh,ps1,Dockerfile,*.tf}`

## How to Use

### 1. Customize Foundation Files

Start by filling in the three foundational files with your project details:

```bash
# Edit product overview
vi .x100/steering/product.md

# Edit technology stack
vi .x100/steering/tech.md

# Edit project structure
vi .x100/steering/structure.md
```

### 2. Refine Strategy Files

Update the strategy files to match your team's conventions:

```bash
# Customize API standards
vi .x100/steering/api-standards.md

# Customize testing standards
vi .x100/steering/testing-standards.md
```

### 3. Add Custom Files

Create additional steering files for specific needs:

```bash
# Example: Component design patterns
cat > .x100/steering/component-patterns.md << 'EOF'
---
include: "**/*.tsx, **/*.jsx"
---

# Component Patterns

## Component Structure
- Use functional components with hooks
- Keep components under 200 lines
- Extract complex logic to custom hooks
EOF
```

## Inclusion Modes

### Always Included (Default)

Files without front matter are included in every AI interaction:

```markdown
# My Steering File

This will be included in all interactions.
```

### Conditional Inclusion

Use front matter to specify when files should be included:

```markdown
---
include: "**/*.tsx"
---

# React Component Standards

This is only included when working with .tsx files.
```

### Manual Inclusion

Files can be referenced on-demand by name:

```markdown
# In your chat
Can you review this according to #troubleshooting-guide?
```

## Best Practices

✅ **Keep Files Focused**
One domain per file - API design, testing, or deployment

✅ **Use Clear Names**
- `api-rest-conventions.md` - REST API standards
- `testing-unit-patterns.md` - Unit testing approaches
- `components-form-validation.md` - Form standards

✅ **Include Context**
Explain why decisions were made, not just what

✅ **Provide Examples**
Use code snippets and before/after comparisons

✅ **Security First**
Never include API keys, passwords, or sensitive data

✅ **Maintain Regularly**
- Review during sprint planning
- Test file references after restructuring
- Treat steering changes like code changes - require reviews

## File References

Link to live workspace files to keep steering current:

```markdown
## Examples

API specs: #[[file:api/openapi.yaml]]
Component patterns: #[[file:components/ui/button.tsx]]
Config templates: #[[file:.env.example]]
```

## Common Strategies

The included strategy files cover:

- **API Standards** - REST conventions, error handling, versioning
- **Testing Approach** - Unit/integration/e2e patterns, coverage
- **Code Style** - Naming, file organization, architectural decisions
- **Security Guidelines** - Authentication, encryption, validation
- **Deployment Process** - Build, release, rollback procedures

## Works With AGENTS.md

This project also includes an `AGENTS.md` file in the root directory following the [AGENTS.md standard](https://agents.md/). The two systems complement each other:

- **Steering files** (this directory): Persistent project knowledge and conventions
- **AGENTS.md** (root): Task-specific guidance and workflows

AI assistants can use both for comprehensive project context.

## Inspired By

This steering system is inspired by [Kiro's steering feature](https://kiro.dev/docs/steering/), adapted for use with any AI coding assistant. The `AGENTS.md` file follows the [AGENTS.md standard](https://agents.md/).

## Support

For more information about x100 CLI and Spec-Driven Development:
- Run `x100 --help`
- Visit: https://github.com/yourusername/x100-cli

---

*Keep this directory updated as your project and practices evolve. These files are your AI assistant's persistent memory.*
