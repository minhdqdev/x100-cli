# Karate API Automation Testing

Enterprise-grade API automation testing framework using [Karate DSL](https://github.com/karatelabs/karate). This module provides comprehensive REST API testing capabilities with built-in support for parallel execution, multiple environments, and rich reporting.

## 🎯 Features

- **BDD-Style Tests**: Write tests in Gherkin syntax - easy to read and maintain
- **No Coding Required**: Pure DSL approach - no Java/programming knowledge needed for writing tests
- **Parallel Execution**: Run tests in parallel for faster feedback
- **Multiple Environments**: Support for dev, qa, staging, and production environments
- **Rich Assertions**: Built-in matchers for JSON, XML, and text validation
- **Data-Driven Testing**: Support for scenario outlines and external test data
- **Comprehensive Reporting**: HTML reports with detailed test results
- **Retry Mechanism**: Automatic retry for flaky tests
- **CI/CD Ready**: Easy integration with Jenkins, GitLab CI, GitHub Actions

## 📋 Prerequisites

- **Java 11+** (required for Karate)
- **Maven 3.6+** (for dependency management and test execution)

### Installing Java and Maven

**macOS:**
```bash
# Install Java
brew install openjdk@11

# Install Maven
brew install maven
```

**Linux (Ubuntu/Debian):**
```bash
# Install Java
sudo apt update
sudo apt install openjdk-11-jdk

# Install Maven
sudo apt install maven
```

**Windows:**
- Download and install [Java JDK 11+](https://adoptium.net/)
- Download and install [Maven](https://maven.apache.org/download.cgi)

### Verify Installation

```bash
java -version   # Should show Java 11 or higher
mvn -version    # Should show Maven 3.6 or higher
```

## 🚀 Quick Start

### 1. Navigate to Karate Directory

```bash
cd tests/karate
```

### 2. Run All Tests

```bash
# Run all tests sequentially
mvn test

# Run all tests in parallel (5 threads)
mvn test -Pparallel

# Run with specific environment
mvn test -Dkarate.env=qa

# Run smoke tests only
mvn test -Dtest=TestRunner#testSmoke
```

### 3. View Test Reports

After test execution, reports are generated in multiple formats:

- **Karate HTML Report**: `target/karate-reports/karate-summary.html`
- **Cucumber HTML Report**: `target/cucumber-html-reports/overview-features.html`
- **JUnit XML**: `target/surefire-reports/`

Open in browser:
```bash
# macOS
open target/cucumber-html-reports/overview-features.html

# Linux
xdg-open target/cucumber-html-reports/overview-features.html

# Windows
start target/cucumber-html-reports/overview-features.html
```

## 📁 Project Structure

```
tests/karate/
├── pom.xml                                    # Maven configuration
├── README.md                                  # This file
├── src/test/
│   ├── java/karate/
│   │   ├── TestRunner.java                   # Sequential test runner
│   │   └── ParallelRunner.java               # Parallel test runner
│   └── resources/
│       ├── karate-config.js                  # Global configuration
│       └── karate/
│           ├── features/                     # Test feature files
│           │   ├── auth/
│           │   │   └── authentication.feature
│           │   ├── users/
│           │   │   └── users.feature
│           │   └── common/
│           │       └── common.feature        # Reusable scenarios
│           ├── data/                         # Test data files
│           │   ├── users.json
│           │   └── test-credentials.json
│           └── config/                       # Environment configs
│               ├── dev.properties
│               └── qa.properties
└── target/                                   # Generated reports (git-ignored)
```

## ✍️ Writing Tests

### Basic Test Structure

```gherkin
Feature: User API Tests

  Background:
    * url baseUrl
    * def apiPath = '/api/v1/users'

  Scenario: Get all users
    Given path apiPath
    When method GET
    Then status 200
    And match response == '#array'
```

### Using Test Data

```gherkin
Scenario: Create user with test data
  * def userData = read('classpath:karate/data/users.json')[0]
  Given path '/api/v1/users'
  And request userData
  When method POST
  Then status 201
```

### Data-Driven Tests

```gherkin
Scenario Outline: Search users
  Given path '/api/v1/users'
  And param name = '<searchName>'
  When method GET
  Then status 200

  Examples:
    | searchName |
    | John       |
    | Jane       |
```

### Calling Reusable Scenarios

```gherkin
Scenario: Use shared login
  * def loginResult = call read('classpath:karate/features/common/common.feature@Login')
  * def token = loginResult.accessToken
  
  Given path '/api/v1/users/me'
  And header Authorization = 'Bearer ' + token
  When method GET
  Then status 200
```

## 🎨 Advanced Features

### JSON Matching

```gherkin
# Exact match
* match response == { id: 1, name: 'John' }

# Fuzzy match with data types
* match response == { id: '#number', name: '#string' }

# Array matching
* match response == '#array'
* match each response == { id: '#number', name: '#string' }

# Contains matching
* match response contains { name: 'John' }

# Optional fields
* match response == { id: '#number', email: '##string' }
```

### Dynamic Values

```gherkin
# Generate random email
* def randomEmail = utils.randomEmail()

# Generate UUID
* def uuid = utils.uuid()

# Get current timestamp
* def timestamp = utils.timestamp()
```

### Retry Logic

```gherkin
# Configure retry for specific scenario
* configure retry = { count: 5, interval: 2000 }
Given path '/api/v1/status'
When method GET
Then status 200
And match response.status == 'completed'
```

### File Upload

```gherkin
Given path '/api/v1/upload'
And multipart file file = { read: 'test.pdf', filename: 'test.pdf' }
When method POST
Then status 200
```

### Database Validation

```gherkin
* def config = { username: 'dbuser', password: 'dbpass', url: 'jdbc:postgresql://localhost:5432/testdb', driverClassName: 'org.postgresql.Driver' }
* def DbUtils = Java.type('com.intuit.karate.core.MockUtils')
* def result = DbUtils.getDbResult(config, 'SELECT * FROM users WHERE id = 1')
* match result[0].name == 'John Doe'
```

## 🏃 Running Tests

### By Test Runner

```bash
# Sequential execution
mvn test -Dtest=TestRunner

# Parallel execution (5 threads)
mvn test -Dtest=ParallelRunner

# Specific test method
mvn test -Dtest=TestRunner#testUsers
mvn test -Dtest=TestRunner#testAuth
```

### By Tags

```bash
# Run smoke tests
mvn test -Dkarate.options="--tags @smoke"

# Run specific feature
mvn test -Dkarate.options="--tags @users"

# Exclude tests
mvn test -Dkarate.options="--tags ~@negative"

# Multiple tags (AND)
mvn test -Dkarate.options="--tags @smoke,@users"
```

### By Environment

```bash
# Run in QA environment
mvn test -Dkarate.env=qa

# Run in staging
mvn test -Dkarate.env=staging

# Run in production
mvn test -Dkarate.env=prod
```

### Parallel Execution

```bash
# Use parallel profile with custom thread count
mvn test -Pparallel -Dkarate.threads=10

# Parallel execution with specific environment
mvn test -Pparallel -Dkarate.env=qa -Dkarate.threads=8
```

## 🔧 Configuration

### Environment Configuration

Edit `karate-config.js` to add or modify environment settings:

```javascript
if (env === 'prod') {
  config.baseUrl = 'https://api.production.com';
  config.apiUrl = 'https://api.production.com/api/v1';
  config.debugMode = false;
}
```

### Authentication

Configure authentication in `karate-config.js`:

```javascript
// Basic Auth
config.auth.basicAuth = {
  username: 'user',
  password: 'pass'
};

// Bearer Token
config.auth.bearerToken = 'your-token-here';

// API Key
config.auth.apiKey = 'your-api-key';
```

### Custom Properties

Pass custom properties at runtime:

```bash
mvn test -Dauth.username=myuser -Dauth.password=mypass
```

## 📊 Reporting

### Report Types

1. **Karate Timeline Report** - Visual timeline of test execution
2. **Cucumber HTML Report** - Detailed feature and scenario results
3. **JUnit XML** - For CI/CD integration

### Generating Reports

Reports are automatically generated after test execution. To regenerate:

```bash
mvn test
# Reports will be in:
# - target/karate-reports/
# - target/cucumber-html-reports/
# - target/surefire-reports/
```

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
name: Karate Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up JDK 11
        uses: actions/setup-java@v3
        with:
          java-version: '11'
          distribution: 'temurin'
      - name: Run Karate Tests
        run: |
          cd tests/karate
          mvn test -Pparallel
      - name: Upload Test Reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: tests/karate/target/cucumber-html-reports/
```

### GitLab CI

```yaml
karate-tests:
  stage: test
  image: maven:3.8-openjdk-11
  script:
    - cd tests/karate
    - mvn test -Pparallel -Dkarate.env=qa
  artifacts:
    when: always
    paths:
      - tests/karate/target/cucumber-html-reports/
    reports:
      junit: tests/karate/target/surefire-reports/TEST-*.xml
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Karate Tests') {
            steps {
                dir('tests/karate') {
                    sh 'mvn clean test -Pparallel'
                }
            }
        }
    }
    post {
        always {
            publishHTML([
                reportDir: 'tests/karate/target/cucumber-html-reports',
                reportFiles: 'overview-features.html',
                reportName: 'Karate Test Report'
            ])
            junit 'tests/karate/target/surefire-reports/*.xml'
        }
    }
}
```

## 🐛 Debugging

### Enable Debug Logging

```bash
# Run with debug output
mvn test -Dlogback.configurationFile=logback-test.xml
```

### Debug Single Scenario

Add `@debug` tag to scenario and run:

```gherkin
@debug
Scenario: Debug this test
  Given path '/api/v1/users'
  When method GET
  Then status 200
```

```bash
mvn test -Dkarate.options="--tags @debug"
```

### View Request/Response

Enable in `karate-config.js`:

```javascript
karate.configure('logPrettyRequest', true);
karate.configure('logPrettyResponse', true);
```

## 📝 Best Practices

1. **Use Background** for common setup across scenarios
2. **Tag Tests** appropriately (@smoke, @regression, @slow)
3. **Externalize Test Data** in JSON files
4. **Create Reusable Scenarios** in common.feature
5. **Use Meaningful Names** for scenarios and features
6. **Keep Tests Independent** - avoid dependencies between tests
7. **Use Parallel Execution** for faster feedback
8. **Version Control Reports** - add target/ to .gitignore
9. **Environment Variables** for sensitive data
10. **Regular Maintenance** - update dependencies and clean up old tests

## 🔗 Useful Resources

- [Karate Documentation](https://github.com/karatelabs/karate)
- [Karate Examples](https://github.com/karatelabs/karate/tree/master/karate-demo)
- [Karate Forum](https://github.com/karatelabs/karate/discussions)
- [API Testing Best Practices](https://github.com/karatelabs/karate/wiki/Best-Practices)

## 🆘 Troubleshooting

### Common Issues

**Issue: Tests fail with connection timeout**
```bash
# Increase timeout in karate-config.js
config.defaultTimeout = 60000;  // 60 seconds
```

**Issue: Parallel tests failing**
```bash
# Reduce thread count
mvn test -Pparallel -Dkarate.threads=3
```

**Issue: Report not generated**
```bash
# Clean and rebuild
mvn clean test
```

**Issue: Java version mismatch**
```bash
# Check Java version
java -version

# Set JAVA_HOME if needed
export JAVA_HOME=/path/to/java11
```

## 📞 Support

For issues or questions:
1. Check the [Karate documentation](https://github.com/karatelabs/karate)
2. Search [existing issues](https://github.com/karatelabs/karate/issues)
3. Open a new issue with detailed information

## 📄 License

This Karate test suite is part of the x100-template project and follows the same license.
