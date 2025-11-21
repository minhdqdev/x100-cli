Feature: Product Management API Tests
  As an API consumer
  I want to test product management endpoints
  So that I can ensure product operations work correctly

  Background:
    * url baseUrl
    * def productPath = '/api/v1/products'
    * configure headers = headers

  @smoke @products
  Scenario: Get all products
    Given path productPath
    When method GET
    Then status 200
    And match response == '#array'
    And match each response == 
    """
    {
      id: '#number',
      name: '#string',
      price: '#number',
      category: '#string',
      inStock: '#boolean'
    }
    """

  @products @crud
  Scenario: Create a new product
    * def productData = 
    """
    {
      name: 'Test Product',
      description: 'A test product for automation',
      price: 99.99,
      category: 'Electronics',
      sku: '#(utils.randomSku())',
      inStock: true,
      quantity: 100
    }
    """
    Given path productPath
    And request productData
    When method POST
    Then status 201
    And match response.id == '#number'
    And match response.name == productData.name
    And match response.price == productData.price
    * def productId = response.id

  @products @crud
  Scenario: Get product by ID
    # First create a product
    * def productData = { name: 'Test Product', price: 49.99, category: 'Books' }
    Given path productPath
    And request productData
    When method POST
    Then status 201
    * def productId = response.id
    
    # Now get the product
    Given path productPath + '/' + productId
    When method GET
    Then status 200
    And match response == 
    """
    {
      id: '#(productId)',
      name: 'Test Product',
      price: 49.99,
      category: 'Books',
      createdAt: '#string',
      updatedAt: '#string'
    }
    """

  @products @crud
  Scenario: Update product
    # Create product first
    * def productData = { name: 'Original Product', price: 29.99, category: 'Toys' }
    Given path productPath
    And request productData
    When method POST
    Then status 201
    * def productId = response.id
    
    # Update the product
    * def updateData = { name: 'Updated Product', price: 39.99, category: 'Games' }
    Given path productPath + '/' + productId
    And request updateData
    When method PUT
    Then status 200
    And match response.name == 'Updated Product'
    And match response.price == 39.99

  @products @crud
  Scenario: Delete product
    # Create product first
    * def productData = { name: 'To Be Deleted', price: 19.99, category: 'Misc' }
    Given path productPath
    And request productData
    When method POST
    Then status 201
    * def productId = response.id
    
    # Delete the product
    Given path productPath + '/' + productId
    When method DELETE
    Then status 204
    
    # Verify deletion
    Given path productPath + '/' + productId
    When method GET
    Then status 404

  @products @search
  Scenario: Search products by category
    Given path productPath
    And param category = 'Electronics'
    When method GET
    Then status 200
    And match response == '#array'
    And match each response.category == 'Electronics'

  @products @search
  Scenario: Search products by price range
    Given path productPath
    And param minPrice = 10
    And param maxPrice = 50
    When method GET
    Then status 200
    And match response == '#array'
    And match each response.price >= 10
    And match each response.price <= 50

  @products @pagination
  Scenario: Get products with pagination
    Given path productPath
    And param page = 1
    And param size = 20
    And param sort = 'name'
    And param order = 'asc'
    When method GET
    Then status 200
    And match response == 
    """
    {
      data: '#array',
      page: 1,
      size: 20,
      total: '#number',
      totalPages: '#number'
    }
    """

  @products @validation
  Scenario: Create product with invalid data should fail
    * def invalidProduct = { name: '', price: -10 }
    Given path productPath
    And request invalidProduct
    When method POST
    Then status 400
    And match response.errors == '#array'
    And match response.errors contains deep { field: 'name' }
    And match response.errors contains deep { field: 'price' }

  @products @stock
  Scenario: Update product stock
    # Create product first
    * def productData = { name: 'Stock Product', price: 25.00, quantity: 50 }
    Given path productPath
    And request productData
    When method POST
    Then status 201
    * def productId = response.id
    
    # Update stock
    * def stockUpdate = { quantity: 75 }
    Given path productPath + '/' + productId + '/stock'
    And request stockUpdate
    When method PATCH
    Then status 200
    And match response.quantity == 75

  @products @negative
  Scenario: Get non-existent product should return 404
    Given path productPath + '/999999'
    When method GET
    Then status 404
    And match response.error == '#string'

  @products
  Scenario Outline: Create products with different categories
    * def productData = 
    """
    {
      name: '<name>',
      price: <price>,
      category: '<category>'
    }
    """
    Given path productPath
    And request productData
    When method POST
    Then status 201
    And match response.category == '<category>'

    Examples:
      | name          | price | category    |
      | Product A     | 29.99 | Electronics |
      | Product B     | 15.50 | Books       |
      | Product C     | 99.00 | Clothing    |
      | Product D     | 45.75 | Home        |
