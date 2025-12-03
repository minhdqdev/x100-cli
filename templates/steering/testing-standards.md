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

---

*This file is conditionally included when working with test files.*
