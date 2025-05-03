from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[type='submit']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://127.0.0.1:8000/login"
    
    def navigate(self):
        self.driver.get(self.url)
    
    def login(self, username, password):
        self.input_text(*self.USERNAME_INPUT, username)
        self.input_text(*self.PASSWORD_INPUT, password)
        self.click_element(*self.LOGIN_BUTTON)
        
    def is_login_successful(self):
        return self.is_url("http://127.0.0.1:8000/") 