---
include: "**/*.{py,ts,tsx,js,jsx,go,java,rs}"
---

# Code Conventions

## General Principles

- **Readability over cleverness** - Write code for humans first
- **Consistency** - Follow established patterns
- **Simplicity** - Keep it simple until complexity is justified
- **DRY** - Don't repeat yourself
- **YAGNI** - You aren't gonna need it

## Naming Conventions

**Python:**
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants

**TypeScript/JavaScript:**
- `camelCase` for functions and variables
- `PascalCase` for classes and components
- `UPPER_CASE` for constants

## Function Design

- Single responsibility principle
- Aim for < 50 lines per function
- Use early returns to reduce nesting
- Limit to 3-4 parameters

## Error Handling

Use custom error classes and handle errors gracefully with specific error types.

## Documentation

**Do comment:**
- Complex algorithms or business logic
- Non-obvious decisions ("why" not "what")
- Public APIs and interfaces

**Don't comment:**
- Obvious code
- Outdated information
- Commented-out code

---

*This file is conditionally included when working with code files.*
