# EBazaar E-Commerce Test Automation Summary Report
**Date:** 2025-05-04

## 1. Test Execution Summary
- **Total Tests:** 52
- **Passed:** 23
- **Failed:** 29
- **Duration:** 301.68 seconds
- **Browser:** Chrome
- **Environment:** QA

## 2. Test Cases and Results

### 2.1 Login Functionality
- **Status:** Passed
- **Duration:** 3.1765872000250965 seconds
- **Description:** Test login functionality
- **Issues Found:** Failed: test_login_link_exists - self = <test_e_commerce.TestBasicUI object at 0x000002437E750210>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="d9d9fb18fed739970927027ceb11a583")>

    def test_login_link_exists(self, driver):
        """Test login link is present"""
        try:
            logging.info("Starting login link test")
            driver.get("http://127.0.0.1:8000")
>           login_link = driver.find_element(By.LINK_TEXT, "Login")

tests\test_e_commerce.py:705: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437BFC1890>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"link text","selector":"Login"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException

### 2.2 Add to Cart Functionality
- **Status:** Passed
- **Duration:** 4.861230099922977 seconds
- **Description:** Test adding product to cart
- **Issues Found:** None

### 2.3 Complete Order Process
- **Status:** Passed
- **Duration:** 5.742669699946418 seconds
- **Description:** Test complete order process
- **Issues Found:** None

## 3. Test Coverage
- User Authentication
- Product Navigation
- Shopping Cart Operations
- Checkout Process

## 4. Issues and Observations
Failed: test_multiple_products_cart - self = <test_e_commerce.TestECommerce object at 0x000002437E7313D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="422b156067d50bfa1310bb7483cbe91f")>

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

tests\test_e_commerce.py:138: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
pages\product_page.py:23: in add_to_cart
    self.click_element(*self.ADD_TO_CART_BUTTON)
pages\base_page.py:17: in click_element
    element = self.find_clickable_element(by, value)
pages\base_page.py:14: in find_clickable_element
    return self.wait.until(EC.element_to_be_clickable((by, value)))
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.support.wait.WebDriverWait (session="422b156067d50bfa1310bb7483cbe91f")>
method = <function element_to_be_clickable.<locals>._predicate at 0x000002437E723CE0>
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
Failed: test_complete_checkout_multiple_products - self = <test_e_commerce.TestECommerce object at 0x000002437E730ED0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="ed204211e4cd47690bd3ec68ffc88a53")>

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

tests\test_e_commerce.py:238: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
pages\product_page.py:23: in add_to_cart
    self.click_element(*self.ADD_TO_CART_BUTTON)
pages\base_page.py:17: in click_element
    element = self.find_clickable_element(by, value)
pages\base_page.py:14: in find_clickable_element
    return self.wait.until(EC.element_to_be_clickable((by, value)))
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.support.wait.WebDriverWait (session="ed204211e4cd47690bd3ec68ffc88a53")>
method = <function element_to_be_clickable.<locals>._predicate at 0x000002437E7DD3A0>
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
Failed: test_register_page_loads - self = <test_e_commerce.TestECommerce object at 0x000002437E732A90>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="95b019e43b0c07787d8a3b0c1b9c4855")>

    @pytest.mark.description("Verify registration page loads correctly")
    def test_register_page_loads(self, driver):
        """Test that registration page loads correctly"""
        driver.get("http://127.0.0.1:8000/register")
>       assert "Register" in driver.title
E       assert 'Register' in 'Home'
E        +  where 'Home' = <selenium.webdriver.chrome.webdriver.WebDriver (session="95b019e43b0c07787d8a3b0c1b9c4855")>.title

tests\test_e_commerce.py:277: AssertionError
Failed: test_navigation_menu - self = <test_e_commerce.TestECommerce object at 0x000002437E7441D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="a7cb888a23304aec1f9a41270ab3f291")>

    @pytest.mark.description("Verify navigation menu elements")
    def test_navigation_menu(self, driver):
        """Test navigation menu elements"""
        driver.get("http://127.0.0.1:8000")
        nav_items = driver.find_elements(By.CLASS_NAME, "main-menu")
>       assert len(nav_items) > 0
E       assert 0 > 0
E        +  where 0 = len([])

tests\test_e_commerce.py:317: AssertionError
Failed: test_product_search - self = <test_e_commerce.TestECommerce object at 0x000002437E744890>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="7fe7f52bcce62ded8ffb0c166b24e2bb")>

    @pytest.mark.description("Verify product search functionality")
    def test_product_search(self, driver):
        """Test product search functionality"""
        driver.get("http://127.0.0.1:8000")
>       search_input = driver.find_element(By.CLASS_NAME, "search-input")

tests\test_e_commerce.py:326: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437ECB0110>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".search-input"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_product_filtering - self = <test_e_commerce.TestECommerce object at 0x000002437E744F50>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="62b055561f7a323135f4c6d686824d8a")>

    @pytest.mark.description("Verify product filtering options")
    def test_product_filtering(self, driver):
        """Test product filtering options"""
        driver.get("http://127.0.0.1:8000/product")
>       filter_button = driver.find_element(By.CLASS_NAME, "filter-link")

tests\test_e_commerce.py:335: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437EB4BCD0>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".filter-link"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_shopping_cart_empty - self = <test_e_commerce.TestECommerce object at 0x000002437E745610>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="20f82c69809958d6df3622fedb332c59")>

    @pytest.mark.description("Verify empty shopping cart display")
    def test_shopping_cart_empty(self, driver):
        """Test empty shopping cart display"""
        driver.get("http://127.0.0.1:8000/cart")
        cart_items = driver.find_elements(By.CLASS_NAME, "table-shopping-cart")
        assert len(cart_items) == 0
>       assert "Your cart is empty" in driver.page_source
E       assert 'Your cart is empty' in '<html lang="en"><head>\n  <meta http-equiv="content-type" content="text/html; charset=utf-8">\n  <title>Page not found at /cart</title>\n  <meta name="robots" content="NONE,NOARCHIVE">\n  <style>\n    html * { padding:0; margin:0; }\n    body * { padding:10px 20px; }\n    body * * { padding:0; }\n    body { font-family: sans-serif; background:#eee; color:#000; }\n    body > :where(header, main, footer) { border-bottom:1px solid #ddd; }\n    h1 { font-weight:normal; margin-bottom:.4em; }\n    h1 small { font-size:60%; color:#666; font-weight:normal; }\n    table { border:none; border-collapse: collapse; width:100%; }\n    td, th { vertical-align:top; padding:2px 3px; }\n    th { width:12em; text-align:right; color:#666; padding-right:.5em; }\n    #info { background:#f6f6f6; }\n    #info ol { margin: 0.5em 4em; }\n    #info ol li { font-family: monospace; }\n    #summary { background: #ffc; }\n    #explanation { background:#eee; border-bottom: 0px none; }\n    pre.exception_value { font-family: sans-serif; color: #575757; font-size: 1.5em; margin: 10px 0 10px 0; }\n  </style>\n</head>\n<body>\n  <header id="summary">\n    <h1>Page not found <small>(404)</small></h1>\n    \n    <ta...          </code>\n            \n              <code>\n                register\n                [name=\'register\']\n              </code>\n            \n          </li>\n        \n          <li>\n            \n              <code>\n                \n                \n              </code>\n            \n              <code>\n                your-cart\n                [name=\'view_cart\']\n              </code>\n            \n          </li>\n        \n          <li>\n            \n              <code>\n                \n                \n              </code>\n            \n              <code>\n                add-to-cart/&lt;int:product_id&gt;\n                [name=\'add_to_cart\']\n              </code>\n            \n          </li>\n        \n      </ol>\n      <p>\n        \n          The current path, <code>cart</code>,\n        \n        didn’t match any of these.\n      </p>\n    \n  </main>\n\n  <footer id="explanation">\n    <p>\n      You’re seeing this error because you have <code>DEBUG = True</code> in\n      your Django settings file. Change that to <code>False</code>, and Django\n      will display a standard 404 page.\n    </p>\n  </footer>\n\n\n</body></html>'
E        +  where '<html lang="en"><head>\n  <meta http-equiv="content-type" content="text/html; charset=utf-8">\n  <title>Page not found at /cart</title>\n  <meta name="robots" content="NONE,NOARCHIVE">\n  <style>\n    html * { padding:0; margin:0; }\n    body * { padding:10px 20px; }\n    body * * { padding:0; }\n    body { font-family: sans-serif; background:#eee; color:#000; }\n    body > :where(header, main, footer) { border-bottom:1px solid #ddd; }\n    h1 { font-weight:normal; margin-bottom:.4em; }\n    h1 small { font-size:60%; color:#666; font-weight:normal; }\n    table { border:none; border-collapse: collapse; width:100%; }\n    td, th { vertical-align:top; padding:2px 3px; }\n    th { width:12em; text-align:right; color:#666; padding-right:.5em; }\n    #info { background:#f6f6f6; }\n    #info ol { margin: 0.5em 4em; }\n    #info ol li { font-family: monospace; }\n    #summary { background: #ffc; }\n    #explanation { background:#eee; border-bottom: 0px none; }\n    pre.exception_value { font-family: sans-serif; color: #575757; font-size: 1.5em; margin: 10px 0 10px 0; }\n  </style>\n</head>\n<body>\n  <header id="summary">\n    <h1>Page not found <small>(404)</small></h1>\n    \n    <ta...          </code>\n            \n              <code>\n                register\n                [name=\'register\']\n              </code>\n            \n          </li>\n        \n          <li>\n            \n              <code>\n                \n                \n              </code>\n            \n              <code>\n                your-cart\n                [name=\'view_cart\']\n              </code>\n            \n          </li>\n        \n          <li>\n            \n              <code>\n                \n                \n              </code>\n            \n              <code>\n                add-to-cart/&lt;int:product_id&gt;\n                [name=\'add_to_cart\']\n              </code>\n            \n          </li>\n        \n      </ol>\n      <p>\n        \n          The current path, <code>cart</code>,\n        \n        didn’t match any of these.\n      </p>\n    \n  </main>\n\n  <footer id="explanation">\n    <p>\n      You’re seeing this error because you have <code>DEBUG = True</code> in\n      your Django settings file. Change that to <code>False</code>, and Django\n      will display a standard 404 page.\n    </p>\n  </footer>\n\n\n</body></html>' = <selenium.webdriver.chrome.webdriver.WebDriver (session="20f82c69809958d6df3622fedb332c59")>.page_source

tests\test_e_commerce.py:346: AssertionError
Failed: test_product_quick_view - self = <test_e_commerce.TestECommerce object at 0x000002437E745CD0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="ee42fd6e4fa4b86b48191cffa921f816")>

    @pytest.mark.description("Verify product quick view functionality")
    def test_product_quick_view(self, driver):
        """Test product quick view functionality"""
        driver.get("http://127.0.0.1:8000")
>       quick_view_button = driver.find_element(By.CLASS_NAME, "js-show-modal1")

tests\test_e_commerce.py:352: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437EE51A90>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".js-show-modal1"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_responsive_design - self = <test_e_commerce.TestECommerce object at 0x000002437E746390>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="5634c60098e27534a31095ea5702c52b")>

    @pytest.mark.description("Verify responsive design elements")
    def test_responsive_design(self, driver):
        """Test responsive design elements"""
        driver.get("http://127.0.0.1:8000")
        driver.set_window_size(375, 812) # iPhone X dimensions
>       menu_mobile = driver.find_element(By.CLASS_NAME, "menu-mobile")

tests\test_e_commerce.py:362: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437ECFBB50>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".menu-mobile"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_footer_links - self = <test_e_commerce.TestECommerce object at 0x000002437E746A50>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="ba413df5f4ffe147070e7baaa53db91d")>

    @pytest.mark.description("Verify footer links and social media icons")
    def test_footer_links(self, driver):
        """Test footer links and social media icons"""
        driver.get("http://127.0.0.1:8000")
        footer = driver.find_element(By.TAG_NAME, "footer")
        social_links = footer.find_elements(By.CLASS_NAME, "social")
>       assert len(social_links) > 0
E       assert 0 > 0
E        +  where 0 = len([])

tests\test_e_commerce.py:371: AssertionError
Failed: test_product_sorting - self = <test_e_commerce.TestECommerce object at 0x000002437E747110>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="08aab0d7536e145af1d91b95f8bcfa4b")>

    @pytest.mark.description("Verify product sorting functionality")
    def test_product_sorting(self, driver):
        """Test product sorting functionality"""
        driver.get("http://127.0.0.1:8000/product")
>       sort_select = driver.find_element(By.CLASS_NAME, "select2")

tests\test_e_commerce.py:377: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437ED37090>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".select2"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_category_navigation - self = <test_e_commerce.TestECommerce object at 0x000002437E7477D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="6e2e7f62d4b5eaf9ad521dc314995bb7")>

    @pytest.mark.description("Verify category navigation")
    def test_category_navigation(self, driver):
        """Test category navigation"""
        driver.get("http://127.0.0.1:8000/all_categories")
        categories = driver.find_elements(By.CLASS_NAME, "sec-banner")
>       assert len(categories) > 0
E       assert 0 > 0
E        +  where 0 = len([])

tests\test_e_commerce.py:388: AssertionError
Failed: test_add_to_wishlist - self = <test_e_commerce.TestECommerce object at 0x000002437E747E90>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="5230a87c7e6b9ad4066ba5baaceb7b8b")>

    @pytest.mark.description("Verify adding product to wishlist")
    def test_add_to_wishlist(self, driver):
        """Test adding product to wishlist"""
        driver.get("http://127.0.0.1:8000/product")
>       wishlist_button = driver.find_element(By.CLASS_NAME, "js-addwish-b2")

tests\test_e_commerce.py:396: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437EBC2050>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".js-addwish-b2"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_newsletter_subscription - self = <test_e_commerce.TestECommerce object at 0x000002437E748590>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="41e044ffe5a1faeb4ae8c27f616dc3bf")>

    @pytest.mark.description("Verify newsletter subscription form")
    def test_newsletter_subscription(self, driver):
        """Test newsletter subscription form"""
        driver.get("http://127.0.0.1:8000")
>       email_input = driver.find_element(By.CLASS_NAME, "newsletter-email")

tests\test_e_commerce.py:404: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437EE60950>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".newsletter-email"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_admin_logout - self = <test_e_commerce.TestAdminInterface object at 0x000002437E747C10>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="0a1130a8deaa52ba01af167643b205cd")>

    @pytest.mark.admin
    def test_admin_logout(self, driver):
        """Test admin logout functionality"""
        try:
            logging.info("Starting admin logout test")
    
            # First login
            self.test_admin_login(driver)
    
            # Find and click logout
>           driver.find_element(By.LINK_TEXT, "LOG OUT").click()

tests\test_e_commerce.py:493: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437EBC2390>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"link text","selector":"LOG OUT"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_admin_password_reset_link - self = <test_e_commerce.TestAdminInterface object at 0x000002437E749790>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="c889e78995856899c196cb6b1a54f57f")>

    @pytest.mark.admin
    def test_admin_password_reset_link(self, driver):
        """Test admin password reset link"""
        try:
            logging.info("Starting admin password reset link test")
            driver.get("http://127.0.0.1:8000/admin/")
    
            # Check if password reset link exists
>           reset_link = driver.find_element(By.LINK_TEXT, "Forgotten your password?")

tests\test_e_commerce.py:535: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437EEAFB10>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"link text","selector":"Forgotten your password?"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_admin_search_box - self = <test_e_commerce.TestAdminInterface object at 0x000002437E74A150>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="040217a98f639e0e00fc4faf5e30fec4")>

    @pytest.mark.admin
    def test_admin_search_box(self, driver):
        """Test admin search box presence"""
        try:
            logging.info("Starting admin search box test")
    
            # First login
            self.test_admin_login(driver)
    
            # Check if search box exists
>           search_box = driver.find_element(By.NAME, "q")

tests\test_e_commerce.py:602: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437ED37590>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"[name="q"]"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_home_page_load - self = <test_e_commerce.TestBasicUI object at 0x000002437E74B550>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="4a9af13c74cfa79a10256692b74b9128")>

    def test_home_page_load(self, driver):
        """Test home page loads successfully"""
        try:
            logging.info("Starting home page load test")
            driver.get("http://127.0.0.1:8000")
>           assert "Home" in driver.title
E           assert 'Home' in 'DoesNotExist at /'
E            +  where 'DoesNotExist at /' = <selenium.webdriver.chrome.webdriver.WebDriver (session="4a9af13c74cfa79a10256692b74b9128")>.title

tests\test_e_commerce.py:681: AssertionError
Failed: test_login_link_exists - self = <test_e_commerce.TestBasicUI object at 0x000002437E750210>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="d9d9fb18fed739970927027ceb11a583")>

    def test_login_link_exists(self, driver):
        """Test login link is present"""
        try:
            logging.info("Starting login link test")
            driver.get("http://127.0.0.1:8000")
>           login_link = driver.find_element(By.LINK_TEXT, "Login")

tests\test_e_commerce.py:705: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437BFC1890>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"link text","selector":"Login"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_register_link_exists - self = <test_e_commerce.TestBasicUI object at 0x000002437E750890>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="c30c475dd4ae50735e11e425f103feed")>

    def test_register_link_exists(self, driver):
        """Test register link is present"""
        try:
            logging.info("Starting register link test")
            driver.get("http://127.0.0.1:8000")
>           register_link = driver.find_element(By.LINK_TEXT, "Register")

tests\test_e_commerce.py:718: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437ECA5410>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"link text","selector":"Register"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_logo_exists - self = <test_e_commerce.TestBasicUI object at 0x000002437E750ED0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="38bd59d3f8e4fd6f5e1f6e14e656b1cb")>

    def test_logo_exists(self, driver):
        """Test logo is present"""
        try:
            logging.info("Starting logo test")
            driver.get("http://127.0.0.1:8000")
>           logo = driver.find_element(By.CLASS_NAME, "logo")

tests\test_e_commerce.py:731: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437EB485D0>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".logo"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_navigation_menu_exists - self = <test_e_commerce.TestBasicUI object at 0x000002437E751510>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="43047653c4bbc854c5dd1708b30a7b0f")>

    def test_navigation_menu_exists(self, driver):
        """Test navigation menu is present"""
        try:
            logging.info("Starting navigation menu test")
            driver.get("http://127.0.0.1:8000")
>           nav_menu = driver.find_element(By.TAG_NAME, "nav")

tests\test_e_commerce.py:744: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437EED6510>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"tag name","selector":"nav"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_mobile_view - self = <test_e_commerce.TestResponsiveness object at 0x000002437E752910>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="ab9c520c30e279959310990f8a6c3601")>

    def test_mobile_view(self, driver):
        """Test mobile view rendering"""
        try:
            logging.info("Starting mobile view test")
            driver.get("http://127.0.0.1:8000")
            # Set viewport to mobile size
            driver.set_window_size(375, 812)  # iPhone X dimensions
    
            # Check if mobile menu is visible
>           mobile_menu = driver.find_element(By.CLASS_NAME, "menu-mobile")

tests\test_e_commerce.py:788: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437ED93090>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".menu-mobile"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_search_bar - self = <test_e_commerce.TestUIComponents object at 0x000002437E753790>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="879c492d180a4f98e4b642a9b41ea634")>

    def test_search_bar(self, driver):
        """Test search bar functionality"""
        try:
            logging.info("Starting search bar test")
            driver.get("http://127.0.0.1:8000")
    
            # Find and test search bar
>           search_bar = driver.find_element(By.CLASS_NAME, "search-input")

tests\test_e_commerce.py:820: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437EF0C350>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".search-input"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_navigation_links - self = <test_e_commerce.TestUIComponents object at 0x000002437E753DD0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="40266d39d8e62c6196e65f74058cf0e7")>

    def test_navigation_links(self, driver):
        """Test navigation links"""
        try:
            logging.info("Starting navigation links test")
            driver.get("http://127.0.0.1:8000")
    
            # Test common navigation links
            nav_links = ["Home", "Shop", "Contact"]
            for link_text in nav_links:
>               link = driver.find_element(By.LINK_TEXT, link_text)

tests\test_e_commerce.py:838: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437E7A65D0>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"link text","selector":"Home"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_social_media_links - self = <test_e_commerce.TestUIComponents object at 0x000002437E758450>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="41aa1c27c26b5c602788b6d82a2f41f4")>

    def test_social_media_links(self, driver):
        """Test social media links in footer"""
        try:
            logging.info("Starting social media links test")
            driver.get("http://127.0.0.1:8000")
    
            footer = driver.find_element(By.TAG_NAME, "footer")
            social_links = footer.find_elements(By.CLASS_NAME, "social")
>           assert len(social_links) > 0
E           assert 0 > 0
E            +  where 0 = len([])

tests\test_e_commerce.py:854: AssertionError
Failed: test_login_form_elements - self = <test_e_commerce.TestForms object at 0x000002437E753990>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="601904219193f478f6b1ed2bae3997e7")>

    def test_login_form_elements(self, driver):
        """Test login form elements"""
        try:
            logging.info("Starting login form elements test")
            driver.get("http://127.0.0.1:8000/login")
    
            # Check form elements
            username = driver.find_element(By.NAME, "username")
            password = driver.find_element(By.NAME, "password")
            submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    
>           assert username.is_displayed()
E           assert False
E            +  where False = is_displayed()
E            +    where is_displayed = <selenium.webdriver.remote.webelement.WebElement (session="601904219193f478f6b1ed2bae3997e7", element="f.7F0A587C2E50A44084D5E2314BBA047D.d.70C0B58FBA9BB7612E91353361B41654.e.1")>.is_displayed

tests\test_e_commerce.py:873: AssertionError
Failed: test_register_form_elements - self = <test_e_commerce.TestForms object at 0x000002437E752B10>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="f47dd46379516acfef95a179f7026186")>

    def test_register_form_elements(self, driver):
        """Test registration form elements"""
        try:
            logging.info("Starting register form elements test")
            driver.get("http://127.0.0.1:8000/register")
    
            # Check form elements
            username = driver.find_element(By.NAME, "username")
            email = driver.find_element(By.NAME, "email")
            password = driver.find_element(By.NAME, "password")
            confirmation = driver.find_element(By.NAME, "confirmation")
            submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    
>           assert username.is_displayed()
E           assert False
E            +  where False = is_displayed()
E            +    where is_displayed = <selenium.webdriver.remote.webelement.WebElement (session="f47dd46379516acfef95a179f7026186", element="f.02901E28EDBE4D7FCDB7BDD7E379AB79.d.EC3871817D72CBD7A788E21A9FCEAC0D.e.1")>.is_displayed

tests\test_e_commerce.py:895: AssertionError
Failed: test_hover_effects - self = <test_e_commerce.TestUserInteractions object at 0x000002437E7516D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="1d4444a1e3598579ff4bda6882a3ea4f")>

    def test_hover_effects(self, driver):
        """Test hover effects on navigation links"""
        try:
            logging.info("Starting hover effects test")
            driver.get("http://127.0.0.1:8000")
    
            # Test hover on nav links
>           nav_link = driver.find_element(By.LINK_TEXT, "Home")

tests\test_e_commerce.py:914: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x000002437EDC1410>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...B381D479+5401]\\n\\tBaseThreadInitThunk [0x00007FF82AEB7374+20]\\n\\tRtlUserThreadStart [0x00007FF82CD9CC91+33]\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"link text","selector":"Home"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
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

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException

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
- Test Logs: `logs/test_execution_20250504_024418.log`
- Failure Screenshots: `screenshots/` (if any)

## 7. Environment Details
- Python Version: 3.11.9
- Selenium Version: 4.18.1
- Operating System: Windows
- Browser: Chrome

## 8. Execution Instructions
