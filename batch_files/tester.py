import unittest
from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://172.17.0.9:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        self.driver.implicitly_wait(5)

    def test_login(self):
        self.driver.get("http://104.131.127.229/user/login/")
        username = self.driver.find_element_by_id("id_username")
        username.send_keys("adinh")

        password = self.driver.find_element_by_id("id_password")
        password.send_keys("flash")

        self.driver.find_element_by_xpath("//button[@type='submit']").click()

    def test_sign_up(self):
        self.driver.get("http://104.131.127.229/user/signup")

        username = self.driver.find_element_by_id("id_first_name")
        username.send_keys("linda")

        password = self.driver.find_element_by_id("id_last_name")
        password.send_keys("jiong")

        username = self.driver.find_element_by_id("id_username")
        username.send_keys("linda")

        password = self.driver.find_element_by_id("id_password")
        password.send_keys("jiong")

        self.driver.find_element_by_xpath("//button[@type='submit']").click()

    def tearDown(self):
        self.driver.close()
        # display.stop()


if __name__ == '__main__':
    unittest.main()
