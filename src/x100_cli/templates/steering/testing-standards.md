---
include: "**/*.test.*, **/*.spec.*, **/tests/**/*"
---

# Testing Standards

## Testing Philosophy

- Write tests for all business logic
- Test behavior, not implementation details
- Keep tests isolated and independent
- Make tests readable and maintainable
- Aim for >80% code coverage

## Test Structure

### Arrange-Act-Assert (AAA) Pattern

```typescript
describe('UserService', () => {
  it('creates user with valid data', async () => {
    // Arrange - Set up test data and dependencies
    const userData = { email: 'test@example.com', name: 'Test User' };
    const mockRepository = new MockUserRepository();
    const service = new UserService(mockRepository);
    
    // Act - Execute the behavior being tested
    const result = await service.createUser(userData);
    
    // Assert - Verify the outcome
    expect(result.email).toBe('test@example.com');
    expect(mockRepository.saveWasCalled).toBe(true);
  });
});
```

## Test Types

### Unit Tests
- Test individual functions, methods, or classes
- Mock all external dependencies
- Fast execution (milliseconds)
- Run on every commit
- Location: Co-located with source files or in `tests/unit/`

### Integration Tests
- Test interactions between components
- Use real dependencies where practical
- Test API endpoints, database interactions
- Run before merging to main branch
- Location: `tests/integration/`

### End-to-End Tests
- Test complete user workflows
- Use real or staging environment
- Focus on critical paths from PRD
- Run before releases
- Location: `tests/e2e/`

## Coverage Requirements

- Overall: >80%
- Business logic: >90%
- Critical paths: 100%
- New code: >90%

## 12-Factor App Testing Principles

### II. Dependencies - Test Dependency Isolation
- **Reproducible Test Environment**: Use same dependency management as production
- **Isolated Dependencies**: Each test run uses fresh, isolated dependencies
- **Mock External Services**: Don't rely on internet-accessible services in unit tests

**Example - JavaScript (Jest):**
```javascript
// Good - mocked external dependency
jest.mock('stripe');
const stripe = require('stripe');
stripe.mockImplementation(() => ({
  charges: { create: jest.fn().mockResolvedValue({ id: 'ch_123' }) }
}));

test('processes payment', async () => {
  const result = await processPayment({ amount: 1000 });
  expect(result.id).toBe('ch_123');
});

// Bad - real external service in tests
const stripe = require('stripe')(process.env.STRIPE_KEY); // Flaky tests!
```

**Example - Python (pytest with unittest.mock):**
```python
from unittest.mock import Mock, patch
import pytest

# Good - mocked external dependency
@patch('stripe.Charge')
def test_process_payment(mock_charge):
    mock_charge.create.return_value = Mock(id='ch_123')
    
    result = process_payment(amount=1000)
    assert result['id'] == 'ch_123'
    mock_charge.create.assert_called_once()

# Bad - real external service in tests
import stripe
stripe.api_key = os.environ['STRIPE_KEY']  # Flaky tests!
```

### III. Config - Test Configuration
- **Separate Test Config**: Use dedicated `.env.test` or test-specific environment variables
- **No Hardcoded Test Data**: Load test database URLs from environment
- **Config Validation Tests**: Test that app fails fast on missing required config

**Example - Python:**
```python
import os
import pytest

# Good - test config from environment
TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL', 'sqlite:///:memory:')

# Test config validation
def test_missing_required_config():
    # Save original value
    original = os.environ.get('DATABASE_URL')
    
    # Remove required config
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
    
    with pytest.raises(ValueError):
        app.load_config()
    
    # Restore original value
    if original:
        os.environ['DATABASE_URL'] = original
```

**Example - JavaScript:**
```javascript
describe('Config validation', () => {
  const originalEnv = process.env.DATABASE_URL;
  
  afterEach(() => {
    // Restore original environment
    if (originalEnv) {
      process.env.DATABASE_URL = originalEnv;
    }
  });
  
  it('fails fast on missing required config', () => {
    delete process.env.DATABASE_URL;
    
    expect(() => {
      loadConfig();
    }).toThrow('DATABASE_URL environment variable required');
  });
  
  it('uses test database from environment', () => {
    process.env.DATABASE_URL = 'postgresql://localhost:5432/testdb';
    const config = loadConfig();
    expect(config.databaseUrl).toBe('postgresql://localhost:5432/testdb');
  });
});
```

### IV. Backing Services - Test with Attached Resources
- **Swappable Test Resources**: Use in-memory databases for unit tests, real databases for integration tests
- **Container-Based Testing**: Use Docker Compose to spin up test backing services
- **Resource Cleanup**: Always clean up test data and connections

**Example - Docker Compose for Tests:**
```yaml
# docker-compose.test.yml
services:
  test-db:
    image: postgres:15
    environment:
      POSTGRES_DB: testdb
      POSTGRES_USER: testuser
      POSTGRES_PASSWORD: testpass
  test-redis:
    image: redis:7
```

### V. Build, Release, Run - Test Each Stage
- **Build Stage Tests**: Run unit tests during build
- **Release Stage Tests**: Validate configuration and dependencies
- **Run Stage Tests**: Integration and E2E tests in environment close to production

**CI/CD Pipeline:**
```yaml
stages:
  - build:
      - npm install
      - npm run lint
      - npm run test:unit
  - release:
      - npm run build
      - docker build -t app:${VERSION}
  - test:
      - npm run test:integration
      - npm run test:e2e
```

### VI. Processes - Test Stateless Behavior
- **No Shared State**: Tests must not depend on previous test state
- **Parallel Execution**: Tests should run safely in parallel
- **Process Independence**: Test that multiple instances can run simultaneously

**Example - JavaScript:**
```javascript
describe('Stateless API', () => {
  beforeEach(async () => {
    // Each test gets fresh state
    await database.clear();
    await redis.flushdb();
  });
  
  it('handles concurrent requests independently', async () => {
    const userData = { name: 'Test User', email: 'test@example.com' };
    
    // Test parallel request handling
    const requests = Array(10).fill().map(() => 
      api.post('/users', userData)
    );
    const responses = await Promise.all(requests);
    expect(responses.every(r => r.status === 201)).toBe(true);
  });
  
  it('does not share state between requests', async () => {
    // First request
    await api.post('/counter/increment');
    const response1 = await api.get('/counter');
    
    // Second request in different "process"
    await api.post('/counter/increment');
    const response2 = await api.get('/counter');
    
    // Both should read from external store, not in-memory
    expect(response2.data.count).toBe(2);
  });
});
```

**Example - Python (pytest):**
```python
import pytest
from httpx import AsyncClient

@pytest.fixture(autouse=True)
async def reset_state():
    """Each test gets fresh state"""
    await database.clear()
    await redis.flushdb()
    yield

@pytest.mark.asyncio
async def test_handles_concurrent_requests_independently():
    user_data = {'name': 'Test User', 'email': 'test@example.com'}
    
    # Test parallel request handling
    async with AsyncClient(app=app, base_url='http://test') as client:
        requests = [
            client.post('/users', json=user_data)
            for _ in range(10)
        ]
        responses = await asyncio.gather(*requests)
        assert all(r.status_code == 201 for r in responses)

@pytest.mark.asyncio
async def test_no_shared_state_between_requests():
    async with AsyncClient(app=app, base_url='http://test') as client:
        # First request
        await client.post('/counter/increment')
        response1 = await client.get('/counter')
        
        # Second request
        await client.post('/counter/increment')
        response2 = await client.get('/counter')
        
        # Both should read from external store
        assert response2.json()['count'] == 2
```

### IX. Disposability - Test Fast Startup and Graceful Shutdown
- **Startup Time Tests**: Assert application starts within acceptable timeframe
- **Shutdown Tests**: Verify graceful shutdown completes pending requests
- **Crash Recovery Tests**: Test that app recovers properly after forced termination

**Example - JavaScript:**
```javascript
test('app starts within 5 seconds', async () => {
  const startTime = Date.now();
  const app = await startApplication();
  const startupTime = Date.now() - startTime;
  expect(startupTime).toBeLessThan(5000);
  await app.close();
});

test('graceful shutdown completes pending requests', async () => {
  const app = await startApplication();
  const request = app.request('/slow-endpoint'); // Takes 2 seconds
  setTimeout(() => app.shutdown(), 100); // Shutdown while request in flight
  const response = await request;
  expect(response.status).toBe(200); // Request completed
});

test('app recovers after crash', async () => {
  const app1 = await startApplication();
  await app1.kill(); // Simulate crash
  
  const app2 = await startApplication();
  const response = await app2.request('/health');
  expect(response.status).toBe(200);
  await app2.close();
});
```

**Example - Python:**
```python
import pytest
import time
from datetime import datetime

@pytest.mark.asyncio
async def test_app_starts_within_5_seconds():
    start_time = time.time()
    app = await start_application()
    startup_time = time.time() - start_time
    assert startup_time < 5.0
    await app.close()

@pytest.mark.asyncio
async def test_graceful_shutdown_completes_pending_requests():
    app = await start_application()
    
    # Start slow request (takes 2 seconds)
    request_task = asyncio.create_task(
        app.request('/slow-endpoint')
    )
    
    # Shutdown while request in flight
    await asyncio.sleep(0.1)
    shutdown_task = asyncio.create_task(app.shutdown())
    
    # Request should complete
    response = await request_task
    assert response.status_code == 200
    await shutdown_task

@pytest.mark.asyncio
async def test_app_recovers_after_crash():
    app1 = await start_application()
    await app1.kill()  # Simulate crash
    
    app2 = await start_application()
    response = await app2.request('/health')
    assert response.status_code == 200
    await app2.close()
```

### X. Dev/Prod Parity - Test Environment Parity
- **Same Services**: Use same type of database in tests as in production (PostgreSQL not SQLite)
- **Same Dependencies**: Lock dependency versions in test and production
- **Container Testing**: Run tests in containers matching production environment

### XI. Logs - Test Logging Behavior
- **Capture stdout/stderr**: Verify logs are written to standard output
- **Structured Log Tests**: Validate log format and required fields
- **No Sensitive Data**: Test that logs don't contain secrets or PII

**Example - JavaScript:**
```javascript
const { captureStdout } = require('./test-utils');

test('logs are structured JSON', () => {
  const output = captureStdout(() => {
    logger.info('test message', { userId: 123 });
  });
  const logEntry = JSON.parse(output);
  expect(logEntry).toMatchObject({
    level: 'info',
    message: 'test message',
    userId: 123,
    timestamp: expect.any(String)
  });
});

test('passwords are never logged', () => {
  const output = captureStdout(() => {
    authenticateUser('user@example.com', 'secret123');
  });
  expect(output).not.toContain('secret123');
  expect(output).not.toContain('password');
});

test('logs written to stdout not files', () => {
  const consoleSpy = jest.spyOn(console, 'log');
  logger.info('test message');
  expect(consoleSpy).toHaveBeenCalled();
  consoleSpy.mockRestore();
});
```

**Example - Python:**
```python
import pytest
import json
import logging
from io import StringIO

def test_logs_are_structured_json(caplog):
    """Test that logs are structured JSON format"""
    with caplog.at_level(logging.INFO):
        logger.info('test message', extra={'user_id': 123})
    
    log_output = caplog.records[0].getMessage()
    log_entry = json.loads(log_output)
    assert log_entry['level'] == 'info'
    assert log_entry['message'] == 'test message'
    assert log_entry['user_id'] == 123
    assert 'timestamp' in log_entry

def test_passwords_never_logged(caplog):
    """Test that sensitive data is not logged"""
    with caplog.at_level(logging.INFO):
        authenticate_user('user@example.com', 'secret123')
    
    log_output = caplog.text
    assert 'secret123' not in log_output
    assert 'password' not in log_output.lower()

def test_logs_written_to_stdout(capsys):
    """Test that logs go to stdout"""
    logger.info('test message')
    captured = capsys.readouterr()
    assert 'test message' in captured.out
    assert captured.err == ''  # Nothing to stderr for info logs
```

---

*This file is conditionally included when working with test files.*
