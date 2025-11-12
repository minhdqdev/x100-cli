# Technical Guideline

## 1. Purpose

This guideline helps SA and DEV choose consistent defaults for software product. Unless a documented exception exists, follow these recommendations to achieve maintainable systems and predictable operations. Record any deviation in an ADR that explains the trade-offs and approval.

## 2. Architectural Principles

- **Follow Twelve-Factor App methodology**: Build apps that are portable, cloud-native, and maintainable. See [twelve-factor app principles](#21-twelve-factor-app-principles) below for implementation details.
- Start simple: favour modular monolith or service-oriented designs before introducing microservices or event-driven architecture.
- Make domain boundaries explicit through well-defined modules, APIs, and shared contracts.
- Prefer convention over configuration: adopt mature frameworks and tooling rather than bespoke glue code.
- Automate from the outset: tests, packaging, deployment, and quality checks run in CI/CD for every change.
- Keep documentation and diagrams versioned with the codebase; update them as part of feature work.

### 2.1 Twelve-Factor App Principles

All applications should follow [The Twelve-Factor App](https://12factor.net/) methodology to ensure scalability, maintainability, and cloud-readiness:

#### I. Codebase
- One codebase tracked in version control (Git), many deploys
- Use Git submodules for backend/frontend when needed
- Never duplicate code across repos; share via packages

#### II. Dependencies
- Explicitly declare and isolate dependencies
- Python: use `uv` with lock files (`uv.lock`)
- Node.js: use `pnpm` with lock files (`pnpm-lock.yaml`)
- Never rely on implicit system packages

#### III. Config
- Store config in environment variables, never in code
- Use `.env` files locally (never commit), environment injection in production
- No hardcoded URLs, secrets, or environment-specific values
- Use feature flags for behavioral config

#### IV. Backing Services
- Treat databases, caches, queues as attached resources
- Access via URLs/connection strings in environment variables
- Should be swappable without code changes (dev PostgreSQL → prod RDS)
- Examples: PostgreSQL, Redis, S3, external APIs

#### V. Build, Release, Run
- Strictly separate build, release, and run stages
- Build: Convert code to executable bundle (Docker image)
- Release: Combine build with config for specific environment
- Run: Execute the release in the execution environment
- Use immutable releases with unique IDs (Git SHA, version tags)

#### VI. Processes
- Execute app as one or more stateless processes
- Never store session state in memory; use Redis, database, or tokens
- Shared data goes in backing services (PostgreSQL, S3)
- Any process can be killed/restarted without data loss

#### VII. Port Binding
- Export services via port binding
- Backend: bind to port via environment variable (e.g., `PORT=8000`)
- Frontend: Next.js binds to `PORT` (default 3000)
- No reliance on runtime injection of webserver (self-contained)

#### VIII. Concurrency
- Scale out via the process model
- Use separate process types for different workloads:
  - `web`: Handle HTTP requests (uvicorn, Next.js server)
  - `worker`: Background jobs (Celery, Bull)
  - `scheduler`: Cron-like tasks (Celery Beat)
- Scale by adding more processes, not threads (horizontal scaling)

#### IX. Disposability
- Maximize robustness with fast startup and graceful shutdown
- Processes should start quickly (< 10 seconds ideally)
- Handle SIGTERM for graceful shutdown: finish current requests, close connections
- Workers should return jobs to queue on shutdown
- Be robust against sudden death (crashes, hardware failures)

#### X. Dev/Prod Parity
- Keep development, staging, and production as similar as possible
- Same backing services (PostgreSQL everywhere, not SQLite in dev)
- Same Docker images across environments
- Deploy frequently to minimize divergence
- Use Docker Compose for local dev to mirror production

#### XI. Logs
- Treat logs as event streams
- Write to stdout/stderr, never manage log files
- Use structured logging (JSON format)
- Let environment handle routing (Docker logs, CloudWatch, Datadog)
- Include trace IDs for request correlation

#### XII. Admin Processes
- Run admin/management tasks as one-off processes
- Examples: database migrations, data imports, console sessions
- Use same codebase and config as regular processes
- Django: `python manage.py migrate`, `python manage.py shell`
- Run in same environment with same dependencies

## 3. Codebase Management

### 3.1 Repository layout

- Default: manage backend and frontend as Git submodules under `src/backend/` and `src/frontend/` to allow independent release cadences while keeping the integration repo slim.
- Alternative: a monorepo is acceptable when both stacks share release cadence and tooling; document the rationale in an ADR and ensure build pipelines remain isolated per component.
- Avoid mixing unrelated prototypes or throwaway code inside production repositories.

### 3.2 Collaboration practices

- Use trunk-based development or short-lived feature branches with mandatory reviews and automated checks.
- Run the full test suite and static analysis in CI for every merge request across all submodules.
- Tag releases and maintain change logs so operational teams can trace deployments back to commits.

### 3.3. Dependency management

#### Django/Python

- Use `uv` to manage dependencies and generate lock files (`uv lock`).

### 3.4. Package management

#### Django/Python

- Django app should be named `core` to avoid conflicts with third-party packages. Avoid creating multiple Django apps unless there is a clear modularity or reuse benefit.
- Every module should have docstrings and type annotations (PEP 484).
- Follow PEP 8 for code style; use `black` for formatting and `flake8` for linting.
- Group related functionality into submodules under `core/`, e.g., `core/models/`, `core/views/`, `core/services/`, `core/utils/`.
- Each submodule should have an `__init__.py` file to mark it as a package.
- Models should be defined in `core/models.py` or `core/models/` if complex.
- Views should be in `core/views.py` or `core/views/` if complex.
- Serializers should be in `core/serializers.py` or `core/serializers/` if complex.
- Utility functions should be in `core/utils.py` or `core/utils/` if complex.
- Avoid deeply nested packages; flatten the structure when possible to reduce import complexity.
- Use relative imports for intra-package references and absolute imports for external packages.
- Service modules should include header docstrings explaining their purpose and usage.
- Service modules should be put under `core/services/` with a `__init__.py` file to mark it as a package. `services/__init__.py` should import submodules to expose a clean public API, for example:

```python
from .brew_service import BrewService
from .digest_service import DigestService

__all__ = [
    "BrewService",
    "DigestService",
]
```

## 4. Default Technology Stack

### 4.1 Backend

- Language: Python 3.12+ is the default because of the team skillset, ecosystem maturity, and excellent Django support.
- Framework: Django is preferred for its batteries-included ORM, admin, and security hardening. Consider FastAPI only for lightweight APIs that do not need Django’s features.
- Dependency management: use `uv` to guarantee reproducible lock files, deterministic builds, and rapid installs.
- Application server: run behind `uvicorn` for ASGI support and async capabilities. Reserve alternatives (e.g., Gunicorn, Hypercorn) for platform constraints that block `uvicorn`.
- Caching: use Redis for in-memory caching and rate limiting.
- Task queue: use Celery with Redis as the broker for background jobs.
- Messaging: use RabbitMQ or Redis streams for inter-service communication when needed. For complicated workflows, consider Apache Kafka.
- Testing: write unit tests with `pytest` and `pytest-django`, use `factory_boy` for test data, and run integration tests with `pytest` or `requests`. Include linting (flake8, black) and type checking (mypy) in CI.
- Data access: use Django’s ORM with repository abstractions when cross-service reuse is required. Only use raw SQL when justified by performance or complex queries.
- Observability: ship structured logs (JSON), capture OpenTelemetry traces, and expose Prometheus metrics by default.

Refer to the `./DJANGO.md` file for best practices specific to Django projects.

### 4.2 Frontend

- Framework: Next.js with React 18+ and TypeScript provides server-side rendering, routing, and strong DX.
- Styling: use a design system or component library agreed by the product team; document deviations.
- Testing: add unit tests (Vitest/Jest), integration tests (Playwright/Cypress), and linting (ESLint) to CI.

Refer to the `./NEXTJS.md` file for best practices specific to Next.js projects.

### 4.3 Data stores and messaging

- Primary datastore: PostgreSQL is the standard for relational workloads because of reliability, migrations, and first-class Django support. Choose managed instances (e.g., RDS) whenever possible.
- Secondary stores: introduce MySQL or other relational databases only when a hosting constraint prevents PostgreSQL.
- NoSQL: adopt MongoDB or DynamoDB for document/large-scale workloads with clearly justified access patterns. Document read/write volume, consistency requirements, and retention policy before adoption.
- Caching & queues: Redis is the default cache and message broker. Use Celery or RQ for background jobs; consider cloud-native alternatives (SQS, Pub/Sub) only when integrating with cloud-managed ecosystems.

### 4.4 Infrastructure

- Containerisation: package services with Docker. Provide reproducible `Dockerfile`s checked into each submodule.
- Orchestration: use Docker Compose for local development and integration testing. Move to Kubernetes or managed container services when scale, resilience, or multi-service deployments require it; capture the transition in an ADR.

## 5. API Design

- Document every external API with OpenAPI 3.x and publish generated docs alongside the service.
- Version APIs explicitly (`/api/v1/...`) and deprecate old versions with clear timelines.
- Follow REST conventions: nouns in URLs, appropriate HTTP verbs, HATEOAS when helpful.
- Standardise error responses with machine-readable codes, human-readable messages, and trace IDs.
- Provide pagination, filtering, and sorting for collection endpoints. Define rate limits and idempotency expectations.
- Include example requests/responses and authentication expectations in the OpenAPI spec.

## 6. Data Management

- Table names should be singular and lowercase with underscores (e.g., `user_profile`).
- Manage schema changes with migrations committed to source control; one migration per logical change.
- Apply retention policies, archival plans, and GDPR-compliant deletion workflows.
- Encrypt sensitive data at rest and in transit. Use application-level encryption for fields that require it.
- Establish backup schedules, test restores quarterly, and document RPO/RTO targets.

## Testing

- Write unit tests for all business logic, aiming for >80% coverage.
- Use integration tests to cover critical workflows and edge cases.
- Run tests in isolated environments with a fresh database state for each run.
- Use `pyproject.toml` as the single configuration file for `pytest` other than the old `pytest.ini`.

## 7. Security

- Enforce HTTPS everywhere; redirect HTTP to HTTPS automatically.
- Authenticate APIs with bearer tokens (JWT or opaque tokens) and authorise with least-privilege roles.
- **Never commit secrets**: Store credentials in secret managers (Vault, AWS Secrets Manager) or environment variables; follow Twelve-Factor config principles.
- Use `.env` files for local development (add to `.gitignore`), environment injection for production.
- Run SAST, dependency vulnerability scanning, and container image scanning in CI.
- Apply secure coding guidelines (OWASP ASVS) and threat-model significant features. Document mitigations.

## 8. Performance & Resilience

- **Design for horizontal scalability**: Follow Twelve-Factor concurrency model; scale by adding processes, not vertical resources.
- **Build stateless processes**: Store session state in backing services (Redis, database), never in-memory.
- Implement caching strategies (Redis, CDN) for frequent reads, with explicit cache invalidation rules.
- Offload long-running work to asynchronous workers or event-driven pipelines (Celery, Bull).
- Define performance budgets and SLIs/SLOs; test them via load/chaos testing prior to launch.
- Instrument code with metrics, traces, and logs; aggregate them in a central observability stack.
- Use circuit breakers, retries with exponential backoff, and timeouts when calling external services.
- Design for disposability: handle SIGTERM gracefully, restart quickly, survive sudden process death.

## 9. Deployment & Operations

- **Follow Twelve-Factor principles**: Build immutable images, use environment variables for config, treat logs as streams (see [Section 2.1](#21-twelve-factor-app-principles)).
- Build immutable Docker images with pinned base image versions and dependencies.
- Use GitHub Actions or GitLab CI/CD pipelines for automated builds, tests, security scans, and deployments.
- Roll out changes with canary or blue/green deployments when production impact is high; otherwise use rolling updates.
- Manage configuration via environment variables injected at deploy time; keep environment parity across dev/staging/prod.
- Design for disposability: fast startup (< 10s), graceful shutdown (handle SIGTERM), robust against crashes.
- Maintain runbooks, incident response checklists, and rollback procedures stored alongside the service.

## 10. Language-Specific Best Practices

### 10.1 Frontend (React/Next.js/TypeScript)

**Component Structure:**
```typescript
// ProductCard.tsx
import { type FC } from 'react';
import { type Product } from '@/types';

interface ProductCardProps {
  product: Product;
  onAddToCart: (productId: string) => void;
}

/**
 * Displays product information with add-to-cart action.
 * Implements design from Figma: [link]
 * 
 * @see PRD Section 3.2 - Product Discovery Journey
 */
export const ProductCard: FC<ProductCardProps> = ({ product, onAddToCart }) => {
  // Implementation
};
```

**Standards:**
- Server components by default, client components marked explicitly
- Strong TypeScript types, no `any`
- Tailwind for styling, design tokens from theme
- Loading/error states for all data fetching
- Accessibility: semantic HTML, ARIA, keyboard nav
- Performance: code splitting, image optimization

### 10.2 Backend (Python/Django, Node.js/Express)

**Service Layer Pattern:**
```python
# core/services/email_verification.py
"""
Email verification service for user authentication.

Implements PRD Section 4.2 - User Authentication.
See ADR-0015 for retry strategy.
"""
from typing import Optional
import logging
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

class EmailVerificationService:
    """Handles email verification token generation and validation."""
    
    def send_verification_email(self, user_id: str, email: str) -> bool:
        """
        Send verification email to user.
        
        Args:
            user_id: User's unique identifier
            email: Email address to verify
            
        Returns:
            True if email sent successfully
            
        Raises:
            ValidationError: If email format invalid
        """
        logger.info("Sending verification email", extra={
            "user_id": user_id,
            "email": email,
        })
        # Implementation
```

**Standards:**
- Type hints everywhere
- Docstrings for all public APIs
- Structured logging with context
- Custom exceptions with actionable messages
- Service layer for business logic
- Keep views/controllers thin
- Database migrations for schema changes

### 10.3 Testing Standards

**Test Structure:**
```typescript
// ProductCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ProductCard } from './ProductCard';
import { mockProduct } from '@/test/fixtures';

describe('ProductCard', () => {
  it('displays product information correctly', () => {
    // Arrange
    const product = mockProduct({ name: 'Test Product' });
    const onAddToCart = jest.fn();
    
    // Act
    render(<ProductCard product={product} onAddToCart={onAddToCart} />);
    
    // Assert
    expect(screen.getByText('Test Product')).toBeInTheDocument();
  });
  
  it('calls onAddToCart when button clicked', () => {
    // Test implementation
  });
  
  it('handles out-of-stock products', () => {
    // Edge case test
  });
});
```

**Coverage Requirements:**
- Unit: All business logic functions
- Integration: API endpoints, database interactions
- E2E: Critical user journeys from PRD Section 3
- Edge cases: Nulls, empty arrays, max values, errors
- Performance: Load tests for scalability concerns

## 11. Observability Requirements

**Every feature must include:**

### 11.1 Structured Logging

```typescript
logger.info('User created account', {
  user_id: user.id,
  signup_method: 'email',
  referral_source: req.query.ref,
  timestamp: new Date().toISOString(),
});
```

### 11.2 Error Tracking

```python
try:
    result = external_api.call()
except ExternalAPIError as e:
    logger.error("External API call failed", extra={
        "error": str(e),
        "trace_id": request.trace_id,
        "retry_attempt": attempt,
    })
    raise
```

### 11.3 Metrics (for critical paths)

```typescript
metrics.increment('auth.signup.success', {
  method: 'email',
  source: referralSource,
});

metrics.timing('auth.signup.duration', duration);
```

## 12. Common Pitfalls to Avoid

❌ **Starting code without reading PRD/user story**
✅ Always review requirements and acceptance criteria first

❌ **Skipping tests because "it's simple"**
✅ Write tests for everything; simple code still breaks

❌ **Hardcoding values instead of using config**
✅ Use environment variables and feature flags

❌ **Ignoring error cases and edge cases**
✅ Handle errors gracefully, test edge cases

❌ **Writing code without considering observability**
✅ Add logging, metrics, and error tracking upfront

❌ **Not documenting "why" behind complex logic**
✅ Add comments explaining rationale, not just "what"

❌ **Large commits with multiple concerns**
✅ Keep commits small, focused, and atomic

❌ **Pushing code that doesn't pass CI locally**
✅ Run all quality gates before pushing

❌ **Creating PRs without linking to issues**
✅ Always reference GitHub issue and PRD section

❌ **Not testing manually before requesting review**
✅ Verify feature works end-to-end yourself first

❌ **Mixing business logic in views/controllers**
✅ Keep business logic in service layer

❌ **Not using type hints or proper TypeScript types**
✅ Strong typing catches bugs early and improves DX

❌ **Skipping accessibility considerations for UI**
✅ Build accessible interfaces from day one

❌ **Over-engineering solutions prematurely**
✅ Start simple, refactor when complexity is justified

❌ **Not planning for rollback or failure scenarios**
✅ Always have a rollback strategy and error handling

## 13. Governance and Decision Records

- Capture architectural decisions in ADRs within `docs/adrs/`; link them from relevant sections of this guideline.
- Review this guideline quarterly to ensure technology choices remain current.
- Provide onboarding notes and diagrams (`docs/diagrams/`, `docs/data/`) that reflect the latest state before major releases.
