from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time

# Setup class for Selenium tests
class SeleniumSetupTest:
    def __init__(self):
        # Initialize Chrome WebDriver
        self.driver = webdriver.Chrome()
        # Maximize browser window
        self.driver.maximize_window()
        # Base URL for our test website
        self.base_url = "http://127.0.0.1:8000"
    
    def test_google_search(self):
        """
        A simple test that:
        1. Opens Google
        2. Searches for 'Selenium WebDriver'
        3. Verifies search results appear
        """
        try:
            # Navigate to Google
            self.driver.get("https://www.google.com")
            
            # Find search box and enter text
            search_box = self.driver.find_element(By.NAME, "q")
            search_box.send_keys("Selenium WebDriver")
            search_box.send_keys(Keys.RETURN)
            
            # Wait for search results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            # Verify search results are displayed
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            assert len(search_results) > 0, "No search results found"
            
            print("Test passed successfully!")
            
        except Exception as e:
            print(f"Test failed: {str(e)}")
            
        finally:
            # Close the browser
            self.driver.quit()
    
    def test_login(self):
        """
        Test login functionality with your credentials
        """
        try:
            # Navigate to login page
            self.driver.get(f"{self.base_url}/login")
            
            # Enter login credentials
            username = self.driver.find_element(By.NAME, "username")
            password = self.driver.find_element(By.NAME, "password")
            
            username.send_keys("yousha")
            password.send_keys("yousha")
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            login_button.click()
            
            # Wait for redirect to index page
            WebDriverWait(self.driver, 10).until(
                EC.url_to_be(f"{self.base_url}/")
            )
            
            print("Login test passed successfully!")
            return True
            
        except Exception as e:
            print(f"Login test failed: {str(e)}")
            return False
    
    def test_form_submission(self):
        """
        Test registration form submission
        """
        try:
            self.driver.get(f"{self.base_url}/register")
            
            # Fill registration form
            username = self.driver.find_element(By.NAME, "username")
            email = self.driver.find_element(By.NAME, "email")
            user_type = self.driver.find_element(By.NAME, "user_type")
            password = self.driver.find_element(By.NAME, "password")
            confirmation = self.driver.find_element(By.NAME, "confirmation")
            
            # Use test data
            username.send_keys("testuser123")
            email.send_keys("test@example.com")
            user_type.send_keys("Customer")
            password.send_keys("testpass123")
            confirmation.send_keys("testpass123")
            
            # Submit form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            submit_button.click()
            
            # Wait for redirect to index page after successful registration
            WebDriverWait(self.driver, 10).until(
                EC.url_to_be(f"{self.base_url}/")
            )
            
            print("Form submission test passed successfully!")
            
        except Exception as e:
            print(f"Form submission test failed: {str(e)}")
    
    def test_place_order(self):
        """
        Test adding product to cart and checkout process
        """
        try:
            # First login
            if not self.test_login():
                raise Exception("Login failed, cannot proceed with order test")
            
            print("Starting order placement test...")
            
            # Navigate to specific product
            self.driver.get(f"{self.base_url}/category/1/product/1")
            time.sleep(2)
            print("On product detail page...")
            
            # Find quantity input and buttons
            quantity_container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "wrap-num-product"))
            )
            
            # Click the plus button to increase quantity
            plus_button = quantity_container.find_element(
                By.CLASS_NAME, "btn-num-product-up"
            )
            plus_button.click()
            print("Increased quantity...")
            
            # Find and click the Add to Cart button
            add_to_cart_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 
                    "button.flex-c-m.stext-101.cl0.size-101.bg1.bor1.hov-btn1.p-lr-15.trans-04.js-addcart-detail"
                ))
            )
            self.driver.execute_script("arguments[0].click();", add_to_cart_button)
            print("Clicked Add to Cart button...")
            
            # Wait for cart page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "table-shopping-cart"))
            )
            print("Cart page loaded...")
            
            try:
                # Find the shipping form
                shipping_form = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "rs1-select2"))
                )
                
                # Select country using JavaScript
                country_select = self.driver.find_element(By.NAME, "time")
                self.driver.execute_script(
                    "arguments[0].value = 'USA';", 
                    country_select
                )
                print("Selected country...")
                
                # Fill state
                state_input = self.driver.find_element(By.NAME, "state")
                state_input.send_keys("California")
                print("Entered state...")
                
                # Fill postcode
                postcode_input = self.driver.find_element(By.NAME, "postcode")
                postcode_input.send_keys("90210")
                print("Entered postcode...")
                
                # Find and click Update Totals using JavaScript
                update_button = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    "div.flex-c-m.stext-101.cl2.size-115.bg8.bor13.hov-btn3.p-lr-15.trans-04.pointer"
                )
                self.driver.execute_script("arguments[0].click();", update_button)
                print("Clicked Update Totals...")
                
                # Wait a moment for totals to update
                time.sleep(2)
                
                # Find and click Proceed to Checkout using JavaScript
                checkout_button = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    "button.flex-c-m.stext-101.cl0.size-116.bg3.bor14.hov-btn3.p-lr-15.trans-04.pointer"
                )
                self.driver.execute_script("arguments[0].click();", checkout_button)
                print("Clicked Proceed to Checkout...")
                
            except Exception as e:
                print(f"Error during shipping form: {str(e)}")
                print(f"Current URL during error: {self.driver.current_url}")
                print("Page source:", self.driver.page_source[:500])
                raise
            
            print("Order placement test completed successfully!")
            
        except Exception as e:
            print(f"Order placement test failed: {str(e)}")
            print(f"Current URL: {self.driver.current_url}")
            self.driver.save_screenshot("error_screenshot.png")
        
        finally:
            # Close the browser
            self.driver.quit()

# Run all tests
if __name__ == "__main__":
    test = SeleniumSetupTest()
    test.test_place_order()  # This will run login first, then test the order process
