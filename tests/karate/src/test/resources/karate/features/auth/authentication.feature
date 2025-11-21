Feature: Authentication API Tests
  As an API consumer
  I want to test authentication endpoints
  So that I can ensure secure access to the API

  Background:
    * url baseUrl
    * def authPath = '/api/v1/auth'

  @smoke @auth
  Scenario: User login with valid credentials
    * def credentials = read('classpath:karate/data/test-credentials.json')
    * def loginData = 
    """
    {
      username: '#(credentials.testUser.username)',
      password: '#(credentials.testUser.password)'
    }
    """
    Given path authPath + '/login'
    And request loginData
    When method POST
    Then status 200
    And match response == 
    """
    {
      token: '#string',
      refreshToken: '#string',
      expiresIn: '#number',
      user: {
        id: '#number',
        username: '#string',
        email: '#string'
      }
    }
    """
    * def accessToken = response.token
    * def userId = response.user.id

  @auth @negative
  Scenario: User login with invalid credentials
    * def invalidLogin = 
    """
    {
      username: 'wronguser',
      password: 'wrongpass'
    }
    """
    Given path authPath + '/login'
    And request invalidLogin
    When method POST
    Then status 401
    And match response.error == '#string'
    And match response.message contains 'Invalid credentials'

  @auth
  Scenario: User registration
    * def randomEmail = utils.randomEmail()
    * def registrationData = 
    """
    {
      username: 'newuser_#(utils.timestamp())',
      email: '#(randomEmail)',
      password: 'SecurePass123!',
      firstName: 'New',
      lastName: 'User'
    }
    """
    Given path authPath + '/register'
    And request registrationData
    When method POST
    Then status 201
    And match response == 
    """
    {
      id: '#number',
      username: '#string',
      email: '#(randomEmail)',
      firstName: 'New',
      lastName: 'User',
      createdAt: '#string'
    }
    """

  @auth @validation
  Scenario: Registration with weak password should fail
    * def weakPasswordData = 
    """
    {
      username: 'testuser',
      email: 'test@example.com',
      password: '123'
    }
    """
    Given path authPath + '/register'
    And request weakPasswordData
    When method POST
    Then status 400
    And match response.error contains 'password'

  @auth
  Scenario: Refresh access token
    # First login to get tokens
    * def credentials = read('classpath:karate/data/test-credentials.json')
    * def loginData = { username: '#(credentials.testUser.username)', password: '#(credentials.testUser.password)' }
    Given path authPath + '/login'
    And request loginData
    When method POST
    Then status 200
    * def refreshToken = response.refreshToken
    
    # Now refresh the token
    * def refreshData = { refreshToken: '#(refreshToken)' }
    Given path authPath + '/refresh'
    And request refreshData
    When method POST
    Then status 200
    And match response == 
    """
    {
      token: '#string',
      refreshToken: '#string',
      expiresIn: '#number'
    }
    """

  @auth
  Scenario: Access protected endpoint with valid token
    # First login
    * def credentials = read('classpath:karate/data/test-credentials.json')
    * def loginData = { username: '#(credentials.testUser.username)', password: '#(credentials.testUser.password)' }
    Given path authPath + '/login'
    And request loginData
    When method POST
    Then status 200
    * def accessToken = response.token
    
    # Access protected resource
    Given path '/api/v1/users/me'
    And header Authorization = 'Bearer ' + accessToken
    When method GET
    Then status 200
    And match response == 
    """
    {
      id: '#number',
      username: '#string',
      email: '#string'
    }
    """

  @auth @negative
  Scenario: Access protected endpoint without token
    Given path '/api/v1/users/me'
    When method GET
    Then status 401
    And match response.error contains 'unauthorized'

  @auth @negative
  Scenario: Access protected endpoint with invalid token
    Given path '/api/v1/users/me'
    And header Authorization = 'Bearer invalid_token_12345'
    When method GET
    Then status 401
    And match response.error contains 'token'

  @auth
  Scenario: User logout
    # First login
    * def credentials = read('classpath:karate/data/test-credentials.json')
    * def loginData = { username: '#(credentials.testUser.username)', password: '#(credentials.testUser.password)' }
    Given path authPath + '/login'
    And request loginData
    When method POST
    Then status 200
    * def accessToken = response.token
    
    # Logout
    Given path authPath + '/logout'
    And header Authorization = 'Bearer ' + accessToken
    When method POST
    Then status 200
    
    # Verify token is invalidated
    Given path '/api/v1/users/me'
    And header Authorization = 'Bearer ' + accessToken
    When method GET
    Then status 401

  @auth
  Scenario: Password reset request
    * def resetRequest = { email: 'testuser@example.com' }
    Given path authPath + '/password/reset-request'
    And request resetRequest
    When method POST
    Then status 200
    And match response.message == '#string'

  @auth
  Scenario: Password reset with token
    # Note: In real scenarios, reset token would be obtained from password reset request
    # or test data. This uses a placeholder token for demonstration.
    * def resetToken = karate.properties['test.resetToken'] || 'test-reset-token-' + utils.uuid()
    * def resetData = 
    """
    {
      resetToken: '#(resetToken)',
      newPassword: 'NewSecurePass123!'
    }
    """
    Given path authPath + '/password/reset'
    And request resetData
    When method POST
    Then status 200
    And match response.message contains 'success'
