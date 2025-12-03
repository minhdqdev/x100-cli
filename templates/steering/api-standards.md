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

---

*This file is conditionally included when working with API-related files. Keep it updated as your API conventions evolve.*
