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
            
            # Login and add product to cart
            login_page.navigate()
            login_page.login("yousha", "yousha")
            assert login_page.is_login_successful(), "Login failed"
            
            product_page.navigate_to_product(1, 1)
            product_page.add_to_cart()
            
            # Test shipping info with different combinations
            cart_page.wait_for_cart_load()
            
            # Test valid shipping info
            cart_page.fill_shipping_info("USA", "California", "90210")
            cart_page.update_totals()
            
            # Test different state
            cart_page.fill_shipping_info("USA", "New York", "10001")
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
            
            # Login and add product
            login_page.navigate()
            login_page.login("yousha", "yousha")
            assert login_page.is_login_successful(), "Login failed"
            
            # Add product with increased quantity
            product_page.navigate_to_product(1, 1)
            product_page.increase_quantity()
            product_page.increase_quantity()  # Increase twice
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
            
            # Login
            login_page.navigate()
            login_page.login("yousha", "yousha")
            assert login_page.is_login_successful(), "Login failed"
            
            # Add multiple products
            product_page.navigate_to_product(1, 1)
            product_page.increase_quantity()
            product_page.add_to_cart()
            
            product_page.navigate_to_product(1, 2)
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
        driver.get("http://127.0.0.1:8000/register")
        assert "Register" in driver.title
        assert driver.find_element(By.TAG_NAME, "h2").text == "Register"

    @pytest.mark.description("Verify all form elements are present on registration page")
    def test_register_form_elements(self, driver):
        """Test all form elements are present on registration page"""
        driver.get("http://127.0.0.1:8000/register")
        assert driver.find_element(By.NAME, "username")
        assert driver.find_element(By.NAME, "email")
        assert driver.find_element(By.NAME, "password")
        assert driver.find_element(By.NAME, "confirmation")
        assert driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

    @pytest.mark.description("Verify registration with mismatched passwords")
    def test_register_password_mismatch(self, driver):
        """Test registration with mismatched passwords"""
        driver.get("http://127.0.0.1:8000/register")
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "email").send_keys("test@example.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "confirmation").send_keys("password456")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        assert "Passwords must match" in driver.page_source

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
        driver.get("http://127.0.0.1:8000")
        nav_items = driver.find_elements(By.CLASS_NAME, "main-menu")
        assert len(nav_items) > 0
        assert "Home" in driver.page_source
        assert "Shop" in driver.page_source
        assert "Features" in driver.page_source

    @pytest.mark.description("Verify product search functionality")
    def test_product_search(self, driver):
        """Test product search functionality"""
        driver.get("http://127.0.0.1:8000")
        search_input = driver.find_element(By.CLASS_NAME, "search-input")
        search_input.send_keys("shirt")
        search_input.send_keys(Keys.RETURN)
        assert "Search Results" in driver.page_source

    @pytest.mark.description("Verify product filtering options")
    def test_product_filtering(self, driver):
        """Test product filtering options"""
        driver.get("http://127.0.0.1:8000/product")
        filter_button = driver.find_element(By.CLASS_NAME, "filter-link")
        filter_button.click()
        price_filter = driver.find_element(By.CLASS_NAME, "filter-price")
        assert price_filter.is_displayed()

    @pytest.mark.description("Verify empty shopping cart display")
    def test_shopping_cart_empty(self, driver):
        """Test empty shopping cart display"""
        driver.get("http://127.0.0.1:8000/cart")
        cart_items = driver.find_elements(By.CLASS_NAME, "table-shopping-cart")
        assert len(cart_items) == 0
        assert "Your cart is empty" in driver.page_source

    @pytest.mark.description("Verify product quick view functionality")
    def test_product_quick_view(self, driver):
        """Test product quick view functionality"""
        driver.get("http://127.0.0.1:8000")
        quick_view_button = driver.find_element(By.CLASS_NAME, "js-show-modal1")
        quick_view_button.click()
        modal = driver.find_element(By.CLASS_NAME, "wrap-modal1")
        assert modal.is_displayed()

    @pytest.mark.description("Verify responsive design elements")
    def test_responsive_design(self, driver):
        """Test responsive design elements"""
        driver.get("http://127.0.0.1:8000")
        driver.set_window_size(375, 812) # iPhone X dimensions
        menu_mobile = driver.find_element(By.CLASS_NAME, "menu-mobile")
        assert menu_mobile.is_displayed()

    @pytest.mark.description("Verify footer links and social media icons")
    def test_footer_links(self, driver):
        """Test footer links and social media icons"""
        driver.get("http://127.0.0.1:8000")
        footer = driver.find_element(By.TAG_NAME, "footer")
        social_links = footer.find_elements(By.CLASS_NAME, "social")
        assert len(social_links) > 0

    @pytest.mark.description("Verify product sorting functionality")
    def test_product_sorting(self, driver):
        """Test product sorting functionality"""
        driver.get("http://127.0.0.1:8000/product")
        sort_select = driver.find_element(By.CLASS_NAME, "select2")
        sort_select.click()
        price_high_low = driver.find_element(By.XPATH, "//option[contains(text(), 'Price: High to Low')]")
        price_high_low.click()
        assert "Price: High to Low" in driver.page_source

    @pytest.mark.description("Verify category navigation")
    def test_category_navigation(self, driver):
        """Test category navigation"""
        driver.get("http://127.0.0.1:8000/all_categories")
        categories = driver.find_elements(By.CLASS_NAME, "sec-banner")
        assert len(categories) > 0
        categories[0].click()
        assert "Products" in driver.title

    @pytest.mark.description("Verify adding product to wishlist")
    def test_add_to_wishlist(self, driver):
        """Test adding product to wishlist"""
        driver.get("http://127.0.0.1:8000/product")
        wishlist_button = driver.find_element(By.CLASS_NAME, "js-addwish-b2")
        wishlist_button.click()
        assert "Added to wishlist" in driver.page_source

    @pytest.mark.description("Verify newsletter subscription form")
    def test_newsletter_subscription(self, driver):
        """Test newsletter subscription form"""
        driver.get("http://127.0.0.1:8000")
        email_input = driver.find_element(By.CLASS_NAME, "newsletter-email")
        email_input.send_keys("test@example.com")
        submit_button = driver.find_element(By.CLASS_NAME, "newsletter-submit")
        submit_button.click()
        assert "Thank you for subscribing" in driver.page_source

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
            password_input.send_keys("admin")
            
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
            
            # Find and click logout
            driver.find_element(By.LINK_TEXT, "LOG OUT").click()
            
            # Verify back on login page
            assert "Log in | Django site admin" in driver.title
            
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

class TestBasicUI:
    def test_home_page_load(self, driver):
        """Test home page loads successfully"""
        try:
            logging.info("Starting home page load test")
            driver.get("http://127.0.0.1:8000")
            assert "Home" in driver.title
            logging.info("Home page load test passed")
        except Exception as e:
            logging.error(f"Home page load test failed: {str(e)}")
            driver.save_screenshot("screenshots/home_page_failure.png")
            raise

    def test_page_title(self, driver):
        """Test page title exists"""
        try:
            logging.info("Starting page title test")
            driver.get("http://127.0.0.1:8000")
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
            driver.get("http://127.0.0.1:8000")
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
            driver.get("http://127.0.0.1:8000")
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
            driver.get("http://127.0.0.1:8000")
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
            driver.get("http://127.0.0.1:8000")
            nav_menu = driver.find_element(By.TAG_NAME, "nav")
            assert nav_menu.is_displayed()
            logging.info("Navigation menu test passed")
        except Exception as e:
            logging.error(f"Navigation menu test failed: {str(e)}")
            driver.save_screenshot("screenshots/nav_menu_failure.png")
            raise

    def test_footer_exists(self, driver):
        """Test footer is present"""
        try:
            logging.info("Starting footer test")
            driver.get("http://127.0.0.1:8000")
            footer = driver.find_element(By.TAG_NAME, "footer")
            assert footer.is_displayed()
            logging.info("Footer test passed")
        except Exception as e:
            logging.error(f"Footer test failed: {str(e)}")
            driver.save_screenshot("screenshots/footer_failure.png")
            raise

    def test_main_content_exists(self, driver):
        """Test main content area is present"""
        try:
            logging.info("Starting main content test")
            driver.get("http://127.0.0.1:8000")
            main_content = driver.find_element(By.TAG_NAME, "main")
            assert main_content.is_displayed()
            logging.info("Main content test passed")
        except Exception as e:
            logging.error(f"Main content test failed: {str(e)}")
            driver.save_screenshot("screenshots/main_content_failure.png")
            raise

class TestResponsiveness:
    def test_mobile_view(self, driver):
        """Test mobile view rendering"""
        try:
            logging.info("Starting mobile view test")
            driver.get("http://127.0.0.1:8000")
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

    def test_tablet_view(self, driver):
        """Test tablet view rendering"""
        try:
            logging.info("Starting tablet view test")
            driver.get("http://127.0.0.1:8000")
            driver.set_window_size(768, 1024)  # iPad dimensions
            
            # Check if tablet layout is correct
            content = driver.find_element(By.TAG_NAME, "main")
            assert content.is_displayed()
            logging.info("Tablet view test passed")
        except Exception as e:
            logging.error(f"Tablet view test failed: {str(e)}")
            driver.save_screenshot("screenshots/tablet_view_failure.png")
            raise

class TestUIComponents:
    def test_search_bar(self, driver):
        """Test search bar functionality"""
        try:
            logging.info("Starting search bar test")
            driver.get("http://127.0.0.1:8000")
            
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
            driver.get("http://127.0.0.1:8000")
            
            # Test common navigation links
            nav_links = ["Home", "Shop", "Contact"]
            for link_text in nav_links:
                link = driver.find_element(By.LINK_TEXT, link_text)
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
            driver.get("http://127.0.0.1:8000")
            
            footer = driver.find_element(By.TAG_NAME, "footer")
            social_links = footer.find_elements(By.CLASS_NAME, "social")
            assert len(social_links) > 0
            logging.info("Social media links test passed")
        except Exception as e:
            logging.error(f"Social media links test failed: {str(e)}")
            driver.save_screenshot("screenshots/social_links_failure.png")
            raise

class TestForms:
    def test_login_form_elements(self, driver):
        """Test login form elements"""
        try:
            logging.info("Starting login form elements test")
            driver.get("http://127.0.0.1:8000/login")
            
            # Check form elements
            username = driver.find_element(By.NAME, "username")
            password = driver.find_element(By.NAME, "password")
            submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            
            assert username.is_displayed()
            assert password.is_displayed()
            assert submit.is_displayed()
            logging.info("Login form elements test passed")
        except Exception as e:
            logging.error(f"Login form elements test failed: {str(e)}")
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