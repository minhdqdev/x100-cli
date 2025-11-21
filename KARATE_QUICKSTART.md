# Karate API Testing - Quick Start Guide

This guide will get you started with Karate API automation testing in the x100 template in under 5 minutes.

## 📋 Prerequisites

Install Java and Maven (if not already installed):

**macOS:**
```bash
brew install openjdk@11 maven
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install openjdk-11-jdk maven
```

**Windows:**
- Download [Java JDK 11+](https://adoptium.net/)
- Download [Maven](https://maven.apache.org/download.cgi)

Verify installation:
```bash
java -version   # Should show Java 11+
mvn -version    # Should show Maven 3.6+
```

## 🚀 Quick Start (3 Steps)

### Step 1: Navigate to Karate Directory
```bash
cd tests/karate
```

### Step 2: Run Your First Test
```bash
# Run smoke tests (fastest)
./run-tests.sh smoke

# Or run all tests
./run-tests.sh all
```

### Step 3: View Results
```bash
# Open HTML report
./run-tests.sh report

# Or manually open:
open target/cucumber-html-reports/overview-features.html
```

That's it! You've just run your first Karate tests. ✅

## 📚 What's Included

The integration includes example tests for:

- **User Management** - CRUD operations, search, pagination
- **Authentication** - Login, registration, token refresh, logout
- **Product Management** - Product CRUD, inventory, search

All tests are production-ready and demonstrate best practices.

## 🎯 Common Tasks

### Run Different Test Suites

```bash
cd tests/karate

# Run smoke tests only (quick validation)
./run-tests.sh smoke

# Run specific feature tests
./run-tests.sh users        # User management tests
./run-tests.sh auth         # Authentication tests

# Run by tag
./run-tests.sh tags @regression

# Run all tests in parallel (faster)
./run-tests.sh parallel
```

### Run in Different Environments

```bash
# Development (default)
./run-tests.sh all

# QA environment
./run-tests.sh all -e qa

# Staging environment
./run-tests.sh all -e staging
```

### Parallel Execution

```bash
# Run with 5 threads (default)
./run-tests.sh parallel

# Run with 10 threads (faster)
./run-tests.sh parallel -t 10

# Run in QA with 8 threads
./run-tests.sh parallel -e qa -t 8
```

## ✍️ Writing Your First Test

Create a new feature file at `tests/karate/src/test/resources/karate/features/my-api/my-test.feature`:

```gherkin
Feature: My First API Test

  Background:
    * url baseUrl
    * def apiPath = '/api/v1/my-resource'

  @smoke
  Scenario: Get my resource
    Given path apiPath
    When method GET
    Then status 200
    And match response == '#array'
```

Run your test:
```bash
cd tests/karate
mvn test -Dkarate.options="--tags @smoke"
```

## 🔧 Using with x100 Workflow

### In Claude Code

Enable the Karate commands:
```bash
# From project root
./x100 command enable test-api
./x100 command enable generate-api-tests
./x100 agent enable karate-test-generator
```

Then use in Claude Code:
```bash
# Run API tests
/test-api

# Run smoke tests
/test-api smoke

# Run specific tests
/test-api users

# Generate tests from spec
/generate-api-tests docs/api-spec.yaml
```

### In Automated Workflow

When using `/workflow`:
```bash
/workflow docs/user-stories/US-001-api-feature.md
```

The workflow will automatically:
1. Create API implementation
2. Generate Karate tests
3. Run tests
4. Report results

## 📊 Understanding Reports

After running tests, you get:

### 1. Karate Summary Report
- Location: `target/karate-reports/karate-summary.html`
- Shows: Timeline, scenarios, pass/fail status

### 2. Cucumber HTML Report (Detailed)
- Location: `target/cucumber-html-reports/overview-features.html`
- Shows: Feature-by-feature results, screenshots, logs

### 3. JUnit XML (for CI/CD)
- Location: `target/surefire-reports/TEST-*.xml`
- Used by: Jenkins, GitLab CI, GitHub Actions

## 🔍 Debugging Failed Tests

If a test fails:

1. **Check the console output** - shows the failure reason
2. **Open HTML report** - detailed error information
3. **Enable debug mode**:
   ```bash
   ./run-tests.sh all -d
   ```
4. **Run single scenario** - faster debugging
   ```bash
   mvn test -Dkarate.options="--tags @debug"
   ```

## 🎨 Test Features

### Dynamic Data
```gherkin
# Random email
* def email = utils.randomEmail()

# Random UUID
* def id = utils.uuid()

# Timestamp
* def timestamp = utils.timestamp()
```

### Assertions
```gherkin
# Exact match
* match response == { id: 1, name: 'John' }

# Type matching
* match response == { id: '#number', name: '#string' }

# Array matching
* match response == '#array'
* match each response == { id: '#number' }

# Contains
* match response contains { name: 'John' }
```

### Data-Driven Tests
```gherkin
Scenario Outline: Test with multiple values
  Given path '/api/search'
  And param q = '<query>'
  When method GET
  Then status 200

  Examples:
    | query  |
    | apple  |
    | banana |
    | orange |
```

### Reusable Scenarios
```gherkin
# Call login from common.feature
* def login = call read('classpath:karate/features/common/common.feature@login')
* def token = login.accessToken
```

## 🚨 Common Issues

### "java: command not found"
```bash
# Install Java
brew install openjdk@11  # macOS
sudo apt install openjdk-11-jdk  # Linux
```

### "mvn: command not found"
```bash
# Install Maven
brew install maven  # macOS
sudo apt install maven  # Linux
```

### Tests time out
Increase timeout in `karate-config.js`:
```javascript
config.defaultTimeout = 60000;  // 60 seconds
```

### Port already in use
Change the port in your environment config or stop the conflicting service.

## 📖 Next Steps

1. **Read Full Documentation**
   - [Karate README](tests/karate/README.md) - Comprehensive guide
   - [Integration Guide](tests/karate/INTEGRATION.md) - x100 workflow integration

2. **Explore Example Tests**
   - `tests/karate/src/test/resources/karate/features/users/` - User tests
   - `tests/karate/src/test/resources/karate/features/auth/` - Auth tests

3. **Check CI/CD Setup**
   - `.github/workflows/karate-tests.yml` - GitHub Actions workflow

4. **Learn Karate DSL**
   - [Official Karate Documentation](https://github.com/karatelabs/karate)
   - [Karate Examples](https://github.com/karatelabs/karate/tree/master/karate-demo)

## 💡 Pro Tips

1. **Use tags** - `@smoke`, `@regression` for selective execution
2. **Run in parallel** - Much faster for large test suites
3. **External test data** - Use JSON files for test data
4. **Environment configs** - Separate configs for dev/qa/staging/prod
5. **CI/CD integration** - Automated testing on every commit

## 🎯 Example Workflow

Complete workflow for API development:

```bash
# 1. Write code
vim src/api/users.py

# 2. Generate tests
./x100
# Select: Generate API Tests

# 3. Run tests locally
cd tests/karate
./run-tests.sh smoke

# 4. Fix any failures
vim src/test/resources/karate/features/users/users.feature

# 5. Run full suite
./run-tests.sh parallel

# 6. Commit and push
git add .
git commit -m "feat: add user API with tests"
git push

# 7. CI/CD runs tests automatically
# Check GitHub Actions for results
```

## 🆘 Need Help?

- **Karate Issues**: https://github.com/karatelabs/karate/issues
- **x100 Issues**: https://github.com/minhdqdev/x100-template/issues
- **Documentation**: Check the READMEs in `tests/karate/`

## ✅ Checklist

Before committing:
- [ ] Tests pass locally
- [ ] Code coverage is adequate
- [ ] Tests are tagged appropriately
- [ ] Test data is externalized
- [ ] Tests are documented
- [ ] CI/CD pipeline passes

---

**You're all set!** Start writing amazing API tests with Karate! 🚀
