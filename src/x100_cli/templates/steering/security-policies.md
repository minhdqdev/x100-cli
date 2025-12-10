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

## 12-Factor App Security Principles

### III. Config - Secure Configuration Management
**Strict separation of config from code:**

- **Environment Variables Only**: Store ALL credentials, API keys, and secrets in environment variables
- **Never Commit Secrets**: No `.env` files in version control (use `.env.example` as template)
- **Config Validation**: Validate required environment variables at startup
- **Secrets Management**: Use secret managers (AWS Secrets Manager, HashiCorp Vault) in production

**Example - Python (Config Loading):**
```python
import os

# Good - fail fast if required config missing
DATABASE_URL = os.environ['DATABASE_URL']  # Raises KeyError if not set
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable required")

# Bad - hardcoded or default secrets
API_KEY = os.getenv('API_KEY', 'default-key-123')  # Never do this!
```

**Example - JavaScript (Config Loading):**
```javascript
// Good - fail fast if required config missing
const DATABASE_URL = process.env.DATABASE_URL;
if (!DATABASE_URL) {
  throw new Error('DATABASE_URL environment variable required');
}

const API_KEY = process.env.API_KEY;
if (!API_KEY) {
  throw new Error('API_KEY environment variable required');
}

// Bad - hardcoded or default secrets
const API_KEY = process.env.API_KEY || 'default-key-123'; // Never do this!
```

**What Goes in Environment Variables:**
- Database connection strings
- API keys and tokens
- Encryption keys
- OAuth client secrets
- Service endpoints and URLs
- Feature flags

**What Should NOT Go in Environment Variables:**
- Application code
- Business logic
- Routing rules
- Large configuration structures (use config files loaded by path from env var)

### IV. Backing Services - Secure Service Connections
- **TLS/SSL Always**: All connections to backing services must use encryption
- **Credential Rotation**: Design for rotating credentials without downtime
- **Least Privilege**: Service accounts have minimum necessary permissions
- **Connection Pooling**: Reuse connections securely, close on shutdown

### IX. Disposability - Security on Shutdown
- **Clear Sensitive Memory**: Zero out secrets before process exit
- **Close Connections Securely**: Properly close database and cache connections
- **No Temporary Files**: Don't write secrets to disk, even temporarily

### XI. Logs - Secure Logging
**Never log sensitive data:**
- ❌ Passwords (even hashed)
- ❌ API keys, tokens, secrets
- ❌ Credit card numbers (even partial)
- ❌ PII without explicit consent
- ❌ Session tokens or JWTs
- ❌ Database connection strings

**Log redaction example - JavaScript:**
```javascript
function maskEmail(email) {
  const [name, domain] = email.split('@');
  return `${name[0]}***@${domain}`;
}

// Good - sanitized logging
logger.info('User login', {
  userId: user.id,
  email: maskEmail(user.email), // user@example.com -> u***@example.com
  ip: request.ip
});

// Bad - exposing sensitive data
logger.info('Login attempt', {
  password: password,  // NEVER log passwords!
  token: authToken     // NEVER log tokens!
});
```

**Log redaction example - Python:**
```python
def mask_email(email: str) -> str:
    name, domain = email.split('@')
    return f"{name[0]}***@{domain}"

# Good - sanitized logging
logger.info('User login', extra={
    'user_id': user.id,
    'email': mask_email(user.email),  # user@example.com -> u***@example.com
    'ip': request.client.host
})

# Bad - exposing sensitive data
logger.info('Login attempt', extra={
    'password': password,  # NEVER log passwords!
    'token': auth_token    # NEVER log tokens!
})
```

---

*This file is conditionally included when working with code files.*
