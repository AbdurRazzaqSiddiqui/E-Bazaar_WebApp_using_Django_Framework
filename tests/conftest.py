import pytest
from datetime import datetime
import os
import json

# Create directories for logs and screenshots if they don't exist
os.makedirs('logs', exist_ok=True)
os.makedirs('screenshots', exist_ok=True)
os.makedirs('reports', exist_ok=True)

# Store test results
test_results = {
    'passed': [],
    'failed': [],
    'total_duration': 0,
    'start_time': None,
    'end_time': None,
    'issues_found': []
}

def pytest_configure(config):
    test_results['start_time'] = datetime.now()
    config._metadata = {
        'Project Name': 'EBazaar E-Commerce',
        'Test Environment': 'QA',
        'Browser': 'Chrome',
        'Platform': 'Windows',
        'Python Version': '3.11.9',
        'Selenium Version': '4.18.1'
    }

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        test_name = item.name
        test_doc = str(item.function.__doc__ or '')
        duration = report.duration
        
        result = {
            'name': test_name,
            'description': test_doc,
            'duration': duration,
            'status': 'passed' if report.passed else 'failed'
        }
        
        if report.passed:
            test_results['passed'].append(result)
        else:
            test_results['failed'].append(result)
            test_results['issues_found'].append(f"Failed: {test_name} - {str(report.longrepr)}")
            try:
                driver = item.funcargs.get('driver')
                if driver:
                    screenshot_path = f"screenshots/{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    driver.save_screenshot(screenshot_path)
                    result['screenshot'] = screenshot_path
            except Exception as e:
                print(f"Failed to capture screenshot: {str(e)}")

def pytest_sessionfinish(session):
    test_results['end_time'] = datetime.now()
    test_results['total_duration'] = (test_results['end_time'] - test_results['start_time']).total_seconds()
    
    # Get individual test results
    login_test = next((test for test in test_results['passed'] + test_results['failed'] 
                      if test['name'] == 'test_login'), None)
    cart_test = next((test for test in test_results['passed'] + test_results['failed']
                     if test['name'] == 'test_add_to_cart'), None)
    checkout_test = next((test for test in test_results['passed'] + test_results['failed']
                        if test['name'] == 'test_complete_order'), None)
    
    report_content = f"""# EBazaar E-Commerce Test Automation Summary Report
**Date:** {datetime.now().strftime("%Y-%m-%d")}

## 1. Test Execution Summary
- **Total Tests:** {len(test_results['passed']) + len(test_results['failed'])}
- **Passed:** {len(test_results['passed'])}
- **Failed:** {len(test_results['failed'])}
- **Duration:** {test_results['total_duration']:.2f} seconds
- **Browser:** Chrome
- **Environment:** QA

## 2. Test Cases and Results

### 2.1 Login Functionality
- **Status:** {'Passed' if login_test and login_test['status'] == 'passed' else 'Failed'}
- **Duration:** {login_test['duration'] if login_test else 'N/A'} seconds
- **Description:** {login_test['description'] if login_test else 'Test user login functionality'}
- **Issues Found:** {next((issue for issue in test_results['issues_found'] if 'test_login' in issue), 'None')}

### 2.2 Add to Cart Functionality
- **Status:** {'Passed' if cart_test and cart_test['status'] == 'passed' else 'Failed'}
- **Duration:** {cart_test['duration'] if cart_test else 'N/A'} seconds
- **Description:** {cart_test['description'] if cart_test else 'Test adding product to cart'}
- **Issues Found:** {next((issue for issue in test_results['issues_found'] if 'test_add_to_cart' in issue), 'None')}

### 2.3 Complete Order Process
- **Status:** {'Passed' if checkout_test and checkout_test['status'] == 'passed' else 'Failed'}
- **Duration:** {checkout_test['duration'] if checkout_test else 'N/A'} seconds
- **Description:** {checkout_test['description'] if checkout_test else 'Test complete order process'}
- **Issues Found:** {next((issue for issue in test_results['issues_found'] if 'test_complete_order' in issue), 'None')}

## 3. Test Coverage
- User Authentication
- Product Navigation
- Shopping Cart Operations
- Checkout Process

## 4. Issues and Observations
{chr(10).join(test_results['issues_found']) if test_results['issues_found'] else "No major issues found during this test execution."}

## 5. Recommendations for Improvement
1. Add more test cases for:
   - Invalid login scenarios
   - Product search functionality
   - Multiple product cart operations
   - Different payment methods

2. Technical Improvements:
   - Implement parallel test execution
   - Add API level tests for better coverage
   - Include performance metrics
   - Add cross-browser testing

3. Test Data Management:
   - Create dedicated test data sets
   - Implement data cleanup after tests
   - Add more edge cases

## 6. Test Artifacts
- Detailed HTML Report: `reports/report.html`
- Test Logs: `logs/test_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log`
- Failure Screenshots: `screenshots/` (if any)

## 7. Environment Details
- Python Version: 3.11.9
- Selenium Version: 4.18.1
- Operating System: Windows
- Browser: Chrome

## 8. Execution Instructions
"""

    # Write report to file
    with open('reports/test_summary_report.md', 'w') as f:
        f.write(report_content)
    
    # Also save raw test results
    with open('reports/test_results.json', 'w') as f:
        json.dump(test_results, f, default=str, indent=4) 