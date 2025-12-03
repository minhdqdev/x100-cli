---
include: "**/*.{py,ts,js,go,java,rs}"
---

# Security Policies

## Security Principles

- **Defense in Depth** - Multiple layers of security
- **Least Privilege** - Minimum necessary permissions
- **Fail Securely** - Default to secure state
- **Zero Trust** - Never trust, always verify

## Authentication

### Password Requirements
- Minimum 12 characters
- Use bcrypt, scrypt, or Argon2 for hashing
- Never store plaintext passwords

### Session Management
- Use secure, httpOnly cookies
- Set appropriate timeouts (15-30 minutes)
- Regenerate session IDs after authentication

## Input Validation

- **Never trust user input**
- Validate type, length, format, range
- Use parameterized queries (prevent SQL injection)
- Escape HTML output (prevent XSS)

## Data Protection

**Never log or expose:**
- Passwords (even hashed)
- API keys and secrets
- Credit card numbers
- Authentication tokens

**Encryption:**
- Always use HTTPS (TLS 1.2+)
- Encrypt sensitive database fields
- Store encryption keys separately

## API Security

- Implement rate limiting
- Configure strict CORS policies
- Never commit secrets to version control
- Use environment variables

---

*This file is conditionally included when working with code files.*
