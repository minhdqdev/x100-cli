function fn() {
  // Get the environment from system property, default to 'dev'
  var env = karate.env || 'dev';
  karate.log('karate.env system property was:', env);
  
  // Base configuration for all environments
  var config = {
    env: env,
    // Default timeout for all HTTP calls (in milliseconds)
    defaultTimeout: 30000,
    // Retry configuration
    retryConfig: {
      count: 3,
      interval: 1000
    }
  };

  // Environment-specific configurations
  if (env === 'dev') {
    config.baseUrl = 'http://localhost:8080';
    config.apiUrl = 'http://localhost:8080/api/v1';
    config.debugMode = true;
  } else if (env === 'qa') {
    config.baseUrl = 'https://qa.example.com';
    config.apiUrl = 'https://qa.example.com/api/v1';
    config.debugMode = true;
  } else if (env === 'staging') {
    config.baseUrl = 'https://staging.example.com';
    config.apiUrl = 'https://staging.example.com/api/v1';
    config.debugMode = false;
  } else if (env === 'prod') {
    config.baseUrl = 'https://api.example.com';
    config.apiUrl = 'https://api.example.com/api/v1';
    config.debugMode = false;
  }

  // Common headers
  config.headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  };

  // Authentication configuration (customize based on your auth mechanism)
  config.auth = {
    // Basic Auth example
    basicAuth: {
      username: karate.properties['auth.username'] || 'testuser',
      password: karate.properties['auth.password'] || 'testpass'
    },
    // Bearer Token example (can be set dynamically in tests)
    bearerToken: null,
    // API Key example
    apiKey: karate.properties['auth.apiKey'] || 'test-api-key'
  };

  // Database configuration (if needed)
  config.db = {
    url: karate.properties['db.url'] || 'jdbc:postgresql://localhost:5432/testdb',
    username: karate.properties['db.username'] || 'testuser',
    password: karate.properties['db.password'] || 'testpass'
  };

  // Test data paths
  config.testDataPath = 'classpath:karate/data/';

  // Configure HTTP client
  karate.configure('connectTimeout', config.defaultTimeout);
  karate.configure('readTimeout', config.defaultTimeout);
  karate.configure('ssl', true); // Allow self-signed certificates in non-prod
  
  if (env !== 'prod') {
    karate.configure('ssl', { trustAll: true });
  }

  // Logging configuration
  if (config.debugMode) {
    karate.configure('logPrettyRequest', true);
    karate.configure('logPrettyResponse', true);
  }

  // Custom functions that can be used in all feature files
  config.utils = {
    // Generate random email
    randomEmail: function() {
      return 'test_' + java.lang.System.currentTimeMillis() + '@example.com';
    },
    // Generate random string
    randomString: function(length) {
      var result = '';
      var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
      }
      return result;
    },
    // Generate UUID
    uuid: function() {
      return java.util.UUID.randomUUID().toString();
    },
    // Current timestamp
    timestamp: function() {
      return java.lang.System.currentTimeMillis();
    },
    // Format date
    formatDate: function(format) {
      var sdf = new java.text.SimpleDateFormat(format || 'yyyy-MM-dd');
      return sdf.format(new java.util.Date());
    }
  };

  karate.log('Configuration loaded for environment:', env);
  karate.log('Base URL:', config.baseUrl);
  
  return config;
}
