package karate;

import com.intuit.karate.Results;
import com.intuit.karate.Runner;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

/**
 * Sequential Test Runner for Karate tests
 * Runs all feature files sequentially
 */
class TestRunner {

    @Test
    void testAll() {
        Results results = Runner.path("classpath:karate/features")
                .outputCucumberJson(true)
                .outputJunitXml(true)
                .reportDir("target/karate-reports")
                .parallel(1);
        
        generateReport(results.getReportDir());
        assertEquals(0, results.getFailCount(), results.getErrorMessages());
    }

    @Test
    void testSmoke() {
        Results results = Runner.path("classpath:karate/features")
                .tags("@smoke")
                .outputCucumberJson(true)
                .reportDir("target/karate-reports")
                .parallel(1);
        
        generateReport(results.getReportDir());
        assertEquals(0, results.getFailCount(), results.getErrorMessages());
    }

    @Test
    void testUsers() {
        Results results = Runner.path("classpath:karate/features/users")
                .outputCucumberJson(true)
                .reportDir("target/karate-reports")
                .parallel(1);
        
        generateReport(results.getReportDir());
        assertEquals(0, results.getFailCount(), results.getErrorMessages());
    }

    @Test
    void testAuth() {
        Results results = Runner.path("classpath:karate/features/auth")
                .outputCucumberJson(true)
                .reportDir("target/karate-reports")
                .parallel(1);
        
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
                    "X100 Karate Tests"
                );
            
            config.addClassifications("Platform", "API");
            config.addClassifications("Browser", "N/A");
            config.addClassifications("Environment", System.getProperty("karate.env", "dev"));
            
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
