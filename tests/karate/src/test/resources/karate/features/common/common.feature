@ignore
Feature: Reusable Common Functions
  This feature contains reusable functions and scenarios that can be called from other feature files

  Scenario: Login and get access token
    * def loginData = { username: '#(username)', password: '#(password)' }
    Given url baseUrl
    And path '/api/v1/auth/login'
    And request loginData
    When method POST
    Then status 200
    * def accessToken = response.token
    * def userId = response.user.id

  Scenario: Create test user
    * def randomEmail = utils.randomEmail()
    * def userData = 
    """
    {
      name: '#(name)',
      email: '#(randomEmail)',
      age: 25
    }
    """
    Given url baseUrl
    And path '/api/v1/users'
    And request userData
    When method POST
    Then status 201
    * def createdUserId = response.id
    * def createdUserEmail = response.email

  Scenario: Delete test user
    Given url baseUrl
    And path '/api/v1/users/' + userId
    When method DELETE
    Then status 204

  Scenario: Wait for async operation
    * def maxRetries = 10
    * def retryCount = 0
    * def statusPath = '/api/v1/status/' + operationId
    * def continue = true
    * def status = null
    
    Given url baseUrl
    * configure retry = { count: maxRetries, interval: 2000 }
    And path statusPath
    When method GET
    Then status 200
    * def status = response.status
    * assert status == 'completed'

  Scenario: Generate auth headers
    * def authHeaders = 
    """
    {
      'Authorization': 'Bearer #(token)',
      'Content-Type': 'application/json'
    }
    """
