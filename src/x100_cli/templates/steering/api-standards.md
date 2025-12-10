---
include: "**/*.{py,ts,js,go,java}"
---

# API Standards

## REST Conventions

### URL Structure

- Use nouns for resources: `/api/v1/users`, `/api/v1/products`
- Use plural nouns: `/users` not `/user`
- Use kebab-case for multi-word resources: `/user-profiles`
- Version APIs explicitly: `/api/v1/...`, `/api/v2/...`

### HTTP Methods

- `GET` - Retrieve resources (idempotent, no side effects)
- `POST` - Create new resources
- `PUT` - Replace entire resource
- `PATCH` - Partially update resource
- `DELETE` - Remove resource

### Status Codes

- `200 OK` - Successful GET, PUT, PATCH, or DELETE
- `201 Created` - Successful POST with resource creation
- `204 No Content` - Successful DELETE or action with no response body
- `400 Bad Request` - Invalid request syntax or validation error
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Valid auth but insufficient permissions
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Resource state conflict (e.g., duplicate)
- `422 Unprocessable Entity` - Valid syntax but semantic errors
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server-side error
- `503 Service Unavailable` - Temporary unavailability

## Error Response Format

All errors must follow this structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "trace_id": "abc123-def456-ghi789"
  }
}
```

## Authentication

- Use Bearer tokens: `Authorization: Bearer <token>`
- JWT tokens for stateless authentication
- Refresh tokens for long-lived sessions
- Include token expiry and refresh mechanisms

## Pagination

For collection endpoints, use cursor-based or offset-based pagination:

```json
{
  "data": [...],
  "pagination": {
    "total": 100,
    "page": 1,
    "per_page": 20,
    "has_next": true,
    "next_cursor": "abc123"
  }
}
```

Query parameters:
- `page` - Page number (1-indexed)
- `per_page` or `limit` - Items per page (default: 20, max: 100)
- `cursor` - Cursor for cursor-based pagination

## Rate Limiting

Include rate limit headers:
- `X-RateLimit-Limit` - Maximum requests allowed
- `X-RateLimit-Remaining` - Requests remaining
- `X-RateLimit-Reset` - Unix timestamp when limit resets

## Request/Response Examples

### Create Resource

**Request:**
```http
POST /api/v1/users
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Response:**
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/users/123

{
  "id": "123",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-01-15T10:30:00Z"
}
```

## OpenAPI Documentation

- Maintain OpenAPI 3.0 specification for all APIs
- Store specs in `src/{module}/specs/` directory
- Include request/response examples
- Document authentication requirements
- Version specs with API versions

## Idempotency

- Use `Idempotency-Key` header for POST/PATCH requests
- Store idempotency keys for 24 hours
- Return cached response for duplicate requests

## Retry Strategy

- Implement exponential backoff: 1s, 2s, 4s, 8s
- Max 3 retry attempts for 5xx errors
- Don't retry 4xx errors (except 429)
- Include `Retry-After` header for 429 responses

## 12-Factor App API Principles

### IV. Backing Services - Treat as Attached Resources
APIs should treat all backing services (databases, caches, message queues, external APIs) as attached resources:

- **URL-Based Configuration**: Connect to services via URLs from environment variables
- **Swappable Resources**: Switch between local and cloud services without code changes
- **Resource Abstraction**: Code shouldn't care if database is local or managed service

**Example - JavaScript:**
```javascript
// Good - resource from environment
const dbUrl = process.env.DATABASE_URL;
const db = connectToDatabase(dbUrl);

const redisUrl = process.env.REDIS_URL;
const cache = createRedisClient(redisUrl);

// Bad - hardcoded resource
const db = connectToDatabase('localhost:5432/mydb');
```

**Example - Python:**
```python
import os
from sqlalchemy import create_engine
import redis

# Good - resources from environment
DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
cache = redis.from_url(REDIS_URL)

# Bad - hardcoded resources
engine = create_engine('postgresql://localhost:5432/mydb')
```

### VII. Port Binding - Self-Contained HTTP Services
- **Bind to Port from Environment**: Read port from environment variables
- **Self-Contained Web Server**: Include web server library (Express, FastAPI, etc.)
- **No External Web Server**: Don't rely on Apache, Nginx, or IIS for runtime

**Example - JavaScript (Express):**
```javascript
const express = require('express');
const app = express();
const PORT = process.env.PORT || 8080;

app.listen(PORT, '0.0.0.0', () => {
  console.log(`API listening on port ${PORT}`);
});
```

**Example - Python (FastAPI):**
```python
import os
from fastapi import FastAPI
import uvicorn

app = FastAPI()
PORT = int(os.getenv('PORT', 8080))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=PORT)
```

### VI. Processes - Stateless API Design
- **No Session Affinity**: Any API instance can handle any request
- **Stateless Requests**: Each request contains all necessary information
- **Session Store**: Use Redis or database for session persistence
- **No Memory Caching**: Use external cache (Redis, Memcached) not in-process memory

**Example - JavaScript (Session Management):**
```javascript
// Bad - in-memory sessions (doesn't scale)
const sessions = {};
app.post('/login', (req, res) => {
  sessions[sessionId] = userData;
});

// Good - external session store
const redis = require('redis').createClient({ url: process.env.REDIS_URL });

app.post('/login', async (req, res) => {
  const sessionId = generateSessionId();
  await redis.set(`session:${sessionId}`, JSON.stringify(userData), {
    EX: 3600 // Expire in 1 hour
  });
  res.json({ sessionId });
});

app.get('/api/profile', async (req, res) => {
  const sessionId = req.headers['x-session-id'];
  const userData = await redis.get(`session:${sessionId}`);
  res.json(JSON.parse(userData));
});
```

**Example - Python (Session Management):**
```python
import os
import json
import redis
from fastapi import FastAPI, Header

app = FastAPI()
cache = redis.from_url(os.environ['REDIS_URL'])

# Bad - in-memory sessions (doesn't scale)
sessions = {}

@app.post('/login')
def login_bad(user_data: dict):
    sessions[session_id] = user_data  # Don't do this!

# Good - external session store
@app.post('/login')
async def login(user_data: dict):
    session_id = generate_session_id()
    cache.setex(
        f'session:{session_id}',
        3600,  # Expire in 1 hour
        json.dumps(user_data)
    )
    return {'session_id': session_id}

@app.get('/api/profile')
async def get_profile(x_session_id: str = Header()):
    user_data = cache.get(f'session:{x_session_id}')
    return json.loads(user_data) if user_data else None
```

### XI. Logs - API Logging Standards
- **Log to stdout**: All API logs written to standard output
- **Structured Format**: Use JSON for logs
- **Request Correlation**: Include `trace_id` or `request_id` in all logs
- **No File Logging**: Don't write to `/var/log` or manage log files

**Example Request Logging:**
```json
{
  "timestamp": "2025-12-09T10:04:30.900Z",
  "level": "info",
  "method": "POST",
  "path": "/api/v1/users",
  "status": 201,
  "duration_ms": 45,
  "trace_id": "abc123-def456",
  "user_id": "usr_789"
}
```

---

*This file is conditionally included when working with API-related files. Keep it updated as your API conventions evolve.*
