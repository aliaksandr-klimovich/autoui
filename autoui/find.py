from selenium.webdriver.remote.webelement import WebElement
from autoui.base import BaseSection
from autoui.driver import get_driver


class Find(object):
    def __init__(self, element=WebElement, locator=None):
        self.element = element
        self.locator = locator

    def __get__(self, instance, owner):
        return self.element.find_element(self.element(), *self.locator)
