from selenium.webdriver.common.by import By

class Button():
    def __init__(self, driver):
        self.driver = driver

    def is_login_button_displayed(self):

        login_xpath = "//button/*[text()=' Login']"
        login_element = self.driver.find_element(By.XPATH, login_xpath)

        return login_element.is_displayed(), login_element
    
    def click_login_button(self):
        is_button_displayed, logout_element = self.is_login_button_displayed()

        if is_button_displayed:
            logout_element.click()
        
    def is_logout_button_displayed(self):

        logout_xpath = "//a/*[text()=' Logout']"
        logout_element = self.driver.find_element(By.XPATH, logout_xpath)

        return logout_element.is_displayed(), logout_element
    
    def click_logout_button(self):
        
        is_button_displayed, logout_element = self.is_logout_button_displayed()

        if is_button_displayed:
            logout_element.click()
    
    def click_js_action(self, action: str):

        text = None
        if action.lower() == "alert":
            text = "Alert"
        elif action.lower() == "confirm":
            text = "Confirm"
        elif action.lower() == "prompt":
            text = "Prompt"
        
        xpath = f"//button[text()='Click for JS {text}']"
        self.driver.find_element(By.XPATH, xpath).click()

