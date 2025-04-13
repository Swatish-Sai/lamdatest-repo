from selenium.webdriver.common.by import By

class TextField():

    def __init__(self, driver):
        self.driver = driver

    def fill_text(self, id: str, text: str):
        """
        Fills text in the field with corresponding html input "id"
        """

        web_element = self.driver.find_element(By.ID, id)
        web_element.send_keys(text)
