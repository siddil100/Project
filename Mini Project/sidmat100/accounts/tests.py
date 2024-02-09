from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase

class LoginTestCase(LiveServerTestCase):
    def setUp(self):
        # Set up Firefox WebDriver without specifying executable_path
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)  # Implicit wait for elements to load

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        self.browser.get('http://127.0.0.1:8000/')  # Replace with your application's URL

        # Perform login actions using Selenium
        username_input = self.browser.find_element(By.NAME, 'username')  # Using name attribute
        password_input = self.browser.find_element(By.NAME, 'password')  # Using name attribute
        login_button = self.browser.find_element(By.CLASS_NAME, 'login_btn')  # Using class name

        # Input the login credentials
        username_input.send_keys('swetha1')
        password_input.send_keys('shyam@123')
        
        # Click the login button
        login_button.click()

        # Find the "My Profile" link and assert its presence
        my_profile_link = self.browser.find_element(By.LINK_TEXT, 'My Profile')
        self.assertIsNotNone(my_profile_link)  # Assert that the link is found on the page
