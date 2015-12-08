from unittest import TestCase

from nose.tools import eq_
from selenium.webdriver.common.by import By

from autoui.locators import Locator, XPath, CSS, ID


class TestLocatorInit(TestCase):
    def test_declaration(self):
        Locator(By.ID, 'value')

    def test_id_locator(self):
        id = ID('value')
        eq_(id.by, By.ID)
        eq_(id.value, 'value')

    def test_css_locator(self):
        css = CSS('value')
        eq_(css.by, By.CSS_SELECTOR)
        eq_(css.value, 'value')

    def test_xpath_locator(self):
        xpath = XPath('value')
        eq_(xpath.by, By.XPATH)
        eq_(xpath.value, 'value')

    def test_invalid_by_type(self):
        with self.assertRaises(TypeError):
            Locator(True, 'value')

    def test_invalid_value_type(self):
        with self.assertRaises(TypeError):
            Locator('id', True)

    def test_derived_class_basic_invalid_value_type(self):
        with self.assertRaises(TypeError):
            XPath(True)


class TestLocatorAttribute(TestCase):
    def test_basic_xpath(self):
        value = '.'
        xpath = XPath(value)
        eq_(xpath.by, By.XPATH)
        eq_(xpath.value, value)

    def test_basic_css(self):
        value = '.class'
        css = CSS(value)
        eq_(css.by, By.CSS_SELECTOR)
        eq_(css.value, value)


class TestLocatorMethods(TestCase):
    def test_get_method(self):
        value = 'v'
        xpath = XPath(value)
        eq_(xpath.get(), (By.XPATH, value,))

    def test_str_method(self):
        value = 'value'
        xpath = XPath(value)
        eq_(str(xpath), 'xpath=value')
