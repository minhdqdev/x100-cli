---
description: Run Karate API automation tests
---

You are running Karate API automation tests. Follow these steps:

**Input**: $ARGUMENTS (optional: test scope like 'smoke', 'users', 'auth', or tag like '@smoke')

**Process**:

1. **Navigate to Karate directory**:
   ```bash
   cd tests/karate
   ```

2. **Determine test scope**:
   - If no arguments: run all tests
   - If 'smoke': run smoke tests only
   - If 'users', 'auth', 'products': run specific feature tests
   - If starts with '@': run tests with specific tag
   - If environment specified (dev/qa/staging/prod): use that environment

3. **Check prerequisites**:
   - Verify Java is installed (java -version)
   - Verify Maven is installed (mvn -version)
   - If missing, provide installation instructions

4. **Run appropriate tests**:
   ```bash
   # All tests
   ./run-tests.sh all
   
   # Smoke tests
   ./run-tests.sh smoke
   
   # Specific feature
   ./run-tests.sh users
   
   # With specific environment
   ./run-tests.sh all -e qa
   
   # Parallel execution
   ./run-tests.sh parallel -e qa -t 5
   
   # By tag
   ./run-tests.sh tags @smoke
   ```

5. **Monitor execution**:
   - Show test progress
   - Report any failures immediately
   - Capture error messages

6. **Generate and analyze results**:
   - Show test summary (passed/failed counts)
   - Display execution time
   - Show report locations

7. **If tests fail**:
   - Show failure details
   - Analyze root cause
   - Suggest fixes
   - Offer to re-run after fixes

8. **Present results**:
   - Summary statistics
   - Link to HTML reports
   - Any recommendations

**Output**: Test execution results and report locations

**Example commands**:
- `/test-api` - Run all tests
- `/test-api smoke` - Run smoke tests
- `/test-api users` - Run user tests
- `/test-api @regression` - Run regression tests
- `/test-api qa` - Run all tests in QA environment
