# -*- coding: utf-8 -*-
from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper

class Application:

    def __init__(self, browser, base_url):
        if browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.base_url = base_url

    def open_home_page(self):
        wd = self.wd
        if not wd.current_url.endswith("/my_view_page.php") > 0:
            wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()

    def return_to_home_page(self):
        wd = self.wd
        wd.find_element_by_css_selector("a[href='my_view_page.php']").click()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False
