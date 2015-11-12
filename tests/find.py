from unittest import TestCase

from mock import Mock

from autoui.driver import get_driver
from autoui.exceptions import AutoUIException
from autoui.find import Find
from autoui.locators import ID, _Locator


class TestFindInit(TestCase):
    def setUp(self):
        self.web_element = Mock()
        get_driver._driver = Mock()
        get_driver._driver.find_element = Mock(return_value=self.web_element)

    def test_basic(self):
        class Page(object):
            locator = Find(self.web_element, ID('value'))

        p = Page().locator

    def test_incorrect_locator_type(self):
        with self.assertRaises(AutoUIException) as e:
            class Page(object):
                locator = Find(self.web_element, 'value')

    def test_locator_is_not_of_type_Locator(self):
        with self.assertRaises(AutoUIException) as e:
            class Page(object):
                locator = Find(self.web_element, _Locator('value'))
