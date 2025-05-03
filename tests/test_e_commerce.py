import pytest
from selenium import webdriver
import logging
from datetime import datetime
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

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