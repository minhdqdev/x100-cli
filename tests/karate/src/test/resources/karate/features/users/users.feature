Feature: User Management API Tests
  As an API consumer
  I want to test user management endpoints
  So that I can ensure the API works correctly

  Background:
    * url baseUrl
    * def apiPath = '/api/v1/users'
    * configure headers = headers

  @smoke @users
  Scenario: Get all users
    Given path apiPath
    When method GET
    Then status 200
    And match response == '#array'
    And match each response == { id: '#number', name: '#string', email: '#string' }

  @smoke @users
  Scenario: Get user by ID
    Given path apiPath + '/1'
    When method GET
    Then status 200
    And match response == 
    """
    {
      id: '#number',
      name: '#string',
      email: '#string',
      createdAt: '#string',
      updatedAt: '#string'
    }
    """
    And match response.id == 1

  @users @crud
  Scenario: Create a new user
    * def randomEmail = utils.randomEmail()
    * def userData = 
    """
    {
      name: 'Test User',
      email: '#(randomEmail)',
      age: 25
    }
    """
    Given path apiPath
    And request userData
    When method POST
    Then status 201
    And match response.id == '#number'
    And match response.name == userData.name
    And match response.email == userData.email
    * def userId = response.id

  @users @crud
  Scenario: Update an existing user
    # First create a user
    * def randomEmail = utils.randomEmail()
    * def userData = { name: 'Original Name', email: '#(randomEmail)' }
    Given path apiPath
    And request userData
    When method POST
    Then status 201
    * def userId = response.id
    
    # Now update the user
    * def updateData = { name: 'Updated Name', email: '#(randomEmail)' }
    Given path apiPath + '/' + userId
    And request updateData
    When method PUT
    Then status 200
    And match response.name == 'Updated Name'
    And match response.id == userId

  @users @crud
  Scenario: Delete a user
    # First create a user
    * def randomEmail = utils.randomEmail()
    * def userData = { name: 'To Delete', email: '#(randomEmail)' }
    Given path apiPath
    And request userData
    When method POST
    Then status 201
    * def userId = response.id
    
    # Now delete the user
    Given path apiPath + '/' + userId
    When method DELETE
    Then status 204
    
    # Verify user is deleted
    Given path apiPath + '/' + userId
    When method GET
    Then status 404

  @users @validation
  Scenario: Create user with invalid data should fail
    * def invalidUserData = { name: '' }
    Given path apiPath
    And request invalidUserData
    When method POST
    Then status 400
    And match response.error == '#string'

  @users @search
  Scenario Outline: Search users by name
    Given path apiPath
    And param name = '<searchName>'
    When method GET
    Then status 200
    And match response == '#array'
    And match each response contains { name: '#string' }

    Examples:
      | searchName |
      | John       |
      | Jane       |
      | Test       |

  @users @pagination
  Scenario: Get users with pagination
    Given path apiPath
    And param page = 1
    And param size = 10
    When method GET
    Then status 200
    And match response == 
    """
    {
      data: '#array',
      page: 1,
      size: 10,
      total: '#number'
    }
    """
    And match response.data == '#array'
    And assert response.data.length <= 10
