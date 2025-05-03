# EBazaar E-Commerce Test Automation Summary Report
**Date:** 2025-05-04

## 1. Test Execution Summary
- **Total Tests:** 8
- **Passed:** 6
- **Failed:** 2
- **Duration:** 87.72 seconds
- **Browser:** Chrome
- **Environment:** QA

## 2. Test Cases and Results

### 2.1 Login Functionality
- **Status:** Passed
- **Duration:** 3.106982200057246 seconds
- **Description:** Test login functionality
- **Issues Found:** None

### 2.2 Add to Cart Functionality
- **Status:** Passed
- **Duration:** 4.492376899928786 seconds
- **Description:** Test adding product to cart
- **Issues Found:** None

### 2.3 Complete Order Process
- **Status:** Passed
- **Duration:** 5.425132000003941 seconds
- **Description:** Test complete order process
- **Issues Found:** None

## 3. Test Coverage
- User Authentication
- Product Navigation
- Shopping Cart Operations
- Checkout Process

## 4. Issues and Observations
Failed: test_multiple_products_cart - self = <test_e_commerce.TestECommerce object at 0x000002E14A37ED90>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="57fd144676ecf67d0e5fddf9df369035")>

    @pytest.mark.description("Verify multiple product additions to cart")
    def test_multiple_products_cart(self, driver):
        """Test adding multiple products to cart"""
        login_page = LoginPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
    
        try:
            logging.info("Starting multiple products cart test")
    
            # Login first
            login_page.navigate()
            login_page.login("yousha", "yousha")
            assert login_page.is_login_successful(), "Login failed"
    
            # Add first product
            product_page.navigate_to_product(1, 1)
            product_page.increase_quantity()
            product_page.add_to_cart()
    
            # Add second product
            product_page.navigate_to_product(1, 2)
>           product_page.add_to_cart()

tests\test_e_commerce.py:131: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
pages\product_page.py:23: in add_to_cart
    self.click_element(*self.ADD_TO_CART_BUTTON)
pages\base_page.py:17: in click_element
    element = self.find_clickable_element(by, value)
pages\base_page.py:14: in find_clickable_element
    return self.wait.until(EC.element_to_be_clickable((by, value)))
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.support.wait.WebDriverWait (session="57fd144676ecf67d0e5fddf9df369035")>
method = <function element_to_be_clickable.<locals>._predicate at 0x000002E14A3A4EA0>
message = ''

    def until(self, method: Callable[[D], Union[Literal[False], T]], message: str = "") -> T:
        """Wait until the method returns a value that is not False.
    
        Calls the method provided with the driver as an argument until the
        return value does not evaluate to ``False``.
    
        Parameters:
        -----------
        method: callable(WebDriver)
            - A callable object that takes a WebDriver instance as an argument.
    
        message: str
            - Optional message for :exc:`TimeoutException`
    
        Return:
        -------
        object: T
            - The result of the last call to `method`
    
        Raises:
        -------
        TimeoutException
            - If 'method' does not return a truthy value within the WebDriverWait
            object's timeout
    
        Example:
        --------
        >>> from selenium.webdriver.common.by import By
        >>> from selenium.webdriver.support.ui import WebDriverWait
        >>> from selenium.webdriver.support import expected_conditions as EC
    
        # Wait until an element is visible on the page
        >>> wait = WebDriverWait(driver, 10)
        >>> element = wait.until(EC.visibility_of_element_located((By.ID, "exampleId")))
        >>> print(element.text)
        """
        screen = None
        stacktrace = None
    
        end_time = time.monotonic() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                screen = getattr(exc, "screen", None)
                stacktrace = getattr(exc, "stacktrace", None)
            if time.monotonic() > end_time:
                break
            time.sleep(self._poll)
>       raise TimeoutException(message, screen, stacktrace)
E       selenium.common.exceptions.TimeoutException: Message: 
E       Stacktrace:
E       	GetHandleVerifier [0x00007FF6B382EFA5+77893]
E       	GetHandleVerifier [0x00007FF6B382F000+77984]
E       	(No symbol) [0x00007FF6B35F91BA]
E       	(No symbol) [0x00007FF6B364F16D]
E       	(No symbol) [0x00007FF6B364F41C]
E       	(No symbol) [0x00007FF6B36A2237]
E       	(No symbol) [0x00007FF6B367716F]
E       	(No symbol) [0x00007FF6B369F07F]
E       	(No symbol) [0x00007FF6B3676F03]
E       	(No symbol) [0x00007FF6B3640328]
E       	(No symbol) [0x00007FF6B3641093]
E       	GetHandleVerifier [0x00007FF6B3AE7B6D+2931725]
E       	GetHandleVerifier [0x00007FF6B3AE2132+2908626]
E       	GetHandleVerifier [0x00007FF6B3B000F3+3031443]
E       	GetHandleVerifier [0x00007FF6B38491EA+184970]
E       	GetHandleVerifier [0x00007FF6B385086F+215311]
E       	GetHandleVerifier [0x00007FF6B3836EC4+110436]
E       	GetHandleVerifier [0x00007FF6B3837072+110866]
E       	GetHandleVerifier [0x00007FF6B381D479+5401]
E       	BaseThreadInitThunk [0x00007FF82AEB7374+20]
E       	RtlUserThreadStart [0x00007FF82CD9CC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\support\wait.py:146: TimeoutException
Failed: test_complete_checkout_multiple_products - self = <test_e_commerce.TestECommerce object at 0x000002E14A388210>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="fa553a41b131b924d703bfe5df15a8f0")>

    @pytest.mark.description("Verify complete checkout process with different products")
    def test_complete_checkout_multiple_products(self, driver):
        """Test complete checkout process with multiple products"""
        login_page = LoginPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
    
        try:
            logging.info("Starting complete checkout with multiple products test")
    
            # Login
            login_page.navigate()
            login_page.login("yousha", "yousha")
            assert login_page.is_login_successful(), "Login failed"
    
            # Add multiple products
            product_page.navigate_to_product(1, 1)
            product_page.increase_quantity()
            product_page.add_to_cart()
    
            product_page.navigate_to_product(1, 2)
>           product_page.add_to_cart()

tests\test_e_commerce.py:231: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
pages\product_page.py:23: in add_to_cart
    self.click_element(*self.ADD_TO_CART_BUTTON)
pages\base_page.py:17: in click_element
    element = self.find_clickable_element(by, value)
pages\base_page.py:14: in find_clickable_element
    return self.wait.until(EC.element_to_be_clickable((by, value)))
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.support.wait.WebDriverWait (session="fa553a41b131b924d703bfe5df15a8f0")>
method = <function element_to_be_clickable.<locals>._predicate at 0x000002E14A3FE660>
message = ''

    def until(self, method: Callable[[D], Union[Literal[False], T]], message: str = "") -> T:
        """Wait until the method returns a value that is not False.
    
        Calls the method provided with the driver as an argument until the
        return value does not evaluate to ``False``.
    
        Parameters:
        -----------
        method: callable(WebDriver)
            - A callable object that takes a WebDriver instance as an argument.
    
        message: str
            - Optional message for :exc:`TimeoutException`
    
        Return:
        -------
        object: T
            - The result of the last call to `method`
    
        Raises:
        -------
        TimeoutException
            - If 'method' does not return a truthy value within the WebDriverWait
            object's timeout
    
        Example:
        --------
        >>> from selenium.webdriver.common.by import By
        >>> from selenium.webdriver.support.ui import WebDriverWait
        >>> from selenium.webdriver.support import expected_conditions as EC
    
        # Wait until an element is visible on the page
        >>> wait = WebDriverWait(driver, 10)
        >>> element = wait.until(EC.visibility_of_element_located((By.ID, "exampleId")))
        >>> print(element.text)
        """
        screen = None
        stacktrace = None
    
        end_time = time.monotonic() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                screen = getattr(exc, "screen", None)
                stacktrace = getattr(exc, "stacktrace", None)
            if time.monotonic() > end_time:
                break
            time.sleep(self._poll)
>       raise TimeoutException(message, screen, stacktrace)
E       selenium.common.exceptions.TimeoutException: Message: 
E       Stacktrace:
E       	GetHandleVerifier [0x00007FF6B382EFA5+77893]
E       	GetHandleVerifier [0x00007FF6B382F000+77984]
E       	(No symbol) [0x00007FF6B35F91BA]
E       	(No symbol) [0x00007FF6B364F16D]
E       	(No symbol) [0x00007FF6B364F41C]
E       	(No symbol) [0x00007FF6B36A2237]
E       	(No symbol) [0x00007FF6B367716F]
E       	(No symbol) [0x00007FF6B369F07F]
E       	(No symbol) [0x00007FF6B3676F03]
E       	(No symbol) [0x00007FF6B3640328]
E       	(No symbol) [0x00007FF6B3641093]
E       	GetHandleVerifier [0x00007FF6B3AE7B6D+2931725]
E       	GetHandleVerifier [0x00007FF6B3AE2132+2908626]
E       	GetHandleVerifier [0x00007FF6B3B000F3+3031443]
E       	GetHandleVerifier [0x00007FF6B38491EA+184970]
E       	GetHandleVerifier [0x00007FF6B385086F+215311]
E       	GetHandleVerifier [0x00007FF6B3836EC4+110436]
E       	GetHandleVerifier [0x00007FF6B3837072+110866]
E       	GetHandleVerifier [0x00007FF6B381D479+5401]
E       	BaseThreadInitThunk [0x00007FF82AEB7374+20]
E       	RtlUserThreadStart [0x00007FF82CD9CC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\support\wait.py:146: TimeoutException

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
- Test Logs: `logs/test_execution_20250504_013637.log`
- Failure Screenshots: `screenshots/` (if any)

## 7. Environment Details
- Python Version: 3.11.9
- Selenium Version: 4.18.1
- Operating System: Windows
- Browser: Chrome

## 8. Execution Instructions
