from unittest import TestCase

from selenium.webdriver.common.by import By

from autoui.locator import Locator, XPath, CSS, ID
from autoui.exception import AutoUIException


class TestLocatorInit(TestCase):
    def test_basic_locator(self):
        Locator(By.ID, 'value')

    def test_basic_id_locator(self):
        id = ID('value')
        assert id.by == By.ID
        assert id.value == 'value'

    def test_basic_css_locator(self):
        css = CSS('value')
        assert css.by == By.CSS_SELECTOR
        assert css.value == 'value'

    def test_basic_xpath_locator(self):
        xpath = XPath('value')
        assert xpath.by == By.XPATH
        assert xpath.value == 'value'

    def test_invalid_by_type(self):
        with self.assertRaises(AutoUIException) as e:
            Locator(True, 'value')

    def test_invalid_value_type(self):
        with self.assertRaises(AutoUIException) as e:
            Locator('id', True)

    def test_derived_class_basic(self):
        XPath('value')

    def test_derived_class_basic_invalid_value_type(self):
        with self.assertRaises(AutoUIException) as e:
            XPath(True)

    def test_combined_init(self):
        l = Locator(ID, 'value')
        assert l.by == By.ID
        assert l.value == 'value'


class TestLocatorAttribute(TestCase):
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
