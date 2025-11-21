# Karate Integration with x100 Template

This document explains how Karate API automation testing is integrated into the x100 template workflow.

## 🎯 Overview

Karate has been integrated as an enterprise-grade API automation testing solution for the x100 template. This integration provides:

- **BDD-style API testing** using Gherkin syntax
- **No coding required** for writing tests (DSL-based)
- **Parallel test execution** for faster feedback
- **Multi-environment support** (dev, qa, staging, prod)
- **Rich HTML reports** with detailed test results
- **CI/CD ready** with GitHub Actions workflow included

## 🔄 Integration Points

### 1. With x100 Workflow Commands

Karate tests can be integrated with the x100 workflow automation:

#### Using `/test` Command

```bash
# In Claude Code
/test karate
```

This will:
1. Navigate to the Karate test directory
2. Run the appropriate test suite
3. Generate reports
4. Return results

#### Using `/workflow` Command

When using the complete workflow automation:

```bash
/workflow docs/user-stories/US-001-api-feature.md
```

The workflow will automatically:
1. Create technical specification
2. Implement the code
3. **Run Karate API tests** (if API endpoints are involved)
4. Review code quality
5. Commit changes

### 2. With Test Automation Agent

The x100 template includes a test automation agent. Karate tests can be configured as part of the test suite:

**In `.claude/agents/tester.md`**, add Karate integration:

```markdown
For API testing:
- Use Karate DSL for REST API tests
- Run tests from tests/karate directory
- Command: `cd tests/karate && mvn test`
```

### 3. Directory Structure Integration

```
your-project/
├── .x100/                      # x100 template
│   ├── resources/
│   └── scripts/
├── .claude/                    # Claude Code configuration
│   ├── commands/
│   │   ├── test.md            # Can include Karate tests
│   │   └── workflow.md
│   └── agents/
│       └── tester.md          # Can use Karate for API testing
├── src/                        # Your application code
│   ├── backend/               # Backend API
│   └── frontend/
├── tests/
│   ├── karate/                # 🆕 Karate API tests
│   │   ├── pom.xml
│   │   ├── README.md
│   │   └── src/test/
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
└── docs/
```

## 🚀 Usage Scenarios

### Scenario 1: API Feature Development

When developing a new API feature:

1. **Create User Story**: `docs/user-stories/US-XXX-new-api.md`
2. **Run Workflow**: `/workflow docs/user-stories/US-XXX-new-api.md`
3. **Automated Process**:
   - Spec created
   - API code implemented
   - **Karate tests generated** based on spec
   - Tests executed
   - Results reviewed

### Scenario 2: Standalone API Testing

For testing existing APIs:

```bash
# Navigate to Karate directory
cd tests/karate

# Run specific test suite
mvn test -Dtest=TestRunner#testUsers

# Run with environment
mvn test -Dkarate.env=qa

# Run in parallel
mvn test -Pparallel
```

### Scenario 3: Regression Testing

For full regression testing:

```bash
# Run all tests in parallel
cd tests/karate
mvn test -Pparallel -Dkarate.env=staging

# Generate reports
open target/cucumber-html-reports/overview-features.html
```

## 🎨 Custom Workflow Integration

### Creating a Karate-Specific Command

Create `.claude/commands/test-api.md`:

```markdown
---
description: Run Karate API automation tests
---

You are an API testing expert. When the user asks you to test APIs:

1. Navigate to the Karate test directory: `cd tests/karate`
2. Analyze existing feature files to understand test coverage
3. Run appropriate tests based on the context:
   - For smoke testing: `mvn test -Dtest=TestRunner#testSmoke`
   - For specific feature: `mvn test -Dtest=TestRunner#test<Feature>`
   - For all tests: `mvn test -Pparallel`
4. Review the test results from the console output
5. If tests fail, analyze the failure and provide recommendations
6. Generate and show the HTML report: `target/cucumber-html-reports/overview-features.html`

Environment selection:
- Use `-Dkarate.env=dev` for development
- Use `-Dkarate.env=qa` for QA environment
- Use `-Dkarate.env=staging` for staging

Always provide:
- Test execution summary
- Pass/fail status
- Link to detailed reports
- Recommendations for failed tests
```

Enable the command:
```bash
./x100 command enable test-api
```

### Creating a Karate Test Generator Agent

Create `.claude/agents/karate-generator.md`:

```markdown
---
name: Karate Test Generator
description: Generates Karate feature files from API specifications
---

You are an expert in Karate DSL and API testing. Your role is to generate comprehensive Karate feature files based on API specifications.

When generating tests:

1. **Analyze the API Specification**:
   - Identify endpoints, methods, request/response formats
   - Note authentication requirements
   - Identify test data needs

2. **Generate Feature Files**:
   - Use proper Gherkin syntax
   - Include Background section for common setup
   - Create scenarios for happy path, edge cases, and error conditions
   - Use appropriate tags (@smoke, @regression, @negative)

3. **Include Assertions**:
   - Status code validation
   - Response body schema validation
   - Specific field validations
   - Performance assertions if needed

4. **Use Karate Features**:
   - Data-driven testing with Examples
   - Reusable scenarios from common.feature
   - Dynamic data generation with utils functions
   - Proper error handling

5. **Save to Correct Location**:
   - Save in `tests/karate/src/test/resources/karate/features/<domain>/`
   - Use descriptive filenames (e.g., `user-management.feature`)

6. **Update Test Data**:
   - Create/update JSON files in `tests/karate/src/test/resources/karate/data/`

Example structure:
```gherkin
Feature: <Feature Name>
  <Description>

  Background:
    * url baseUrl
    * def apiPath = '/api/v1/<resource>'

  @smoke
  Scenario: <Scenario Name>
    Given path apiPath
    When method GET
    Then status 200
    And match response == <expected>
```
```

Enable the agent:
```bash
./x100 agent enable karate-generator
```

## 📊 Reporting Integration

### Viewing Reports in Workflow

After running tests through the workflow, reports can be accessed:

```bash
# Karate HTML Report
open tests/karate/target/karate-reports/karate-summary.html

# Cucumber HTML Report (more detailed)
open tests/karate/target/cucumber-html-reports/overview-features.html
```

### CI/CD Integration

The included GitHub Actions workflow (`.github/workflows/karate-tests.yml`) automatically:
- Runs tests on push/PR
- Generates reports
- Uploads artifacts
- Posts results to PR comments

## 🔧 Configuration

### Environment Variables

Set in `.claude/settings.json` or environment:

```json
{
  "karate": {
    "defaultEnv": "dev",
    "parallelThreads": 5,
    "timeout": 30000
  }
}
```

### Test Data Management

Test data is organized in `tests/karate/src/test/resources/karate/data/`:

- `users.json` - User test data
- `test-credentials.json` - Authentication credentials
- Add more as needed for your domain

## 🎯 Best Practices

### 1. Feature Organization

Organize tests by domain/resource:
```
features/
├── auth/           # Authentication tests
├── users/          # User management tests
├── products/       # Product tests
└── common/         # Reusable scenarios
```

### 2. Tagging Strategy

Use consistent tags:
- `@smoke` - Critical path tests
- `@regression` - Full regression suite
- `@negative` - Negative test cases
- `@<feature>` - Feature-specific tests

### 3. Test Independence

Each test should:
- Set up its own data
- Clean up after itself
- Not depend on other tests

### 4. Naming Conventions

- Feature files: `kebab-case.feature`
- Scenarios: Descriptive sentences
- Variables: `camelCase`

## 🐛 Troubleshooting

### Issue: Maven not found

```bash
# Install Maven
brew install maven  # macOS
apt install maven   # Linux
```

### Issue: Java version mismatch

```bash
# Check Java version
java -version

# Install correct version
brew install openjdk@11  # macOS
```

### Issue: Tests fail in CI but pass locally

- Check environment configuration
- Verify test data availability
- Review timeout settings
- Check network/connectivity

## 📚 Additional Resources

- [Karate README](./README.md) - Detailed Karate documentation
- [x100 Workflow Guide](../../resources/WORKFLOW.md) - Complete workflow documentation
- [Karate Official Docs](https://github.com/karatelabs/karate)

## 🤝 Contributing

When adding new API features:
1. Write Karate tests alongside code
2. Add tests to appropriate feature directory
3. Update test data if needed
4. Run tests before committing
5. Ensure CI pipeline passes

## 📝 Summary

Karate is now fully integrated into the x100 template, providing:
- ✅ Enterprise-grade API testing
- ✅ Seamless workflow integration
- ✅ CI/CD ready setup
- ✅ Comprehensive reporting
- ✅ Multi-environment support
- ✅ Parallel execution capabilities

Use Karate for all API testing needs in your x100-powered projects!
