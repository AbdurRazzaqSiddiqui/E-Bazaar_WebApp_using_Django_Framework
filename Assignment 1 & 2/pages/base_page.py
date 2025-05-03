from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))
    
    def find_clickable_element(self, by, value):
        return self.wait.until(EC.element_to_be_clickable((by, value)))
    
    def click_element(self, by, value):
        element = self.find_clickable_element(by, value)
        self.driver.execute_script("arguments[0].click();", element)
    
    def input_text(self, by, value, text):
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)
    
    def is_url(self, url):
        return self.wait.until(EC.url_to_be(url))
    
    def take_screenshot(self, name):
        self.driver.save_screenshot(f"screenshots/{name}.png") 