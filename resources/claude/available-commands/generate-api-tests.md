---
description: Generate Karate test features from API specifications
---

You are generating Karate test features from API specifications. Follow these steps:

**Input**: $ARGUMENTS (API specification file path or inline spec)

**Process**:

1. **Read API specification**:
   - Parse OpenAPI/Swagger spec (if provided)
   - Read technical spec document (if provided)
   - Extract endpoint details, request/response formats
   - Identify authentication requirements

2. **Analyze endpoints**:
   - List all endpoints with methods (GET, POST, PUT, DELETE, etc.)
   - Identify request parameters and body schemas
   - Note response codes and schemas
   - Identify test data requirements

3. **Generate Karate feature file**:
   - Create feature file with proper Gherkin syntax
   - Include Background section for common setup
   - Generate scenarios for:
     * Happy path (successful operations)
     * Validation tests (input validation)
     * Error cases (4xx, 5xx responses)
     * Edge cases
   - Use appropriate tags (@smoke, @regression, @negative)
   - Include data-driven tests with Examples (if applicable)

4. **Feature structure**:
   ```gherkin
   Feature: <Resource Name> API Tests
     Description of what's being tested

     Background:
       * url baseUrl
       * def apiPath = '/api/v1/<resource>'
       * configure headers = headers

     @smoke @<resource>
     Scenario: Get all <resources>
       Given path apiPath
       When method GET
       Then status 200
       And match response == '#array'

     @<resource> @crud
     Scenario: Create new <resource>
       * def resourceData = { ... }
       Given path apiPath
       And request resourceData
       When method POST
       Then status 201
       And match response.id == '#number'
   ```

5. **Create test data**:
   - Generate JSON test data files in `tests/karate/src/test/resources/karate/data/`
   - Include valid and invalid test data
   - Create data for edge cases

6. **Save files**:
   - Save feature file to: `tests/karate/src/test/resources/karate/features/<domain>/<name>.feature`
   - Save test data to: `tests/karate/src/test/resources/karate/data/<name>.json`

7. **Validate generated tests**:
   - Check syntax is valid
   - Ensure all required assertions are present
   - Verify test independence

8. **Update test runner** (if needed):
   - Add test method to TestRunner.java if new feature category

9. **Document the tests**:
   - Add comments explaining complex scenarios
   - Document any prerequisites or dependencies

**Output**: 
- Generated feature file(s)
- Test data files
- Summary of test coverage
- Instructions to run the tests

**Example Usage**:
- `/generate-api-tests docs/specs/user-api.yaml`
- `/generate-api-tests "User API with CRUD operations"`
