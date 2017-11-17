import unittest
from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('./chromedriver_unix') # local path where chromedriver is located, change to wherever

    def test_login(self):
        self.driver = self.driver
        self.driver.get("http://localhost:8000/login")
        username = self.driver.find_element_by_id("username")
        username.send_keys("abc")

        password = self.driver.find_element_by_id("password")
        password.send_keys("abc")

        self.driver.find_element_by_xpath("//button[@type='submit' and @value='Submit']").click()

    def test_logout(self):
        self.driver = self.driver
        self.driver.get("http://localhost:8000/login")
        username = self.driver.find_element_by_id("username")
        username.send_keys("abc")

        password = self.driver.find_element_by_id("password")
        password.send_keys("abc")

        self.driver.find_element_by_xpath("//button[@type='submit' and @value='Submit']").click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "container-fluid")))

        self.driver.find_element_by_xpath("//a[@href='/logout']").click()

    def tearDown(self):
        self.driver.close()
        # display.stop()


class SearchTestCase(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('./chromedriver_unix')

    def test_search(self):
        self.driver.get("http://localhost:8000/search")
        query = self.driver.find_element_by_id("query")
        query.send_keys("1")

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()