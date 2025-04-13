import unittest
import os
import concurrent.futures
import base64

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

from components.button import Button
from components.textfield import TextField
from helper import Helper


username = os.getenv("LT_USERNAME")  # Replace the username
access_key = os.getenv("LT_ACCESS_KEY")  # Replace the access key


# paste your capibility options below

options = ChromeOptions()
options.browser_version = "latest"
prefs = {
            "profile.password_manager_leak_detection": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
options.add_experimental_option("prefs", prefs)
options.platform_name = "Windows 10"
lt_options = {}
lt_options["username"] = username
lt_options["accessKey"] = access_key
# lt_options["video"] = True
# lt_options["resolution"] = "1920x1080"
lt_options["network"] = True
lt_options["build"] = "Selenium 4 Example"
# lt_options["project"] = "unit_testing"
lt_options["smartUI.project"] = "test"
lt_options["name"] = "Selenium 4 Sample Test"
lt_options["w3c"] = True
lt_options["plugin"] = "python-python"
lt_options["terminal"] = True
lt_options["console"] = True
lt_options["devicelog"] = True
options.set_capability("LT:Options", lt_options)


# Steps to run Smart UI project (https://beta-smartui.lambdatest.com/)
# Step - 1 : Change the hub URL to @beta-smartui-hub.lambdatest.com/wd/hub
# Step - 2 : Add "smartUI.project": "<Project Name>" as a capability above
# Step - 3 : Run "driver.execute_script("smartui.takeScreenshot")" command wherever you need to take a screenshot
# Note: for additional capabilities navigate to https://www.lambdatest.com/support/docs/test-settings-options/


class FirstSampleTest(unittest.TestCase):
    driver = None

    def setUp(self):

        
        self.driver = webdriver.Remote(
            command_executor="http://{}:{}@hub.lambdatest.com/wd/hub".format(
                username, access_key
            ),
            options=options,
        )

        self.helper = Helper(self.driver)
        self.button = Button(self.driver)
        self.text_field = TextField(self.driver)
        self.status = None

    # """ You can write the test cases here """
    def test_demo_site(self):
        # try:
        driver = self.driver
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        driver.set_window_size(1920, 1080)

        # Url
        driver.execute_script('console.log("Loading URL")')
        driver.get(
            "https://stage-lambda-devops-use-only.lambdatestinternal.com/To-do-app/index.html"
        )

        # Let's click on a element
        driver.find_element(By.NAME, "li1").click()
        location = driver.find_element(By.NAME, "li2")
        location.click()
        driver.execute_script('console.log("Clicked on the second element")')

        # Take Smart UI screenshot
        # driver.execute_script("smartui.takeScreenshot")

        # Let's add a checkbox
        driver.find_element(By.ID, "sampletodotext").send_keys("LambdaTest")
        add_button = driver.find_element(By.ID, "addbutton")
        add_button.click()
        driver.execute_script('console.log("Added LambdaTest checkbox")')

        # print the heading
        search = driver.find_element(By.CSS_SELECTOR, ".container h2")
        assert search.is_displayed(), "heading is not displayed"
        driver.execute_script('console.log(search.text)')
        search.click()
        driver.implicitly_wait(3)

        # Let's download the invoice
        heading = driver.find_element(By.CSS_SELECTOR, ".container h2")
        if heading.is_displayed():
            heading.click()
            driver.execute_script("lambda-status=passed")
            driver.execute_script('console.log("Tests are run successfully!")')
        else:
            driver.execute_script("lambda-status=failed")
    
    def test_one(self):
        driver = self.driver
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        driver.set_window_size(1920, 1080)

        driver.execute_script('console.log("Opening Login website")')

        driver.get(
            "https://the-internet.herokuapp.com/login"
        )

        try:

            driver.execute_script('console.log("Logging in with correct credentials")')
            self.helper.login(os.getenv("LT_WEBSITE_USER"), os.getenv("LT_WEBSITE_PASS"))

            self.helper.wait_for_page_completion()

            driver.execute_script('console.log("Checking logged banner")')

            banner_xpath = '//*[@id="flash"]'

            banner_text = driver.find_element(By.XPATH, banner_xpath).text

            assert "You logged into a secure area!" in banner_text.strip(), "Login message is not correct!"

            driver.execute_script('console.log("Green login banner visible!")')

            driver.execute_script('console.log("Checking logout button visibility")')

            assert self.button.is_logout_button_displayed(), "Logout button is not visible!"

            driver.execute_script('console.log("Logout button is visible")')

            driver.execute_script('console.log("Logging user out")')

            self.button.click_logout_button()

            self.helper.wait_for_page_completion()

            assert driver.current_url == "https://the-internet.herokuapp.com/login", "Not redirected to login page after logout!"

            driver.execute_script('console.log("User logout successful")')

            driver.execute_script('console.log("Trying invalid username and/or password")')

            self.helper.login(os.getenv("LT_WEBSITE_USER")+"321312", os.getenv("LT_WEBSITE_PASS")+"312312")

            driver.execute_script('console.log("Checking error banner")')

            banner_text = driver.find_element(By.XPATH, banner_xpath).text

            assert "Your username is invalid!" in banner_text.strip(), "Error message is not correct!"

            driver.execute_script('console.log("Validated incorrect username and/or pass. Error banner is visible")')
            driver.execute_script('console.log("Tests are run successfully!")')

            self.status = True
        
        except Exception as e:
            driver.execute_script(f'console.log("Failed with expection: {e}")')
            self.status = False
    

    def test_two(self):

        try:
            driver = self.driver
            driver.implicitly_wait(10)
            driver.set_page_load_timeout(30)
            driver.set_window_size(1920, 1080)

            driver.execute_script('console.log("Opening JS alert website")')

            driver.get(
                "https://the-internet.herokuapp.com/javascript_alerts"
            )

            self.helper.wait_for_page_completion()

            driver.execute_script('console.log("Checking Alert button")')

            self.button.click_js_action("alert")

            alert = driver.switch_to.alert

            alert.accept()

            assert "You successfully clicked an alert" in self.helper.get_result_text(), "Wrong result for alert"

            driver.execute_script('console.log("Alert present and was accepted")')

            driver.execute_script('console.log("Checking Prompt dismiss button")')

            self.button.click_js_action("Confirm")

            alert = driver.switch_to.alert

            alert.dismiss()

            assert "You clicked: Cancel" in self.helper.get_result_text(), "Wrong result for confirm dismiss"

            driver.execute_script('console.log("Checking Prompt accept button")')

            self.button.click_js_action("Confirm")

            alert = driver.switch_to.alert

            alert.accept()

            assert "You clicked: Ok" in self.helper.get_result_text(), "Wrong result for confirm accept"

            driver.execute_script('console.log("Validated JS Confirm")')

            driver.execute_script('console.log("Checking JS Prompt")')

            self.button.click_js_action("Prompt")

            alert = driver.switch_to.alert
            alert.send_keys("Hello!")
            alert.accept()

            assert "You entered: a" in self.helper.get_result_text(), "Wrong result for prompt keys"

            driver.execute_script('console.log("Validated JS Prompt")')

            self.status = True
        
        except Exception as e:
            driver.execute_script(f'console.log("Failed with expection: {e}")')
            self.status = False
    
    # tearDown runs after each test case
    def tearDown(self):
        self.driver.quit()

def run_test_method(method_name):
        suite = unittest.TestSuite()
        suite.addTest(FirstSampleTest(method_name))
        runner = unittest.TextTestRunner()
        runner.run(suite)

if __name__ == "__main__":
    test_methods = ['test_one', 'test_two']

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(run_test_method, test_methods)
    # unittest.main()
