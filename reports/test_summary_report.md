# EBazaar E-Commerce Test Automation Summary Report
**Date:** 2025-05-06

## 1. Test Execution Summary
- **Total Tests:** 52
- **Passed:** 25
- **Failed:** 27
- **Duration:** 424.54 seconds
- **Browser:** Chrome
- **Environment:** QA

## 2. Test Cases and Results

### 2.1 Login Functionality
- **Status:** Passed
- **Duration:** 3.516829600001074 seconds
- **Description:** Test login functionality
- **Issues Found:** Failed: test_login_link_exists - self = <test_e_commerce.TestBasicUI object at 0x0000020CE39D80D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="36e853ec1a94ec0866a0d3c09a129803")>

    def test_login_link_exists(self, driver):
        """Test login link is present"""
        try:
            logging.info("Starting login link test")
            driver.get("http://127.0.0.1:8000/login")
>           login_link = driver.find_element(By.LINK_TEXT, "Login")

tests\test_e_commerce.py:802: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE428C210>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException

### 2.2 Add to Cart Functionality
- **Status:** Passed
- **Duration:** 6.348353400000633 seconds
- **Description:** Test adding product to cart
- **Issues Found:** None

### 2.3 Complete Order Process
- **Status:** Passed
- **Duration:** 8.257800999999745 seconds
- **Description:** Test complete order process
- **Issues Found:** None

## 3. Test Coverage
- User Authentication
- Product Navigation
- Shopping Cart Operations
- Checkout Process

## 4. Issues and Observations
Failed: test_multiple_products_cart - self = <test_e_commerce.TestECommerce object at 0x0000020CE39AD950>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="f49e81c611abb7432e6c26c6fd2398bf")>

    @pytest.mark.description("Verify multiple product additions to cart")
    def test_multiple_products_cart(self, driver):
        """Test adding multiple products to cart"""
        login_page = LoginPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
    
        try:
            logging.info("Starting multiple products cart test")
    
            # Login first
            self.login_user(driver)
    
            # Add first product
            product_page.navigate_to_product(1, 1)
            product_page.increase_quantity()
            product_page.add_to_cart()
    
            # Add second product
            product_page.navigate_to_product(1, 2)
>           product_page.add_to_cart()

tests\test_e_commerce.py:144: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
pages\product_page.py:23: in add_to_cart
    self.click_element(*self.ADD_TO_CART_BUTTON)
pages\base_page.py:17: in click_element
    element = self.find_clickable_element(by, value)
pages\base_page.py:14: in find_clickable_element
    return self.wait.until(EC.element_to_be_clickable((by, value)))
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.support.wait.WebDriverWait (session="f49e81c611abb7432e6c26c6fd2398bf")>
method = <function element_to_be_clickable.<locals>._predicate at 0x0000020CE39C0E00>
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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\support\wait.py:146: TimeoutException
Failed: test_complete_checkout_multiple_products - self = <test_e_commerce.TestECommerce object at 0x0000020CE39AEDD0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="b04e86ec24944b39169930d1599a6e1c")>

    @pytest.mark.description("Verify complete checkout process with different products")
    def test_complete_checkout_multiple_products(self, driver):
        """Test complete checkout process with multiple products"""
        login_page = LoginPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
    
        try:
            logging.info("Starting complete checkout with multiple products test")
    
            # Login first
            self.login_user(driver)
    
            # Add multiple products
            product_page.navigate_to_product(1, 1)
            product_page.increase_quantity()
            product_page.add_to_cart()
    
            product_page.navigate_to_product(1, 2)
>           product_page.add_to_cart()

tests\test_e_commerce.py:233: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
pages\product_page.py:23: in add_to_cart
    self.click_element(*self.ADD_TO_CART_BUTTON)
pages\base_page.py:17: in click_element
    element = self.find_clickable_element(by, value)
pages\base_page.py:14: in find_clickable_element
    return self.wait.until(EC.element_to_be_clickable((by, value)))
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.support.wait.WebDriverWait (session="b04e86ec24944b39169930d1599a6e1c")>
method = <function element_to_be_clickable.<locals>._predicate at 0x0000020CE3DBBBA0>
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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\support\wait.py:146: TimeoutException
Failed: test_register_page_loads - self = <test_e_commerce.TestECommerce object at 0x0000020CE39AFB50>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="de77b5ad024436b8e5b23f1514b52252")>

    @pytest.mark.description("Verify registration page loads correctly")
    def test_register_page_loads(self, driver):
        """Test that registration page loads correctly"""
        driver.get("http://127.0.0.1:8000/register")
>       assert "Register" in driver.title
E       assert 'Register' in 'Home'
E        +  where 'Home' = <selenium.webdriver.chrome.webdriver.WebDriver (session="de77b5ad024436b8e5b23f1514b52252")>.title

tests\test_e_commerce.py:272: AssertionError
Failed: test_navigation_menu - self = <test_e_commerce.TestECommerce object at 0x0000020CE39BD690>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="2871d03dc5ae28646ff2f6bc9c0f242c")>

    @pytest.mark.description("Verify navigation menu elements")
    def test_navigation_menu(self, driver):
        """Test navigation menu elements"""
        driver.get("http://127.0.0.1:8000/categories")
        nav_items = driver.find_elements(By.CLASS_NAME, "main-menu")
>       assert len(nav_items) > 0
E       assert 0 > 0
E        +  where 0 = len([])

tests\test_e_commerce.py:312: AssertionError
Failed: test_product_search - self = <test_e_commerce.TestECommerce object at 0x0000020CE39BDD50>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="abc14dc2db5156ccbfaa2f6267bedf70")>

    @pytest.mark.description("Verify product search functionality")
    def test_product_search(self, driver):
        """Test product search functionality"""
        login_page = LoginPage(driver)
        product_page = ProductPage(driver)
    
        try:
            logging.info("Starting product search test")
    
            # Login first
            self.login_user(driver)
    
            # Perform search
>           product_page.search_product("Test Product")
E           AttributeError: 'ProductPage' object has no attribute 'search_product'

tests\test_e_commerce.py:330: AttributeError
Failed: test_product_filtering - self = <test_e_commerce.TestECommerce object at 0x0000020CE39AF1D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="7585a4fbbd3f3cf49754787e5d8110da")>

    @pytest.mark.description("Verify product filtering options")
    def test_product_filtering(self, driver):
        """Test product filtering options"""
        try:
            logging.info("Starting product filtering test")
    
            # Login first
            self.login_user(driver)
    
            driver.get("http://127.0.0.1:8000/category/1")
            filter_button = driver.find_element(By.CLASS_NAME, "filter-link")
>           filter_button.click()

tests\test_e_commerce.py:351: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webelement.py:119: in click
    self._execute(Command.CLICK_ELEMENT)
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webelement.py:572: in _execute
    return self._parent.execute(command, params)
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE3F97690>
response = {'status': 400, 'value': '{"value":{"error":"element not interactable","message":"element not interactable\\n  (Sessio...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable
E         (Session info: chrome=135.0.7049.115)
E       Stacktrace:
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C8FEC]
E       	(No symbol) [0x00007FF70E620624]
E       	(No symbol) [0x00007FF70E612134]
E       	(No symbol) [0x00007FF70E64712A]
E       	(No symbol) [0x00007FF70E6119E6]
E       	(No symbol) [0x00007FF70E647340]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: ElementNotInteractableException
Failed: test_shopping_cart_empty - self = <test_e_commerce.TestECommerce object at 0x0000020CE39BDA90>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="cb5447dbb9c6c2224ba389924a874db4")>

    @pytest.mark.description("Verify empty shopping cart display")
    def test_shopping_cart_empty(self, driver):
        """Test empty shopping cart display"""
        driver.get("http://127.0.0.1:8000/your-cart")
        cart_items = driver.find_elements(By.CLASS_NAME, "table-shopping-cart")
        assert len(cart_items) == 0
>       assert "Your cart is empty" in driver.page_source
E       assert 'Your cart is empty' in '<html lang="en"><head>\n  <meta http-equiv="content-type" content="text/html; charset=utf-8">\n  <meta name="robots" content="NONE,NOARCHIVE">\n  <title>DoesNotExist\n          at /your-cart</title>\n  <style>\n    html * { padding:0; margin:0; }\n    body * { padding:10px 20px; }\n    body * * { padding:0; }\n    body { font-family: sans-serif; background-color:#fff; color:#000; }\n    body > :where(header, main, footer) { border-bottom:1px solid #ddd; }\n    h1 { font-weight:normal; }\n    h2 { margin-bottom:.8em; }\n    h3 { margin:1em 0 .5em 0; }\n    h4 { margin:0 0 .5em 0; font-weight: normal; }\n    code, pre { font-size: 100%; white-space: pre-wrap; word-break: break-word; }\n    summary { cursor: pointer; }\n    table { border:1px solid #ccc; border-collapse: collapse; width:100%; background:white; }\n    tbody td, tbody th { vertical-align:top; padding:2px 3px; }\n    thead th {\n      padding:1px 6px 1px 3px; background:#fefefe; text-align:left;\n      font-weight:normal; font-size: 0.6875rem; border:1px solid #ddd;\n    }\n    tbody th { width:12em; text-align:right; color:#666; padding-right:.5em; }\n    table.vars { margin:5px 10px 2px 40px; width: auto; }\n    tab...ss="code"><pre>False</pre></td>\n        </tr>\n      \n        <tr>\n          <td>USE_TZ</td>\n          <td class="code"><pre>True</pre></td>\n        </tr>\n      \n        <tr>\n          <td>USE_X_FORWARDED_HOST</td>\n          <td class="code"><pre>False</pre></td>\n        </tr>\n      \n        <tr>\n          <td>USE_X_FORWARDED_PORT</td>\n          <td class="code"><pre>False</pre></td>\n        </tr>\n      \n        <tr>\n          <td>WSGI_APPLICATION</td>\n          <td class="code"><pre>\'ECommerce.wsgi.application\'</pre></td>\n        </tr>\n      \n        <tr>\n          <td>X_FRAME_OPTIONS</td>\n          <td class="code"><pre>\'DENY\'</pre></td>\n        </tr>\n      \n        <tr>\n          <td>YEAR_MONTH_FORMAT</td>\n          <td class="code"><pre>\'F Y\'</pre></td>\n        </tr>\n      \n    </tbody>\n  </table>\n\n</div>\n</main>\n\n\n  <footer id="explanation">\n    <p>\n      You’re seeing this error because you have <code>DEBUG = True</code> in your\n      Django settings file. Change that to <code>False</code>, and Django will\n      display a standard page generated by the handler for this status code.\n    </p>\n  </footer>\n\n\n\n</body></html>'
E        +  where '<html lang="en"><head>\n  <meta http-equiv="content-type" content="text/html; charset=utf-8">\n  <meta name="robots" content="NONE,NOARCHIVE">\n  <title>DoesNotExist\n          at /your-cart</title>\n  <style>\n    html * { padding:0; margin:0; }\n    body * { padding:10px 20px; }\n    body * * { padding:0; }\n    body { font-family: sans-serif; background-color:#fff; color:#000; }\n    body > :where(header, main, footer) { border-bottom:1px solid #ddd; }\n    h1 { font-weight:normal; }\n    h2 { margin-bottom:.8em; }\n    h3 { margin:1em 0 .5em 0; }\n    h4 { margin:0 0 .5em 0; font-weight: normal; }\n    code, pre { font-size: 100%; white-space: pre-wrap; word-break: break-word; }\n    summary { cursor: pointer; }\n    table { border:1px solid #ccc; border-collapse: collapse; width:100%; background:white; }\n    tbody td, tbody th { vertical-align:top; padding:2px 3px; }\n    thead th {\n      padding:1px 6px 1px 3px; background:#fefefe; text-align:left;\n      font-weight:normal; font-size: 0.6875rem; border:1px solid #ddd;\n    }\n    tbody th { width:12em; text-align:right; color:#666; padding-right:.5em; }\n    table.vars { margin:5px 10px 2px 40px; width: auto; }\n    tab...ss="code"><pre>False</pre></td>\n        </tr>\n      \n        <tr>\n          <td>USE_TZ</td>\n          <td class="code"><pre>True</pre></td>\n        </tr>\n      \n        <tr>\n          <td>USE_X_FORWARDED_HOST</td>\n          <td class="code"><pre>False</pre></td>\n        </tr>\n      \n        <tr>\n          <td>USE_X_FORWARDED_PORT</td>\n          <td class="code"><pre>False</pre></td>\n        </tr>\n      \n        <tr>\n          <td>WSGI_APPLICATION</td>\n          <td class="code"><pre>\'ECommerce.wsgi.application\'</pre></td>\n        </tr>\n      \n        <tr>\n          <td>X_FRAME_OPTIONS</td>\n          <td class="code"><pre>\'DENY\'</pre></td>\n        </tr>\n      \n        <tr>\n          <td>YEAR_MONTH_FORMAT</td>\n          <td class="code"><pre>\'F Y\'</pre></td>\n        </tr>\n      \n    </tbody>\n  </table>\n\n</div>\n</main>\n\n\n  <footer id="explanation">\n    <p>\n      You’re seeing this error because you have <code>DEBUG = True</code> in your\n      Django settings file. Change that to <code>False</code>, and Django will\n      display a standard page generated by the handler for this status code.\n    </p>\n  </footer>\n\n\n\n</body></html>' = <selenium.webdriver.chrome.webdriver.WebDriver (session="cb5447dbb9c6c2224ba389924a874db4")>.page_source

tests\test_e_commerce.py:368: AssertionError
Failed: test_product_quick_view - self = <test_e_commerce.TestECommerce object at 0x0000020CE39BE3D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="5eaecc92e8cf8e2f2c0c9d5efc25e321")>

    @pytest.mark.description("Verify product quick view functionality")
    def test_product_quick_view(self, driver):
        """Test product quick view functionality"""
        try:
            logging.info("Starting product quick view test")
    
            # Login first
            self.login_user(driver)
    
            driver.get("http://127.0.0.1:8000/category/1")
            quick_view_button = driver.find_element(By.CLASS_NAME, "js-show-modal-search")
            quick_view_button.click()
>           modal = driver.find_element(By.CLASS_NAME, "wrap-modal1")

tests\test_e_commerce.py:382: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE3EF6390>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".wrap-modal1"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
E       Stacktrace:
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_product_sorting - self = <test_e_commerce.TestECommerce object at 0x0000020CE39BEE50>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="cacc207eed45a771ce5780eca88e7439")>

    @pytest.mark.description("Verify product sorting functionality")
    def test_product_sorting(self, driver):
        """Test product sorting functionality"""
        try:
            logging.info("Starting product sorting test")
    
            # Login first
            self.login_user(driver)
    
            driver.get("http://127.0.0.1:8000/category/1")
            sort_select = driver.find_element(By.CLASS_NAME, "price-high-to-low")
>           sort_select.click()

tests\test_e_commerce.py:445: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webelement.py:119: in click
    self._execute(Command.CLICK_ELEMENT)
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webelement.py:572: in _execute
    return self._parent.execute(command, params)
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE41AEF10>
response = {'status': 400, 'value': '{"value":{"error":"element not interactable","message":"element not interactable\\n  (Sessio...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable
E         (Session info: chrome=135.0.7049.115)
E       Stacktrace:
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C8FEC]
E       	(No symbol) [0x00007FF70E620624]
E       	(No symbol) [0x00007FF70E612134]
E       	(No symbol) [0x00007FF70E64712A]
E       	(No symbol) [0x00007FF70E6119E6]
E       	(No symbol) [0x00007FF70E647340]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: ElementNotInteractableException
Failed: test_category_navigation - self = <test_e_commerce.TestECommerce object at 0x0000020CE39BF1D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="c40eb8e430162467ad1cb2b840baa052")>

    @pytest.mark.description("Verify category navigation")
    def test_category_navigation(self, driver):
        """Test category navigation"""
        login_page = LoginPage(driver)
        product_page = ProductPage(driver)
    
        try:
            logging.info("Starting category navigation test")
    
            # Login first
            self.login_user(driver)
    
            # Navigate through categories
>           product_page.navigate_to_category(1)
E           AttributeError: 'ProductPage' object has no attribute 'navigate_to_category'

tests\test_e_commerce.py:470: AttributeError
Failed: test_add_to_wishlist - self = <test_e_commerce.TestECommerce object at 0x0000020CE39BF710>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="7bfd7ed15f841e75e52ccbb9e2cc6f08")>

    @pytest.mark.description("Verify adding product to wishlist")
    def test_add_to_wishlist(self, driver):
        """Test adding product to wishlist"""
        driver.get("http://127.0.0.1:8000/category/1")
>       wishlist_button = driver.find_element(By.CLASS_NAME, "js-addwish-b2")

tests\test_e_commerce.py:484: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE3F48CD0>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_newsletter_subscription - self = <test_e_commerce.TestECommerce object at 0x0000020CE39BFD10>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="193c3087541232a8dcbd74bf8ca3a2ab")>

    @pytest.mark.description("Verify newsletter subscription form")
    def test_newsletter_subscription(self, driver):
        """Test newsletter subscription form"""
        driver.get("http://127.0.0.1:8000/category/1")
>       email_input = driver.find_element(By.CLASS_NAME, "newsletter-email")

tests\test_e_commerce.py:492: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE11D9010>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_admin_logout - self = <test_e_commerce.TestAdminInterface object at 0x0000020CE39D1710>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="aa0d6c5ff83d50e87bed9e284254d536")>

    @pytest.mark.admin
    def test_admin_logout(self, driver):
        """Test admin logout functionality"""
        try:
            logging.info("Starting admin logout test")
    
            # First login
            self.test_admin_login(driver)
    
            # Find and click logout
>           driver.find_element(By.LINK_TEXT, "LOG OUT").click()

tests\test_e_commerce.py:581: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE2DEF650>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_admin_password_reset_link - self = <test_e_commerce.TestAdminInterface object at 0x0000020CE39D2310>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="3f397567b7d4a0590d7b372c64900109")>

    @pytest.mark.admin
    def test_admin_password_reset_link(self, driver):
        """Test admin password reset link"""
        try:
            logging.info("Starting admin password reset link test")
            driver.get("http://127.0.0.1:8000/admin/")
    
            # Check if password reset link exists
>           reset_link = driver.find_element(By.LINK_TEXT, "Forgotten your password?")

tests\test_e_commerce.py:623: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE3F00310>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_admin_search_box - self = <test_e_commerce.TestAdminInterface object at 0x0000020CE39BEB90>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="fd00f1c42ba9cad40a346845301bd1a9")>

    @pytest.mark.admin
    def test_admin_search_box(self, driver):
        """Test admin search box presence"""
        try:
            logging.info("Starting admin search box test")
    
            # First login
            self.test_admin_login(driver)
    
            # Check if search box exists
>           search_box = driver.find_element(By.NAME, "q")

tests\test_e_commerce.py:690: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE416F5D0>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_login_link_exists - self = <test_e_commerce.TestBasicUI object at 0x0000020CE39D80D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="36e853ec1a94ec0866a0d3c09a129803")>

    def test_login_link_exists(self, driver):
        """Test login link is present"""
        try:
            logging.info("Starting login link test")
            driver.get("http://127.0.0.1:8000/login")
>           login_link = driver.find_element(By.LINK_TEXT, "Login")

tests\test_e_commerce.py:802: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE428C210>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_register_link_exists - self = <test_e_commerce.TestBasicUI object at 0x0000020CE39D85D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="2cd6d5a1a6086c0dd29959bc5ea54010")>

    def test_register_link_exists(self, driver):
        """Test register link is present"""
        try:
            logging.info("Starting register link test")
            driver.get("http://127.0.0.1:8000/register")
>           register_link = driver.find_element(By.LINK_TEXT, "Register")

tests\test_e_commerce.py:815: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE42823D0>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_logo_exists - self = <test_e_commerce.TestBasicUI object at 0x0000020CE39D8C10>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="365af5e398ac95bcd2bc33a7559f21b9")>

    def test_logo_exists(self, driver):
        """Test logo is present"""
        try:
            logging.info("Starting logo test")
            driver.get("http://127.0.0.1:8000/categories")
>           logo = driver.find_element(By.CLASS_NAME, "logo")

tests\test_e_commerce.py:828: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE39A2F50>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_navigation_menu_exists - self = <test_e_commerce.TestBasicUI object at 0x0000020CE39D9250>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="0f4679a91201b0836c3973a6b6880bf2")>

    def test_navigation_menu_exists(self, driver):
        """Test navigation menu is present"""
        try:
            logging.info("Starting navigation menu test")
            driver.get("http://127.0.0.1:8000/categories")
>           nav_menu = driver.find_element(By.TAG_NAME, "nav")

tests\test_e_commerce.py:841: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE3F52790>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_ui_components - self = <test_e_commerce.TestBasicUI object at 0x0000020CE39DA4D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="6713c1cfdcdb0d0c2ff340b49cd12f67")>

    @pytest.mark.description("Verify UI components after login")
    def test_ui_components(self, driver):
        """Test UI components visibility"""
        try:
            logging.info("Starting UI components test")
    
            # Login first
            self.login_user(driver)
    
            # Now verify UI components
            assert driver.find_element(By.CLASS_NAME, "logo").is_displayed(), "Logo not found"
            assert driver.find_element(By.CLASS_NAME, "main-menu").is_displayed(), "Navigation menu not found"
>           assert driver.find_element(By.CLASS_NAME, "search-bar").is_displayed(), "Search bar not found"

tests\test_e_commerce.py:887: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE419BE90>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".search-bar"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
E       Stacktrace:
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_mobile_view - self = <test_e_commerce.TestResponsiveness object at 0x0000020CE39DAC90>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="867da48c942a684dadb49865537c6a04")>

    def test_mobile_view(self, driver):
        """Test mobile view rendering"""
        try:
            logging.info("Starting mobile view test")
            driver.get("http://127.0.0.1:8000/categories")
            # Set viewport to mobile size
            driver.set_window_size(375, 812)  # iPhone X dimensions
    
            # Check if mobile menu is visible
>           mobile_menu = driver.find_element(By.CLASS_NAME, "menu-mobile")

tests\test_e_commerce.py:906: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE4190A50>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_search_bar - self = <test_e_commerce.TestUIComponents object at 0x0000020CE39DB510>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="858a24d6dd9a2ea81038862e07325929")>

    def test_search_bar(self, driver):
        """Test search bar functionality"""
        try:
            logging.info("Starting search bar test")
            driver.get("http://127.0.0.1:8000/categories")
    
            # Find and test search bar
>           search_bar = driver.find_element(By.CLASS_NAME, "search-input")

tests\test_e_commerce.py:922: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE4194250>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_navigation_links - self = <test_e_commerce.TestUIComponents object at 0x0000020CE39DBB50>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="c3bef2b09a75967a430c8aa19f0df1f8")>

    def test_navigation_links(self, driver):
        """Test navigation links"""
        try:
            logging.info("Starting navigation links test")
            driver.get("http://127.0.0.1:8000/categories")
    
            # Test common navigation links
            nav_links = ["menu-item-home", "menu-item-shop", "menu-item-categories"]
            for link_text in nav_links:
>               link = driver.find_element(By.CLASS_NAME, link_text)

tests\test_e_commerce.py:940: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE4220A50>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":".menu-item-home"}
E         (Session info: chrome=135.0.7049.115); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
E       Stacktrace:
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\errorhandler.py:232: NoSuchElementException
Failed: test_social_media_links - self = <test_e_commerce.TestUIComponents object at 0x0000020CE39EC1D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="b84a2da88e8fa860292966fa38a169cb")>

    def test_social_media_links(self, driver):
        """Test social media links in footer"""
        try:
            logging.info("Starting social media links test")
            driver.get("http://127.0.0.1:8000/categories")
    
            footer = driver.find_element(By.TAG_NAME, "footer")
            social_links = footer.find_elements(By.CLASS_NAME, "fa-facebook")
>           assert len(social_links) > 0
E           assert 0 > 0
E            +  where 0 = len([])

tests\test_e_commerce.py:956: AssertionError
Failed: test_login_form_elements - self = <test_e_commerce.TestForms object at 0x0000020CE39D9690>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="ec44ad6bc7a2471c47d08ac50d96bd73")>

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
E            +    where is_displayed = <selenium.webdriver.remote.webelement.WebElement (session="ec44ad6bc7a2471c47d08ac50d96bd73", element="f.3D23CEF688C179A2A7C51E6F4F585B80.d.22A7183BD1523BDDA186F8DF68AA2750.e.1")>.is_displayed

tests\test_e_commerce.py:975: AssertionError
Failed: test_register_form_elements - self = <test_e_commerce.TestForms object at 0x0000020CE39D3510>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="d39abdd022fa547096bb15ecbb8b4212")>

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
E            +    where is_displayed = <selenium.webdriver.remote.webelement.WebElement (session="d39abdd022fa547096bb15ecbb8b4212", element="f.3EB85F249FEE3E470C693C56A23F87F6.d.92765AF64CF7D99A1378340F815D0E9D.e.1")>.is_displayed

tests\test_e_commerce.py:997: AssertionError
Failed: test_hover_effects - self = <test_e_commerce.TestUserInteractions object at 0x0000020CE39EC6D0>
driver = <selenium.webdriver.chrome.webdriver.WebDriver (session="76b1f6c17449b717ff36e53a844f8d20")>

    def test_hover_effects(self, driver):
        """Test hover effects on navigation links"""
        try:
            logging.info("Starting hover effects test")
            driver.get("http://127.0.0.1:8000")
    
            # Test hover on nav links
>           nav_link = driver.find_element(By.LINK_TEXT, "Home")

tests\test_e_commerce.py:1016: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
..\..\..\..\AppData\Roaming\Python\Python311\site-packages\selenium\webdriver\remote\webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x0000020CE4234950>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0E7ED479+5401]\\n\\tBaseThreadInitThunk [0x00007FF81E6C7374+20]\\n\\tRtlUserThreadStart [0x00007FF81FEFCC91+33]\\n"}}'}

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
E       	GetHandleVerifier [0x00007FF70E7FEFA5+77893]
E       	GetHandleVerifier [0x00007FF70E7FF000+77984]
E       	(No symbol) [0x00007FF70E5C91BA]
E       	(No symbol) [0x00007FF70E61F16D]
E       	(No symbol) [0x00007FF70E61F41C]
E       	(No symbol) [0x00007FF70E672237]
E       	(No symbol) [0x00007FF70E64716F]
E       	(No symbol) [0x00007FF70E66F07F]
E       	(No symbol) [0x00007FF70E646F03]
E       	(No symbol) [0x00007FF70E610328]
E       	(No symbol) [0x00007FF70E611093]
E       	GetHandleVerifier [0x00007FF70EAB7B6D+2931725]
E       	GetHandleVerifier [0x00007FF70EAB2132+2908626]
E       	GetHandleVerifier [0x00007FF70EAD00F3+3031443]
E       	GetHandleVerifier [0x00007FF70E8191EA+184970]
E       	GetHandleVerifier [0x00007FF70E82086F+215311]
E       	GetHandleVerifier [0x00007FF70E806EC4+110436]
E       	GetHandleVerifier [0x00007FF70E807072+110866]
E       	GetHandleVerifier [0x00007FF70E7ED479+5401]
E       	BaseThreadInitThunk [0x00007FF81E6C7374+20]
E       	RtlUserThreadStart [0x00007FF81FEFCC91+33]

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
- Test Logs: `logs/test_execution_20250506_010448.log`
- Failure Screenshots: `screenshots/` (if any)

## 7. Environment Details
- Python Version: 3.11.9
- Selenium Version: 4.18.1
- Operating System: Windows
- Browser: Chrome

## 8. Execution Instructions
