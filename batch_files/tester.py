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
        username.send_keys("abc")

        password = self.driver.find_element_by_id("id_password")
        password.send_keys("abc")

        self.driver.find_element_by_xpath("//button[@type='submit']").click()

    # def test_logout(self):
    #     self.driver.get("http://104.131.127.229/user/login/")
    #     username = self.driver.find_element_by_id("id_username")
    #     username.send_keys("abc")
    #
    #     password = self.driver.find_element_by_id("id_password")
    #     password.send_keys("abc")
    #
    #     self.driver.find_element_by_xpath("//button[@type='submit']").click()
    #
    #     self.driver.implicitly_wait(10)
    #
    #     self.driver.find_element_by_xpath("//a[@href='/user/logout/']").click()
    #
    # def test_search(self):
    #     self.driver.get("http://104.131.127.229/user/login/")
    #     username = self.driver.find_element_by_id("id_username")
    #     username.send_keys("abc")
    #
    #     password = self.driver.find_element_by_id("id_password")
    #     password.send_keys("abc")
    #
    #     self.driver.find_element_by_xpath("//button[@type='submit']").click()
    #
    #     elem = self.driver.find_element_by_name('search_box')
    #     elem.send_keys('jacket')
    #
    #     self.driver.implicitly_wait(10)
    #
    #     self.driver.find_element_by_xpath("//a[@href='/item/display/1/']").click()

    def tearDown(self):
        self.driver.close()
        # display.stop()


if __name__ == '__main__':
    unittest.main()
