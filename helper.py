import time
import base64

from selenium.webdriver.common.by import By

from components.button import Button
from components.textfield import TextField

class Helper():
    def __init__(self, driver):
        self.driver = driver
        self.text_field = TextField(driver)
        self.button = Button(driver)
    
    def login(self, username: str, password: str):
        """
        Args:
            username (str): username
            password (str - b64 encoded): base64 encoded password
        """
        self.text_field.fill_text("username", username)
        self.text_field.fill_text("password", base64.b64decode(password).decode())
        self.button.click_login_button()
    
    def logout(self):
        self.button.click_logout_button()
    
    def wait_for_page_completion(self):
        while self.driver.execute_script("return document.readyState;") != "complete":
            time.sleep(5)
    
    def get_result_text(self):
        return self.driver.find_element(By.ID, "result").text
    