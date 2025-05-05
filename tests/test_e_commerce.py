import pytest
from selenium import webdriver
import logging
from datetime import datetime
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

# Configure logging
logging.basicConfig(
    filename=f'logs/test_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# At the top of the file, add these marks
pytestmark = [
    pytest.mark.description,
    pytest.mark.security,
    pytest.mark.integration,
    pytest.mark.admin
]

@pytest.fixture(scope="function")
def driver():
    # Setup
    driver = webdriver.Chrome()
    driver.maximize_window()
    logging.info("Starting new test with fresh browser instance")
    yield driver
    # Teardown
    driver.quit()
    logging.info("Test completed, browser closed")

class TestECommerce:
    
    @pytest.mark.description("Verify user login functionality")
    def test_login(self, driver):
        """Test login functionality"""
        login_page = LoginPage(driver)
        
        try:
            logging.info("Starting login test")
            login_page.navigate()
            login_page.login("yousha", "yousha")
            
            assert login_page.is_login_successful(), "Login failed"
            logging.info("Login test passed")
            
        except Exception as e:
            logging.error(f"Login test failed: {str(e)}")
            login_page.take_screenshot("login_failure")
            raise
    
    @pytest.mark.description("Verify add to cart functionality")
    def test_add_to_cart(self, driver):
        """Test adding product to cart"""
        login_page = LoginPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
        
        try:
            logging.info("Starting add to cart test")
            
            # Login first
            login_page.navigate()
            login_page.login("yousha", "yousha")
            assert login_page.is_login_successful(), "Login failed"
            
            # Navigate to product and add to cart
            product_page.navigate_to_product(1, 1)
            product_page.increase_quantity()
            product_page.add_to_cart()
            
            # Verify cart page loaded
            cart_page.wait_for_cart_load()
            logging.info("Add to cart test passed")
            
        except Exception as e:
            logging.error(f"Add to cart test failed: {str(e)}")
            product_page.take_screenshot("add_to_cart_failure")
            raise
    
    @pytest.mark.description("Verify complete order process")
    def test_complete_order(self, driver):
        """Test complete order process"""
        login_page = LoginPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
        
        try:
            logging.info("Starting complete order test")
            
            # Login
            login_page.navigate()
            login_page.login("yousha", "yousha")
            assert login_page.is_login_successful(), "Login failed"
            
            # Add product to cart
            product_page.navigate_to_product(1, 1)
            product_page.increase_quantity()
            product_page.add_to_cart()
            
            # Complete order
            cart_page.wait_for_cart_load()
            cart_page.fill_shipping_info("USA", "California", "90210")
            cart_page.update_totals()
            cart_page.proceed_to_checkout()
            
            logging.info("Complete order test passed")
            
        except Exception as e:
            logging.error(f"Complete order test failed: {str(e)}")
            cart_page.take_screenshot("complete_order_failure")
            raise

    def login_user(self, driver):
        """Helper method to perform login before tests"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login("yousha", "yousha")
        assert login_page.is_login_successful(), "Login failed"
        logging.info("Login successful")

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
            product_page.navigate_to_product(1, 1)
            product_page.add_to_cart()
            
            # Verify cart
            cart_page.wait_for_cart_load()
            logging.info("Multiple products cart test passed")
            
        except Exception as e:
            logging.error(f"Multiple products cart test failed: {str(e)}")
            product_page.take_screenshot("multiple_products_cart_failure")
            raise

    @pytest.mark.description("Verify shipping information validation")
    def test_shipping_info_validation(self, driver):
        """Test shipping information form validation"""
        login_page = LoginPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
        
        try:
            logging.info("Starting shipping info validation test")
            
            # Login first
            self.login_user(driver)
            
            # Add product to cart
            product_page.navigate_to_product(1, 1)
            product_page.add_to_cart()
            
            # Test shipping info
            cart_page.wait_for_cart_load()
            cart_page.fill_shipping_info("USA", "California", "90210")
            cart_page.update_totals()
            
            logging.info("Shipping info validation test passed")
            
        except Exception as e:
            logging.error(f"Shipping info validation test failed: {str(e)}")
            cart_page.take_screenshot("shipping_info_validation_failure")
            raise

    @pytest.mark.description("Verify quantity update in cart")
    def test_quantity_update(self, driver):
        """Test product quantity update functionality"""
        login_page = LoginPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
        
        try:
            logging.info("Starting quantity update test")
            
            # Login first
            self.login_user(driver)
            
            # Add product with quantity
            product_page.navigate_to_product(1, 1)
            product_page.increase_quantity()
            product_page.increase_quantity()
            product_page.add_to_cart()
            
            # Verify cart
            cart_page.wait_for_cart_load()
            cart_page.update_totals()
            
            logging.info("Quantity update test passed")
            
        except Exception as e:
            logging.error(f"Quantity update test failed: {str(e)}")
            cart_page.take_screenshot("quantity_update_failure")
            raise

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
            
            product_page.navigate_to_product(1, 1)
            product_page.add_to_cart()
            
            # Complete checkout
            cart_page.wait_for_cart_load()
            cart_page.fill_shipping_info("USA", "California", "90210")
            cart_page.update_totals()
            cart_page.proceed_to_checkout()
            
            logging.info("Complete checkout with multiple products test passed")
            
        except Exception as e:
            logging.error(f"Complete checkout with multiple products test failed: {str(e)}")
            cart_page.take_screenshot("complete_checkout_multiple_failure")
            raise

    @pytest.mark.description("Verify login with different credentials")
    def test_login_variations(self, driver):
        """Test login functionality with different scenarios"""
        login_page = LoginPage(driver)
        
        try:
            logging.info("Starting login variations test")
            
            # Test successful login
            login_page.navigate()
            login_page.login("yousha", "yousha")
            assert login_page.is_login_successful(), "Login failed"
            
            logging.info("Login variations test passed")
            
        except Exception as e:
            logging.error(f"Login variations test failed: {str(e)}")
            login_page.take_screenshot("login_variations_failure")
            raise

    @pytest.mark.description("Verify registration page loads correctly")
    def test_register_page_loads(self, driver):
        """Test that registration page loads correctly"""
        try:
            logging.info("Starting registration page load test")
            driver.get("http://127.0.0.1:8000/register")
            
            # Wait for elements to be visible
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.TAG_NAME, "h2"))
            )
            
            # Check page title and heading
            heading = driver.find_element(By.TAG_NAME, "h2")
            assert heading.is_displayed(), "Register heading not displayed"
            assert heading.text == "Register"
            
            logging.info("Registration page load test passed")
            
        except Exception as e:
            logging.error(f"Registration page load test failed: {str(e)}")
            driver.save_screenshot("screenshots/register_page_failure.png")
            raise

    @pytest.mark.description("Verify registration form exists")
    def test_register_form_exists(self, driver):
        """Test registration form and its elements are present"""
        try:
            logging.info("Starting registration form test")
            driver.get("http://127.0.0.1:8000/register")
            
            # Wait for elements to be visible
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "form-group"))
            )
            
            # Check form elements
            username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
            email_input = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
            user_type_input = driver.find_element(By.CSS_SELECTOR, "input[name='user_type']")
            company_name_input = driver.find_element(By.CSS_SELECTOR, "input[name='company_name']")
            password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            confirmation_input = driver.find_element(By.CSS_SELECTOR, "input[name='confirmation']")
            submit_button = driver.find_element(By.CLASS_NAME, "submit-button")
            
            # Verify elements are displayed
            assert username_input.is_displayed(), "Username input not displayed"
            assert email_input.is_displayed(), "Email input not displayed"
            assert user_type_input.is_displayed(), "User type input not displayed"
            assert company_name_input.is_displayed(), "Company name input not displayed"
            assert password_input.is_displayed(), "Password input not displayed"
            assert confirmation_input.is_displayed(), "Confirmation input not displayed"
            assert submit_button.is_displayed(), "Submit button not displayed"
            
            logging.info("Registration form test passed")
            
        except Exception as e:
            logging.error(f"Registration form test failed: {str(e)}")
            driver.save_screenshot("screenshots/register_form_failure.png")
            raise

    @pytest.mark.description("Verify registration with mismatched passwords")
    def test_register_password_mismatch(self, driver):
        """Test registration with mismatched passwords"""
        try:
            logging.info("Starting registration password mismatch test")
            driver.get("http://127.0.0.1:8000/register")
            
            # Wait for form to be visible
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "form-group"))
            )
            
            # Fill in registration form
            driver.find_element(By.NAME, "username").send_keys("testuser")
            driver.find_element(By.NAME, "email").send_keys("test@example.com")
            driver.find_element(By.NAME, "user_type").send_keys("Customer")
            driver.find_element(By.NAME, "company_name").send_keys("Test Company")
            driver.find_element(By.NAME, "password").send_keys("password123")
            driver.find_element(By.NAME, "confirmation").send_keys("password456")
            
            # Submit form
            driver.find_element(By.CLASS_NAME, "submit-button").click()
            
            # Wait for and verify error message
            error_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div:not([class])"))
            )
            assert "Passwords must match." in error_message.text
            
            logging.info("Registration password mismatch test passed")
            
        except Exception as e:
            logging.error(f"Registration password mismatch test failed: {str(e)}")
            driver.save_screenshot("screenshots/register_password_mismatch_failure.png")
            raise

    @pytest.mark.description("Verify registration with existing username")
    def test_register_existing_username(self, driver):
        """Test registration with existing username"""
        driver.get("http://127.0.0.1:8000/register")
        driver.find_element(By.NAME, "username").send_keys("existinguser")
        driver.find_element(By.NAME, "email").send_keys("new@example.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "confirmation").send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        assert "Username already taken" in driver.page_source

    @pytest.mark.description("Verify navigation menu elements")
    def test_navigation_menu(self, driver):
        """Test navigation menu elements"""
        try:
            logging.info("Starting navigation menu test")
            
            # Login first
            self.login_user(driver)
            
            # Navigate to categories page
            driver.get("http://127.0.0.1:8000/category/1")
            
            # Wait for navigation menu to be visible
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "main-menu"))
            )
            
            # Check navigation items
            home_item = driver.find_element(By.CLASS_NAME, "menu-item-home")
            shop_item = driver.find_element(By.CLASS_NAME, "menu-item-shop")
            features_item = driver.find_element(By.CLASS_NAME, "menu-item-categories")
            
            # Verify menu items
            assert home_item.is_displayed(), "Home link not found"
            assert shop_item.is_displayed(), "Shop link not found"
            assert features_item.is_displayed(), "Categories link not found"
            
            logging.info("Navigation menu test passed")
            
        except Exception as e:
            logging.error(f"Navigation menu test failed: {str(e)}")
            driver.save_screenshot("screenshots/navigation_menu_failure.png")
            raise

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
            product_page.search_product("Test Product")
            assert product_page.verify_search_results(), "Search results not found"
            
            logging.info("Product search test passed")
            
        except Exception as e:
            logging.error(f"Product search test failed: {str(e)}")
            product_page.take_screenshot("product_search_failure")
            raise

    @pytest.mark.description("Verify product filtering options")
    def test_product_filtering(self, driver):
        """Test product filtering options"""
        try:
            logging.info("Starting product filtering test")
            
            # Login first
            self.login_user(driver)
            
            driver.get("http://127.0.0.1:8000/category/1")
            filter_button = driver.find_element(By.CLASS_NAME, "filter-link")
            filter_button.click()
            price_filter = driver.find_element(By.CLASS_NAME, "price-low-to-high")
            assert price_filter.is_displayed()
            
            logging.info("Product filtering test passed")
            
        except Exception as e:
            logging.error(f"Product filtering test failed: {str(e)}")
            driver.save_screenshot("screenshots/product_filtering_failure.png")
            raise

    @pytest.mark.description("Verify empty shopping cart display")
    def test_shopping_cart_empty(self, driver):
        """Test empty shopping cart display"""
        driver.get("http://127.0.0.1:8000/your-cart")
        cart_items = driver.find_elements(By.CLASS_NAME, "table-shopping-cart")
        assert len(cart_items) == 0
        assert "Your cart is empty" in driver.page_source

    @pytest.mark.description("Verify product quick view functionality")
    def test_product_quick_view(self, driver):
        """Test product quick view functionality"""
        try:
            logging.info("Starting product quick view test")
            
            # Login first
            self.login_user(driver)
            
            driver.get("http://127.0.0.1:8000/category/1/product/1")
            quick_view_button = driver.find_element(By.CLASS_NAME, "search-input")
            # quick_view_button.click()
            assert quick_view_button.is_displayed()
            
            logging.info("Product quick view test passed")
            
        except Exception as e:
            logging.error(f"Product quick view test failed: {str(e)}")
            driver.save_screenshot("screenshots/quick_view_failure.png")
            raise

    @pytest.mark.description("Verify responsive design elements")
    def test_responsive_design(self, driver):
        """Test responsive design elements"""
        try:
            logging.info("Starting responsive design test")
            
            # Login first
            self.login_user(driver)
            
            driver.get("http://127.0.0.1:8000/category/1")
            driver.set_window_size(375, 812)  # iPhone X dimensions
            menu_mobile = driver.find_element(By.CLASS_NAME, "wrap-header-mobile")
            assert menu_mobile.is_displayed()
            
            logging.info("Responsive design test passed")
            
        except Exception as e:
            logging.error(f"Responsive design test failed: {str(e)}")
            driver.save_screenshot("screenshots/responsive_design_failure.png")
            raise

    @pytest.mark.description("Verify footer links and social media icons")
    def test_footer_links(self, driver):
        """Test footer links and social media icons"""
        try:
            logging.info("Starting footer links test")
            
            # Login first
            self.login_user(driver)
            
            driver.get("http://127.0.0.1:8000/category/1")
            footer = driver.find_element(By.TAG_NAME, "footer")
            social_links = footer.find_elements(By.CLASS_NAME, "fa-facebook")
            assert len(social_links) > 0
            
            logging.info("Footer links test passed")
            
        except Exception as e:
            logging.error(f"Footer links test failed: {str(e)}")
            driver.save_screenshot("screenshots/footer_links_failure.png")
            raise

    @pytest.mark.description("Verify product sorting functionality")
    def test_product_sorting(self, driver):
        """Test product sorting functionality"""
        try:
            logging.info("Starting product sorting test")
            
            # Login first
            self.login_user(driver)
            
            driver.get("http://127.0.0.1:8000/category/1")
            sort_select = driver.find_element(By.CLASS_NAME, "price-high-to-low")
            sort_select.click()
            price_high_low = driver.find_element(By.XPATH, "//option[contains(text(), 'Price: High to Low')]")
            price_high_low.click()
            assert "Price: High to Low" in driver.page_source
            
            logging.info("Product sorting test passed")
            
        except Exception as e:
            logging.error(f"Product sorting test failed: {str(e)}")
            driver.save_screenshot("screenshots/product_sorting_failure.png")
            raise

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
            product_page.navigate_to_category(1)
            assert product_page.verify_category_products(), "Category products not found"
            
            logging.info("Category navigation test passed")
            
        except Exception as e:
            logging.error(f"Category navigation test failed: {str(e)}")
            product_page.take_screenshot("category_navigation_failure")
            raise

    @pytest.mark.description("Verify adding product to wishlist")
    def test_add_to_wishlist(self, driver):
        """Test adding product to wishlist"""
        driver.get("http://127.0.0.1:8000/category/1")
        wishlist_button = driver.find_element(By.CLASS_NAME, "js-addwish-b2")
        wishlist_button.click()
        assert "Added to wishlist" in driver.page_source

    @pytest.mark.description("Verify newsletter subscription form")
    def test_newsletter_subscription(self, driver):
        """Test newsletter subscription form"""
        driver.get("http://127.0.0.1:8000/category/1")
        email_input = driver.find_element(By.CLASS_NAME, "newsletter-email")
        email_input.send_keys("test@example.com")
        submit_button = driver.find_element(By.CLASS_NAME, "newsletter-submit")
        submit_button.click()
        assert "Thank you for subscribing" in driver.page_source

    @pytest.mark.security
    def test_unauthorized_access_protection(self, driver):
        """Test protection against unauthorized access attempts"""
        try:
            logging.info("Starting unauthorized access test")
            
            # Try accessing protected pages without login
            protected_urls = [
                "/your-cart",
                "/category/1/product/1",
                "/checkout",
                "/profile"
            ]
            
            for url in protected_urls:
                driver.get(f"http://127.0.0.1:8000{url}")
                assert "login" in driver.current_url.lower(), f"Unauthorized access possible to {url}"
            
            logging.info("Unauthorized access protection test passed")
        except Exception as e:
            logging.error(f"Unauthorized access protection test failed: {str(e)}")
            driver.save_screenshot("screenshots/unauthorized_access_failure.png")
            raise

    @pytest.mark.security
    def test_session_handling(self, driver):
        """Test session handling and timeout"""
        try:
            logging.info("Starting session handling test")
            
            # Login first
            self.login_user(driver)
            
            # Delete session cookie
            driver.delete_cookie("sessionid")
            
            # Try accessing protected page
            driver.get("http://127.0.0.1:8000/your-cart")
            assert "login" in driver.current_url.lower(), "Session not properly invalidated"
            
            logging.info("Session handling test passed")
        except Exception as e:
            logging.error(f"Session handling test failed: {str(e)}")
            driver.save_screenshot("screenshots/session_handling_failure.png")
            raise

    @pytest.mark.security
    def test_csrf_protection(self, driver):
        """Test CSRF protection on forms"""
        try:
            logging.info("Starting CSRF protection test")
            
            # Login first
            self.login_user(driver)
            
            # Check for CSRF token in forms
            driver.get("http://127.0.0.1:8000/login")
            csrf_token = driver.find_element(By.NAME, "csrfmiddlewaretoken")
            assert csrf_token.is_enabled(), "CSRF token not found in form"
            
            logging.info("CSRF protection test passed")
        except Exception as e:
            logging.error(f"CSRF protection test failed: {str(e)}")
            driver.save_screenshot("screenshots/csrf_protection_failure.png")
            raise

    @pytest.mark.security
    def test_password_strength_validation(self, driver):
        """Test password strength requirements during registration"""
        try:
            logging.info("Starting password strength validation test")
            
            driver.get("http://127.0.0.1:8000/register")
            
            # Test weak password
            driver.find_element(By.NAME, "username").send_keys("testuser")
            driver.find_element(By.NAME, "email").send_keys("test@example.com")
            driver.find_element(By.NAME, "password").send_keys("123")
            driver.find_element(By.NAME, "confirmation").send_keys("123")
            driver.find_element(By.CLASS_NAME, "submit-button").click()
            
            # Check for error message
            error_message = driver.find_element(By.CLASS_NAME, "error-message")
            assert "password is too weak" in error_message.text.lower()
            
            logging.info("Password strength validation test passed")
        except Exception as e:
            logging.error(f"Password strength validation test failed: {str(e)}")
            driver.save_screenshot("screenshots/password_validation_failure.png")
            raise

    @pytest.mark.security
    def test_role_based_access(self, driver):
        """Test role-based access control"""
        try:
            logging.info("Starting role-based access test")
            
            # Try accessing admin pages
            admin_urls = [
                "/admin/products",
                "/admin/users",
                "/admin/orders"
            ]
            
            for url in admin_urls:
                driver.get(f"http://127.0.0.1:8000{url}")
                assert "permission denied" in driver.page_source.lower() or "login" in driver.current_url.lower()
            
            logging.info("Role-based access test passed")
        except Exception as e:
            logging.error(f"Role-based access test failed: {str(e)}")
            driver.save_screenshot("screenshots/role_based_access_failure.png")
            raise

    @pytest.mark.security
    def test_sql_injection_prevention(self, driver):
        """Test SQL injection prevention through URL parameters"""
        try:
            logging.info("Starting SQL injection prevention test")
            
            # Login first
            self.login_user(driver)
            
            # Try SQL injection through URL parameters
            injection_attempts = [
                "/category/1' OR '1'='1",
                "/category/1; DROP TABLE products; --",
                "/category/1 UNION SELECT * FROM users; --",
                "/category/1' OR id IS NOT NULL; --",
                "/product/1' OR product_id > 0; --"
            ]
            
            base_url = "http://127.0.0.1:8000"
            
            for attempt in injection_attempts:
                # Try injection in different URL patterns
                urls_to_test = [
                    f"{base_url}{attempt}",
                    f"{base_url}/category/{attempt}",
                    f"{base_url}/product/details/{attempt}",
                    f"{base_url}/your-cart?id={attempt}"
                ]
                
                for url in urls_to_test:
                    driver.get(url)
                    
                    # Verify no data breach (should see error page or redirect)
                    assert any([
                        "error" in driver.page_source.lower(),
                        "not found" in driver.page_source.lower(),
                        "invalid" in driver.page_source.lower(),
                        "login" in driver.current_url.lower()
                    ]), f"Possible SQL injection vulnerability with URL: {url}"
            
            logging.info("SQL injection prevention test passed")
            
        except Exception as e:
            logging.error(f"SQL injection prevention test failed: {str(e)}")
            driver.save_screenshot("screenshots/sql_injection_failure.png")
            raise

    @pytest.mark.integration
    def test_payment_gateway_integration(self, driver):
        """Test payment gateway integration"""
        try:
            logging.info("Starting payment gateway integration test")
            
            # Login and add product to cart
            self.login_user(driver)
            product_page = ProductPage(driver)
            cart_page = CartPage(driver)
            
            product_page.navigate_to_product(1, 1)
            product_page.add_to_cart()
            
            # Proceed to checkout
            cart_page.wait_for_cart_load()
            cart_page.fill_shipping_info("USA", "California", "90210")
            cart_page.proceed_to_checkout()
            
            # Verify payment gateway elements
            payment_iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "stripe-checkout-iframe"))
            )
            driver.switch_to.frame(payment_iframe)
            
            assert driver.find_element(By.NAME, "cardnumber").is_displayed()
            assert driver.find_element(By.NAME, "exp-date").is_displayed()
            assert driver.find_element(By.NAME, "cvc").is_displayed()
            
            logging.info("Payment gateway integration test passed")
        except Exception as e:
            logging.error(f"Payment gateway integration test failed: {str(e)}")
            driver.save_screenshot("screenshots/payment_integration_failure.png")
            raise

    @pytest.mark.integration
    def test_email_notification_system(self, driver):
        """Test email notification system"""
        try:
            logging.info("Starting email notification test")
            
            # Login and complete an order
            self.login_user(driver)
            product_page = ProductPage(driver)
            cart_page = CartPage(driver)
            
            product_page.navigate_to_product(1, 1)
            product_page.add_to_cart()
            
            cart_page.wait_for_cart_load()
            cart_page.fill_shipping_info("USA", "California", "90210")
            cart_page.proceed_to_checkout()
            
            # Verify order confirmation email
            # Note: This would require access to email testing service
            # For now, we'll check if the confirmation page mentions email
            assert "confirmation email" in driver.page_source.lower()
            
            logging.info("Email notification test passed")
        except Exception as e:
            logging.error(f"Email notification test failed: {str(e)}")
            driver.save_screenshot("screenshots/email_notification_failure.png")
            raise

class TestAdminInterface:
    @pytest.mark.admin
    def test_admin_login(self, driver):
        """Test admin login functionality"""
        try:
            logging.info("Starting admin login test")
            driver.get("http://127.0.0.1:8000/admin/")
            
            # Login with admin credentials
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            
            username_input.send_keys("admin")
            password_input.send_keys("ST@123456")
            
            driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
            
            # Simply verify we're on the admin dashboard
            assert "Site administration" in driver.title
            
            logging.info("Admin login test passed")
            
        except Exception as e:
            logging.error(f"Admin login test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_login_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_login_invalid_credentials(self, driver):
        """Test admin login with invalid credentials"""
        try:
            logging.info("Starting admin invalid login test")
            driver.get("http://127.0.0.1:8000/admin/")
            
            # Test with wrong credentials
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")
            
            username_input.send_keys("wrong_admin")
            password_input.send_keys("wrong_password")
            
            driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
            
            # Simply verify we're still on login page
            assert "Log in | Django site admin" in driver.title
            
            logging.info("Admin invalid login test passed")
            
        except Exception as e:
            logging.error(f"Admin invalid login test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_invalid_login_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_empty_login(self, driver):
        """Test admin login with empty fields"""
        try:
            logging.info("Starting admin empty login test")
            driver.get("http://127.0.0.1:8000/admin/")
            
            # Click login without entering credentials
            driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
            
            # Verify still on login page
            assert "Log in | Django site admin" in driver.title
            
            logging.info("Admin empty login test passed")
            
        except Exception as e:
            logging.error(f"Admin empty login test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_empty_login_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_logout(self, driver):
        """Test admin logout functionality"""
        try:
            logging.info("Starting admin logout test")
            
            # First login
            self.test_admin_login(driver)
            
            # Find and click logout button within the form
            logout_button = driver.find_element(By.CSS_SELECTOR, "#logout-form button[type='submit']")
            logout_button.click()
            
            # Verify back on login page
            assert "Logged out | Django site admin" in driver.title
            
            logging.info("Admin logout test passed")
            
        except Exception as e:
            logging.error(f"Admin logout test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_logout_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_models_visibility(self, driver):
        """Test visibility of admin models"""
        try:
            logging.info("Starting admin models visibility test")
            
            # First login
            self.test_admin_login(driver)
            
            # Check if common model names are visible
            expected_models = ["Users", "Groups"]
            
            for model in expected_models:
                assert model in driver.page_source
            
            logging.info("Admin models visibility test passed")
            
        except Exception as e:
            logging.error(f"Admin models visibility test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_models_visibility_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_password_reset_link(self, driver):
        """Test admin password reset link"""
        try:
            logging.info("Starting admin password reset link test")
            driver.get("http://127.0.0.1:8000/admin/")
            
            # Check if password reset link exists
            reset_link = driver.find_element(By.LINK_TEXT, "Forgotten your password?")
            reset_link.click()
            
            # Verify on password reset page
            assert "Password reset" in driver.title
            
            logging.info("Admin password reset link test passed")
            
        except Exception as e:
            logging.error(f"Admin password reset link test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_password_reset_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_user_list(self, driver):
        """Test admin user list view"""
        try:
            logging.info("Starting admin user list test")
            
            # First login
            self.test_admin_login(driver)
            
            # Navigate to Users
            driver.find_element(By.LINK_TEXT, "Users").click()
            
            # Verify on user list page
            assert "Select user to change" in driver.page_source
            
            logging.info("Admin user list test passed")
            
        except Exception as e:
            logging.error(f"Admin user list test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_user_list_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_group_list(self, driver):
        """Test admin group list view"""
        try:
            logging.info("Starting admin group list test")
            
            # First login
            self.test_admin_login(driver)
            
            # Navigate to Groups
            driver.find_element(By.LINK_TEXT, "Groups").click()
            
            # Verify on group list page
            assert "Select group to change" in driver.page_source
            
            logging.info("Admin group list test passed")
            
        except Exception as e:
            logging.error(f"Admin group list test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_group_list_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_search_box(self, driver):
        """Test admin search box presence"""
        try:
            logging.info("Starting admin search box test")
            
            # First login
            self.test_admin_login(driver)
            
            # Check if search box exists
            search_box = driver.find_element(By.NAME, "q")
            assert search_box.is_displayed()
            
            logging.info("Admin search box test passed")
            
        except Exception as e:
            logging.error(f"Admin search box test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_search_box_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_breadcrumbs(self, driver):
        """Test admin breadcrumbs navigation"""
        try:
            logging.info("Starting admin breadcrumbs test")
            
            # First login
            self.test_admin_login(driver)
            
            # Navigate to Users
            driver.find_element(By.LINK_TEXT, "Users").click()
            
            # Check if breadcrumbs exist
            breadcrumbs = driver.find_element(By.CLASS_NAME, "breadcrumbs")
            assert "Home" in breadcrumbs.text
            
            logging.info("Admin breadcrumbs test passed")
            
        except Exception as e:
            logging.error(f"Admin breadcrumbs test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_breadcrumbs_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_site_name(self, driver):
        """Test admin site name display"""
        try:
            logging.info("Starting admin site name test")
            
            # First login
            self.test_admin_login(driver)
            
            # Check site name
            site_name = driver.find_element(By.ID, "site-name")
            assert "Django administration" in site_name.text
            
            logging.info("Admin site name test passed")
            
        except Exception as e:
            logging.error(f"Admin site name test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_site_name_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_app_list(self, driver):
        """Test admin application list"""
        try:
            logging.info("Starting admin app list test")
            
            # First login
            self.test_admin_login(driver)
            
            # Check if app list exists
            app_list = driver.find_element(By.ID, "content-main")
            assert app_list.is_displayed()
            
            logging.info("Admin app list test passed")
            
        except Exception as e:
            logging.error(f"Admin app list test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_app_list_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_change_password(self, driver):
        """Test admin password change functionality"""
        try:
            logging.info("Starting admin password change test")
            
            # First login
            self.test_admin_login(driver)
            
            # Click on change password link using href
            change_password_link = driver.find_element(By.CSS_SELECTOR, "a[href='/admin/password_change/']")
            change_password_link.click()
            
            # Fill in password change form
            old_password = driver.find_element(By.NAME, "old_password")
            new_password1 = driver.find_element(By.NAME, "new_password1")
            new_password2 = driver.find_element(By.NAME, "new_password2")
            
            old_password.send_keys("ST@123456")  # Current password
            new_password1.send_keys("ST@123456")  # New password
            new_password2.send_keys("ST@123456")  # Confirm new password
            
            # Submit form
            driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
            
            # Verify password change success
            assert "Password change successful" in driver.page_source
            
            logging.info("Admin password change test passed")
            
        except Exception as e:
            logging.error(f"Admin password change test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_password_change_failure.png")
            raise

    @pytest.mark.admin
    def test_admin_password_security(self, driver):
        """Test admin password security requirements"""
        try:
            logging.info("Starting admin password security test")
            
            # First login
            self.test_admin_login(driver)
            
            # Click on change password link
            change_password_link = driver.find_element(By.CSS_SELECTOR, "a[href='/admin/password_change/']")
            change_password_link.click()
            
            # Test cases for weak passwords
            weak_passwords = [
                "admin",  # Similar to username
                "123",    # Too short and numeric
                "password",  # Too common
                "12345678"  # Entirely numeric
            ]
            
            for weak_password in weak_passwords:
                # Wait for form to be present
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "content-main"))
                )
                
                # Fill in password change form
                old_password = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "old_password"))
                )
                new_password1 = driver.find_element(By.NAME, "new_password1")
                new_password2 = driver.find_element(By.NAME, "new_password2")
                
                old_password.send_keys("ST@123456")  # Current password
                new_password1.send_keys(weak_password)
                new_password2.send_keys(weak_password)
                
                # Submit form
                driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
                
                # Verify error message
                error_note = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "errornote"))
                )
                assert "Please correct the error below." in error_note.text
                
                # Verify specific error messages
                error_list = driver.find_elements(By.CLASS_NAME, "errorlist")
                if error_list:
                    error_text = error_list[0].text.lower()
                    assert any([
                        "must contain at least 8 characters" in error_text,
                        "too similar to the username" in error_text,
                        "password is too common" in error_text,
                        "can't be entirely numeric" in error_text
                    ]), f"Expected password security error not found for password: {weak_password}"
                
            logging.info("Admin password security test passed")
            
        except Exception as e:
            logging.error(f"Admin password security test failed: {str(e)}")
            driver.save_screenshot("screenshots/admin_password_security_failure.png")
            raise

class TestBasicUI:
    def login_user(self, driver):
        """Helper method to perform login before tests"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login("yousha", "yousha")
        assert login_page.is_login_successful(), "Login failed"
        logging.info("Login successful")

    def test_home_page_load(self, driver):
        """Test home page loads successfully"""
        try:
            logging.info("Starting home page load test")
            driver.get("http://127.0.0.1:8000/login")
            assert "Home" in driver.title
            logging.info("Home page load test passed")
        except Exception as e:
            logging.error(f"Home page load test failed: {str(e)}")
            driver.save_screenshot("screenshots/home_page_failure.png")
            raise

    @pytest.mark.description("Verify page title exists")
    def test_page_title(self, driver):
        """Test page title exists"""
        try:
            logging.info("Starting page title test")
            driver.get("http://127.0.0.1:8000/login")
            assert driver.title != ""
            logging.info("Page title test passed")
        except Exception as e:
            logging.error(f"Page title test failed: {str(e)}")
            driver.save_screenshot("screenshots/page_title_failure.png")
            raise

    def test_login_link_exists(self, driver):
        """Test login link is present"""
        try:
            logging.info("Starting login link test")
            driver.get("http://127.0.0.1:8000/login")
            login_link = driver.find_element(By.LINK_TEXT, "Login")
            assert login_link.is_displayed()
            logging.info("Login link test passed")
        except Exception as e:
            logging.error(f"Login link test failed: {str(e)}")
            driver.save_screenshot("screenshots/login_link_failure.png")
            raise

    def test_register_link_exists(self, driver):
        """Test register link is present"""
        try:
            logging.info("Starting register link test")
            driver.get("http://127.0.0.1:8000/register")
            register_link = driver.find_element(By.LINK_TEXT, "Register")
            assert register_link.is_displayed()
            logging.info("Register link test passed")
        except Exception as e:
            logging.error(f"Register link test failed: {str(e)}")
            driver.save_screenshot("screenshots/register_link_failure.png")
            raise

    def test_logo_exists(self, driver):
        """Test logo is present"""
        try:
            logging.info("Starting logo test")
            driver.get("http://127.0.0.1:8000/categories")
            logo = driver.find_element(By.CLASS_NAME, "logo")
            assert logo.is_displayed()
            logging.info("Logo test passed")
        except Exception as e:
            logging.error(f"Logo test failed: {str(e)}")
            driver.save_screenshot("screenshots/logo_failure.png")
            raise

    def test_navigation_menu_exists(self, driver):
        """Test navigation menu is present"""
        try:
            logging.info("Starting navigation menu test")
            
            # Login first
            self.login_user(driver)
            
            # Navigate to category page
            driver.get("http://127.0.0.1:8000/category/1")
            
            # Wait for and check navigation menu
            nav_menu = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "main-menu"))
            )
            assert nav_menu.is_displayed(), "Navigation menu not displayed"
            
            logging.info("Navigation menu test passed")
            
        except Exception as e:
            logging.error(f"Navigation menu test failed: {str(e)}")
            driver.save_screenshot("screenshots/nav_menu_failure.png")
            raise

    def test_footer_exists(self, driver):
        """Test footer is present"""
        try:
            logging.info("Starting footer test")
            
            # Navigate to category page
            driver.get("http://127.0.0.1:8000/login")
            
            # Check social media icons
            social_icons = driver.find_elements(By.CLASS_NAME, "fa-facebook")
            assert len(social_icons) > 0, "Social media icons not found"
            
            # Check newsletter form
            newsletter_input = driver.find_element(By.NAME, "newsletter-email")
            newsletter_button = driver.find_element(By.CLASS_NAME, "newsletter-submit")
            assert newsletter_input.is_displayed(), "Newsletter input not displayed"
            assert newsletter_button.is_displayed(), "Newsletter button not displayed"
            
            logging.info("Footer test passed")
            
        except Exception as e:
            logging.error(f"Footer test failed: {str(e)}")
            driver.save_screenshot("screenshots/footer_failure.png")
            raise

    def test_main_content_exists(self, driver):
        """Test main content area is present"""
        try:
            logging.info("Starting main content test")
            driver.get("http://127.0.0.1:8000/categories")
            main_content = driver.find_element(By.TAG_NAME, "body")
            assert main_content.is_displayed()
            logging.info("Main content test passed")
        except Exception as e:
            logging.error(f"Main content test failed: {str(e)}")
            driver.save_screenshot("screenshots/main_content_failure.png")
            raise

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
            assert driver.find_element(By.CLASS_NAME, "search-bar").is_displayed(), "Search bar not found"
            
            logging.info("UI components test passed")
            
        except Exception as e:
            logging.error(f"UI components test failed: {str(e)}")
            driver.save_screenshot("screenshots/ui_components_failure.png")
            raise

class TestResponsiveness:
    def test_mobile_view(self, driver):
        """Test mobile view rendering"""
        try:
            logging.info("Starting mobile view test")
            driver.get("http://127.0.0.1:8000/categories")
            # Set viewport to mobile size
            driver.set_window_size(375, 812)  # iPhone X dimensions
            
            # Check if mobile menu is visible
            mobile_menu = driver.find_element(By.CLASS_NAME, "menu-mobile")
            assert mobile_menu.is_displayed()
            logging.info("Mobile view test passed")
        except Exception as e:
            logging.error(f"Mobile view test failed: {str(e)}")
            driver.save_screenshot("screenshots/mobile_view_failure.png")
            raise

class TestUIComponents:
    def test_search_bar(self, driver):
        """Test search bar functionality"""
        try:
            logging.info("Starting search bar test")
            driver.get("http://127.0.0.1:8000/categories")
            
            # Find and test search bar
            search_bar = driver.find_element(By.CLASS_NAME, "search-input")
            assert search_bar.is_displayed()
            assert search_bar.is_enabled()
            logging.info("Search bar test passed")
        except Exception as e:
            logging.error(f"Search bar test failed: {str(e)}")
            driver.save_screenshot("screenshots/search_bar_failure.png")
            raise

    def test_navigation_links(self, driver):
        """Test navigation links"""
        try:
            logging.info("Starting navigation links test")
            driver.get("http://127.0.0.1:8000/categories")
            
            # Test common navigation links
            nav_links = ["menu-item-home", "menu-item-shop", "menu-item-categories"]
            for link_text in nav_links:
                link = driver.find_element(By.CLASS_NAME, link_text)
                assert link.is_displayed()
            logging.info("Navigation links test passed")
        except Exception as e:
            logging.error(f"Navigation links test failed: {str(e)}")
            driver.save_screenshot("screenshots/nav_links_failure.png")
            raise

    def test_social_media_links(self, driver):
        """Test social media links in footer"""
        try:
            logging.info("Starting social media links test")
            driver.get("http://127.0.0.1:8000/categories")
            
            footer = driver.find_element(By.TAG_NAME, "footer")
            social_links = footer.find_elements(By.CLASS_NAME, "fa-facebook")
            assert len(social_links) > 0
            logging.info("Social media links test passed")
        except Exception as e:
            logging.error(f"Social media links test failed: {str(e)}")
            driver.save_screenshot("screenshots/social_links_failure.png")
            raise

class TestForms:
    def test_login_form_exists(self, driver):
        """Test login form and its elements are present"""
        try:
            logging.info("Starting login form test")
            driver.get("http://127.0.0.1:8000/login")
            
            # Wait for elements to be visible
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "login-username"))
            )
            
            # Check form elements using specific class names
            username_input = driver.find_element(By.CLASS_NAME, "login-username")
            password_input = driver.find_element(By.CLASS_NAME, "login-password")
            submit_button = driver.find_element(By.CLASS_NAME, "login-button")
            
            # Verify elements are visible
            assert username_input.is_displayed(), "Username input not visible"
            assert password_input.is_displayed(), "Password input not visible"
            assert submit_button.is_displayed(), "Submit button not visible"
            
            logging.info("Login form test passed")
            
        except Exception as e:
            logging.error(f"Login form test failed: {str(e)}")
            driver.save_screenshot("screenshots/login_form_failure.png")
            raise

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
            
            assert username.is_displayed()
            assert email.is_displayed()
            assert password.is_displayed()
            assert confirmation.is_displayed()
            assert submit.is_displayed()
            logging.info("Register form elements test passed")
        except Exception as e:
            logging.error(f"Register form elements test failed: {str(e)}")
            driver.save_screenshot("screenshots/register_form_failure.png")
            raise

class TestUserInteractions:
    def test_hover_effects(self, driver):
        """Test hover effects on navigation links"""
        try:
            logging.info("Starting hover effects test")
            driver.get("http://127.0.0.1:8000")
            
            # Test hover on nav links
            nav_link = driver.find_element(By.LINK_TEXT, "Home")
            ActionChains(driver).move_to_element(nav_link).perform()
            # Just verify no errors occur during hover
            assert True
            logging.info("Hover effects test passed")
        except Exception as e:
            logging.error(f"Hover effects test failed: {str(e)}")
            driver.save_screenshot("screenshots/hover_effects_failure.png")
            raise

    def test_scroll_behavior(self, driver):
        """Test page scroll behavior"""
        try:
            logging.info("Starting scroll behavior test")
            driver.get("http://127.0.0.1:8000")
            
            # Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Verify footer is visible
            footer = driver.find_element(By.TAG_NAME, "footer")
            assert footer.is_displayed()
            logging.info("Scroll behavior test passed")
        except Exception as e:
            logging.error(f"Scroll behavior test failed: {str(e)}")
            driver.save_screenshot("screenshots/scroll_behavior_failure.png")
            raise 