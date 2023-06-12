import logging
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver


class LoginPage(BasePage):
    def enter_username(self, username):
        username_input = self.driver.find_element(By.ID, 'email')
        username_input.send_keys(username)

    def enter_password(self, password):
        password_input = self.driver.find_element(By.ID, 'pass')
        password_input.send_keys(password)

    def click_login_button(self):
        login_button = self.driver.find_element(By.NAME, 'login')
        login_button.click()


class HomePage(BasePage):
    def enter_status_message(self, message):
        status_textarea = self.driver.find_element(By.XPATH, "//textarea[contains(@name, 'xhpc_message')]")
        status_textarea.send_keys(message)

    def click_post_button(self):
        post_button = self.driver.find_element(By.XPATH, "//button[@data-testid='react-composer-post-button']")
        post_button.click()


@pytest.fixture
def browser():
    # Initialize the WebDriver instance
    driver = webdriver.Chrome(executable_path="D:\\Driver\\chromedriver.exe")
    yield driver
    # Quit the browser after the test finishes
    driver.quit()


def test_facebook_post_status(browser):
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set username and password
    username = "anandi913028@gmail.com"
    password = "Abc@123456"

    # Open Facebook login page
    logger.info("Opening Facebook login page")
    browser.get("https://www.facebook.com/")

    # Create page objects
    login_page = LoginPage(browser)
    home_page = HomePage(browser)

    # Log in
    logger.info("Logging into Facebook")
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login_button()

    # Post status message
    logger.info("Posting a status message")
    home_page.enter_status_message("Hello World")
    home_page.click_post_button()

    # Wait for the status message to be posted
    WebDriverWait(browser, 10).until(EC.url_contains('home.php'))

    # Verify the status message is posted
    assert "Hello World" in browser.page_source


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
