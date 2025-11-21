#!/bin/bash

# Karate Test Runner Script
# Provides easy commands to run various test scenarios

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ ${1}${NC}"
}

print_success() {
    echo -e "${GREEN}✓ ${1}${NC}"
}

print_error() {
    echo -e "${RED}✗ ${1}${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ ${1}${NC}"
}

# Function to check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    if ! command -v java &> /dev/null; then
        print_error "Java is not installed. Please install Java 11 or higher."
        exit 1
    fi
    
    if ! command -v mvn &> /dev/null; then
        print_error "Maven is not installed. Please install Maven 3.6 or higher."
        exit 1
    fi
    
    JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}' | awk -F. '{print $1}')
    if [ "$JAVA_VERSION" -lt 11 ]; then
        print_error "Java 11 or higher is required. Current version: $(java -version 2>&1 | head -n 1)"
        exit 1
    fi
    
    print_success "All prerequisites met"
}

# Function to display help
show_help() {
    cat << EOF
${GREEN}Karate Test Runner${NC}

Usage: ./run-tests.sh [COMMAND] [OPTIONS]

${YELLOW}Commands:${NC}
  all              Run all tests sequentially
  parallel         Run all tests in parallel
  smoke            Run smoke tests only
  users            Run user management tests
  auth             Run authentication tests
  tags <tag>       Run tests with specific tag (e.g., @smoke, @regression)
  env <env>        Run tests in specific environment (dev, qa, staging, prod)
  clean            Clean test artifacts
  install          Install dependencies
  report           Open test report in browser
  help             Show this help message

${YELLOW}Options:${NC}
  -e, --env <env>     Environment (dev, qa, staging, prod). Default: dev
  -t, --threads <n>   Number of parallel threads. Default: 5
  -d, --debug         Enable debug logging
  -h, --help          Show this help message

${YELLOW}Examples:${NC}
  ${BLUE}./run-tests.sh all${NC}
      Run all tests sequentially in dev environment

  ${BLUE}./run-tests.sh parallel -e qa -t 8${NC}
      Run all tests in parallel using 8 threads in qa environment

  ${BLUE}./run-tests.sh smoke${NC}
      Run only smoke tests

  ${BLUE}./run-tests.sh tags @users${NC}
      Run tests tagged with @users

  ${BLUE}./run-tests.sh env staging${NC}
      Run all tests in staging environment

  ${BLUE}./run-tests.sh clean${NC}
      Clean all test artifacts

EOF
}

# Function to run tests
run_tests() {
    local test_type=$1
    local env=${KARATE_ENV:-dev}
    local threads=${KARATE_THREADS:-5}
    local debug=${DEBUG:-false}
    
    print_info "Running ${test_type} tests..."
    print_info "Environment: ${env}"
    
    local mvn_cmd="mvn test"
    local extra_args=""
    
    if [ "$debug" = "true" ]; then
        extra_args="$extra_args -X"
    fi
    
    case $test_type in
        all)
            mvn_cmd="$mvn_cmd -Dkarate.env=$env $extra_args"
            ;;
        parallel)
            print_info "Threads: ${threads}"
            mvn_cmd="$mvn_cmd -Pparallel -Dkarate.env=$env -Dkarate.threads=$threads $extra_args"
            ;;
        smoke)
            mvn_cmd="$mvn_cmd -Dtest=TestRunner#testSmoke -Dkarate.env=$env $extra_args"
            ;;
        users)
            mvn_cmd="$mvn_cmd -Dtest=TestRunner#testUsers -Dkarate.env=$env $extra_args"
            ;;
        auth)
            mvn_cmd="$mvn_cmd -Dtest=TestRunner#testAuth -Dkarate.env=$env $extra_args"
            ;;
        *)
            print_error "Unknown test type: $test_type"
            exit 1
            ;;
    esac
    
    print_info "Executing: $mvn_cmd"
    
    if eval $mvn_cmd; then
        print_success "Tests completed successfully!"
        print_info "View reports:"
        print_info "  - Karate: target/karate-reports/karate-summary.html"
        print_info "  - Cucumber: target/cucumber-html-reports/overview-features.html"
    else
        print_error "Tests failed!"
        exit 1
    fi
}

# Function to run tests with specific tag
run_by_tag() {
    local tag=$1
    local env=${KARATE_ENV:-dev}
    
    print_info "Running tests with tag: ${tag}"
    print_info "Environment: ${env}"
    
    if mvn test -Dkarate.options="--tags $tag" -Dkarate.env=$env; then
        print_success "Tests completed successfully!"
    else
        print_error "Tests failed!"
        exit 1
    fi
}

# Function to clean artifacts
clean_artifacts() {
    print_info "Cleaning test artifacts..."
    mvn clean
    print_success "Artifacts cleaned"
}

# Function to install dependencies
install_dependencies() {
    print_info "Installing dependencies..."
    mvn clean install -DskipTests
    print_success "Dependencies installed"
}

# Function to open report
open_report() {
    local report_path="target/cucumber-html-reports/overview-features.html"
    
    if [ ! -f "$report_path" ]; then
        print_warning "Report not found. Run tests first."
        exit 1
    fi
    
    print_info "Opening report..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$report_path"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "$report_path"
    else
        print_warning "Please open manually: $report_path"
    fi
}

# Main script logic
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    check_prerequisites
    
    local command=$1
    shift
    
    # Parse options
    while [[ $# -gt 0 ]]; do
        case $1 in
            -e|--env)
                export KARATE_ENV="$2"
                shift 2
                ;;
            -t|--threads)
                export KARATE_THREADS="$2"
                shift 2
                ;;
            -d|--debug)
                export DEBUG="true"
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                break
                ;;
        esac
    done
    
    case $command in
        all)
            run_tests "all"
            ;;
        parallel)
            run_tests "parallel"
            ;;
        smoke)
            run_tests "smoke"
            ;;
        users)
            run_tests "users"
            ;;
        auth)
            run_tests "auth"
            ;;
        tags)
            if [ $# -eq 0 ]; then
                print_error "Tag parameter required"
                exit 1
            fi
            run_by_tag "$1"
            ;;
        env)
            if [ $# -eq 0 ]; then
                print_error "Environment parameter required"
                exit 1
            fi
            export KARATE_ENV="$1"
            run_tests "all"
            ;;
        clean)
            clean_artifacts
            ;;
        install)
            install_dependencies
            ;;
        report)
            open_report
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
