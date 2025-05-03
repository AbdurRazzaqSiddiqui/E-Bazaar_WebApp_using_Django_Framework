from selenium.webdriver.common.by import By
from .base_page import BasePage

class ProductPage(BasePage):
    # Locators
    QUANTITY_CONTAINER = (By.CLASS_NAME, "wrap-num-product")
    QUANTITY_PLUS = (By.CLASS_NAME, "btn-num-product-up")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.flex-c-m.stext-101.cl0.size-101.bg1.bor1.hov-btn1.p-lr-15.trans-04.js-addcart-detail")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.base_url = "http://127.0.0.1:8000"
    
    def navigate_to_product(self, category_id, product_id):
        self.driver.get(f"{self.base_url}/category/{category_id}/product/{product_id}")
    
    def increase_quantity(self):
        container = self.find_element(*self.QUANTITY_CONTAINER)
        plus_button = container.find_element(*self.QUANTITY_PLUS)
        self.driver.execute_script("arguments[0].click();", plus_button)
    
    def add_to_cart(self):
        self.click_element(*self.ADD_TO_CART_BUTTON) 