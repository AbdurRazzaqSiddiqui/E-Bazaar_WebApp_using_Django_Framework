from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage

class CartPage(BasePage):
    # Locators
    CART_TABLE = (By.CLASS_NAME, "table-shopping-cart")
    COUNTRY_SELECT = (By.NAME, "time")
    STATE_INPUT = (By.NAME, "state")
    POSTCODE_INPUT = (By.NAME, "postcode")
    UPDATE_BUTTON = (By.CSS_SELECTOR, "div.flex-c-m.stext-101.cl2.size-115.bg8.bor13.hov-btn3.p-lr-15.trans-04.pointer")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "button.flex-c-m.stext-101.cl0.size-116.bg3.bor14.hov-btn3.p-lr-15.trans-04.pointer")
    
    def wait_for_cart_load(self):
        self.find_element(*self.CART_TABLE)
    
    def fill_shipping_info(self, country, state, postcode):
        # Select country
        country_select = Select(self.find_element(*self.COUNTRY_SELECT))
        country_select.select_by_visible_text(country)
        
        # Fill state and postcode
        self.input_text(*self.STATE_INPUT, state)
        self.input_text(*self.POSTCODE_INPUT, postcode)
    
    def update_totals(self):
        self.click_element(*self.UPDATE_BUTTON)
    
    def proceed_to_checkout(self):
        self.click_element(*self.CHECKOUT_BUTTON) 