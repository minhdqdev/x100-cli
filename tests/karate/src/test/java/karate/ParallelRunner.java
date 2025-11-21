package karate;

import com.intuit.karate.Results;
import com.intuit.karate.Runner;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

/**
 * Parallel Test Runner for Karate tests
 * Executes tests in parallel for faster execution
 * Use with Maven profile: mvn test -Pparallel
 */
class ParallelRunner {

    @Test
    void testParallel() {
        // Get number of threads from system property or use default
        int threads = Integer.parseInt(System.getProperty("karate.threads", "5"));
        
        Results results = Runner.path("classpath:karate/features")
                .outputCucumberJson(true)
                .outputJunitXml(true)
                .reportDir("target/karate-reports")
                .parallel(threads);
        
        generateReport(results.getReportDir());
        
        // Print test summary
        System.out.println("======================================");
        System.out.println("Karate Test Execution Summary");
        System.out.println("======================================");
        System.out.println("Total Features: " + results.getFeaturesTotal());
        System.out.println("Total Scenarios: " + results.getScenariosTotal());
        System.out.println("Passed: " + results.getScenariosTotal() - results.getFailCount());
        System.out.println("Failed: " + results.getFailCount());
        System.out.println("Execution Time: " + results.getElapsedTime() + " ms");
        System.out.println("Threads Used: " + threads);
        System.out.println("======================================");
        
        assertEquals(0, results.getFailCount(), results.getErrorMessages());
    }

    /**
     * Run only smoke tests in parallel
     */
    @Test
    void testSmokeParallel() {
        int threads = Integer.parseInt(System.getProperty("karate.threads", "3"));
        
        Results results = Runner.path("classpath:karate/features")
                .tags("@smoke")
                .outputCucumberJson(true)
                .reportDir("target/karate-reports")
                .parallel(threads);
        
        generateReport(results.getReportDir());
        assertEquals(0, results.getFailCount(), results.getErrorMessages());
    }

    /**
     * Run tests excluding specific tags in parallel
     */
    @Test
    void testExcludingNegative() {
        int threads = Integer.parseInt(System.getProperty("karate.threads", "5"));
        
        Results results = Runner.path("classpath:karate/features")
                .tags("~@negative")
                .outputCucumberJson(true)
                .reportDir("target/karate-reports")
                .parallel(threads);
        
        generateReport(results.getReportDir());
        assertEquals(0, results.getFailCount(), results.getErrorMessages());
    }

    /**
     * Generate HTML report from Cucumber JSON
     */
    public static void generateReport(String karateOutputPath) {
        try {
            String reportDir = System.getProperty("cucumber.report.dir", "target/cucumber-html-reports");
            net.masterthought.cucumber.Configuration config = 
                new net.masterthought.cucumber.Configuration(
                    new java.io.File(reportDir), 
                    "X100 Karate Tests - Parallel Execution"
                );
            
            config.addClassifications("Platform", "API");
            config.addClassifications("Execution Mode", "Parallel");
            config.addClassifications("Environment", System.getProperty("karate.env", "dev"));
            config.addClassifications("Threads", System.getProperty("karate.threads", "5"));
            
            java.util.List<String> jsonFiles = new java.util.ArrayList<>();
            java.io.File reportDir = new java.io.File(karateOutputPath);
            
            if (reportDir.exists() && reportDir.isDirectory()) {
                java.io.File[] files = reportDir.listFiles((dir, name) -> name.endsWith(".json"));
                if (files != null) {
                    for (java.io.File file : files) {
                        jsonFiles.add(file.getAbsolutePath());
                    }
                }
            }
            
            if (!jsonFiles.isEmpty()) {
                net.masterthought.cucumber.ReportBuilder reportBuilder = 
                    new net.masterthought.cucumber.ReportBuilder(jsonFiles, config);
                reportBuilder.generateReports();
                System.out.println("Cucumber HTML report generated at: " + reportDir + "/overview-features.html");
            }
        } catch (Exception e) {
            System.err.println("Error generating Cucumber report: " + e.getMessage());
        }
    }
}
