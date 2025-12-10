# Project Structure

## Directory Layout

```
/
├── src/                  # Source code
├── docs/                 # Documentation
├── tests/                # Test files
├── .x100/                # x100 configuration and steering
│   ├── steering/         # AI steering files
│   └── scripts/          # Project automation scripts
└── README.md
```

## Module Organization

*Describe how your code is organized into modules, packages, or components.*

## Key Directories

*Explain the purpose of key directories in your project.*

## Configuration Files

*List important configuration files and their purposes.*

## Build Artifacts

*Describe where build outputs, compiled files, or generated assets are located.*

## Testing Structure

*Explain how tests are organized and where they reside.*

## 12-Factor App Compliance

### I. Codebase
- **Single Repository**: One codebase tracked in version control, many deploys
- **Shared Code Root**: All environments (dev, staging, production) deploy from the same codebase
- **No Environment-Specific Code**: Use configuration, not code branches, for environment differences

### III. Config
- **Environment Variables**: Store all configuration in environment variables (database URLs, API keys, credentials)
- **Never Commit Secrets**: Use `.env.example` templates; actual `.env` files are gitignored
- **Config Files**: Document required environment variables and their purposes
- **12-Factor Config Pattern**:
  - `config/` - Configuration loading logic
  - `.env.example` - Template showing required variables
  - Environment-specific configs injected at runtime

### XII. Admin Processes
- **Scripts Location**: Admin and management scripts in `scripts/` or `.x100/scripts/`
- **Same Codebase**: Migration and one-off scripts ship with application code
- **Identical Environment**: Run admin tasks in the same environment as regular app processes

---

*This file is automatically included in all AI interactions. Keep it updated as your structure evolves.*
