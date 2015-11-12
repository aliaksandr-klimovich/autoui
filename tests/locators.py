from unittest import TestCase

from selenium.webdriver.common.by import By

from autoui.locators import _Locator, XPath, CSS
from autoui.exceptions import AutoUIException


class TestLocatorsInit(TestCase):
    def test_basic(self):
        _Locator('value')

    def test_invalid_value_type(self):
        with self.assertRaises(AutoUIException) as e:
            _Locator(True)

        with self.assertRaises(AutoUIException) as e:
            _Locator(False)

        with self.assertRaises(AutoUIException) as e:
            _Locator(1)

        with self.assertRaises(AutoUIException) as e:
            _Locator(0)

    def test_derived_class_basic(self):
        XPath('value')

    def test_derived_class_basic_invalid_value_type(self):
        with self.assertRaises(AutoUIException) as e:
            XPath(True)


class TestLocatorsAttributes(TestCase):
    def test_basic_xpath(self):
        value = '.'
        xpath = XPath(value)
        assert xpath.by == By.XPATH
        assert xpath.value == value

    def test_basic_css(self):
        value = '.class'
        css = CSS(value)
        assert css.by == By.CSS_SELECTOR
        assert css.value == value
