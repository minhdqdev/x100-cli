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

## 12-Factor App Code Principles

### VI. Processes - Stateless Code Design
- **No Local State**: Never store session data or cached content in process memory
- **Share-Nothing Architecture**: Each process instance is independent
- **Idempotent Operations**: Operations should be safely retryable
- **No Sticky Sessions**: Code must work regardless of which process handles the request

**Example - JavaScript (Bad - Stateful):**
```javascript
let sessionCache = {}; // Don't do this!

app.get('/api/user', (req, res) => {
  const user = sessionCache[req.sessionId];
  res.json(user);
});
```

**Example - JavaScript (Good - Stateless):**
```javascript
app.get('/api/user', async (req, res) => {
  const user = await redis.get(`session:${req.sessionId}`);
  res.json(user);
});
```

**Example - Python (Bad - Stateful):**
```python
# Don't do this!
session_cache = {}

@app.get('/api/user')
def get_user(session_id: str):
    user = session_cache.get(session_id)
    return user
```

**Example - Python (Good - Stateless):**
```python
@app.get('/api/user')
async def get_user(session_id: str):
    user = await redis.get(f'session:{session_id}')
    return json.loads(user) if user else None
```

### VII. Port Binding - Self-Contained Services
- **Export Services via Port**: Application binds to a port and listens for requests
- **No Runtime Injection**: Don't rely on runtime injection of webserver (e.g., Tomcat, Apache)
- **Self-Contained**: App includes web server library and is completely self-contained

**Example - JavaScript (Express):**
```javascript
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
```

**Example - Python (FastAPI):**
```python
import os
import uvicorn

PORT = int(os.getenv('PORT', 8080))

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=PORT)
```

**Example - Python (Flask):**
```python
import os

PORT = int(os.getenv('PORT', 8080))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
```

### IX. Disposability - Robust Code Patterns
- **Fast Startup**: Minimize initialization time
  - Lazy load non-critical resources
  - Use connection pools efficiently
  - Avoid heavy pre-computation

- **Graceful Shutdown**: Handle termination signals properly

**Example - JavaScript (Node.js):**
```javascript
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('HTTP server closed');
  });
  await database.disconnect();
  await cache.disconnect();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('SIGINT received, shutting down gracefully');
  await gracefulShutdown();
});
```

**Example - Python (FastAPI with async):**
```python
import signal
import sys
import asyncio

async def graceful_shutdown():
    print('Shutdown signal received, closing connections...')
    await database.disconnect()
    await cache.close()
    print('Cleanup complete')
    sys.exit(0)

def signal_handler(sig, frame):
    asyncio.create_task(graceful_shutdown())

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
```

**Example - Python (Flask with sync):**
```python
import signal
import sys

def graceful_shutdown(signum, frame):
    print('Shutdown signal received, closing connections...')
    database.close()
    cache.close()
    print('Cleanup complete')
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)
```

### XI. Logs - Logging Patterns
- **Write to stdout/stderr**: All logs go to standard output
- **Structured Logging**: Use JSON format for easier parsing
- **No File Management**: Don't write to log files or manage rotation
- **Include Context**: Add correlation IDs, user IDs, request IDs

**Example - JavaScript (Winston):**
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  format: winston.format.json(),
  transports: [new winston.transports.Console()]
});

// Good - stdout with structured format
logger.info('User login successful', {
  userId: user.id,
  requestId: req.id,
  timestamp: new Date().toISOString()
});

// Bad - file logging
fs.appendFile('/var/log/app.log', message); // Don't do this!
```

**Example - JavaScript (Simple):**
```javascript
// Good - simple structured logging to stdout
console.log(JSON.stringify({
  level: 'info',
  timestamp: new Date().toISOString(),
  message: 'User login successful',
  userId: user.id,
  requestId: req.id
}));
```

**Example - Python (structlog):**
```python
import structlog
import sys

# Configure structured logging to stdout
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
)

logger = structlog.get_logger()

# Good - structured logging to stdout
logger.info('User login successful', user_id=user.id, request_id=request.id)
```

**Example - Python (Standard logging):**
```python
import logging
import json
import sys

# Configure JSON logging to stdout
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(message)s'
)

logger = logging.getLogger(__name__)

# Good - structured logging
logger.info(json.dumps({
    'level': 'info',
    'timestamp': datetime.utcnow().isoformat(),
    'message': 'User login successful',
    'user_id': user.id,
    'request_id': request.id
}))

# Bad - file logging
logging.FileHandler('/var/log/app.log')  # Don't do this!
```

---

*This file is conditionally included when working with code files.*
