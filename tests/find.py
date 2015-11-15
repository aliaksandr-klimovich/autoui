import re
from unittest import TestCase

from mock import Mock, patch

from autoui.driver import get_driver
from autoui.element.abstract import Element
from autoui.element.common import Button
from autoui.exception import AutoUIException
from autoui.find import Find
from autoui.locator import ID, XPath


class TestFindInit(TestCase):
    repr_name_parser = re.compile(r"<Mock .*? ?name='(.*?)' .*")

    def setUp(self):
        # self.web_element = Mock()
        # self.driver = patch('get_driver')
        # self.driver.return_value = Mock()
        # self.driver.start()
        #
        # get_driver._driver = self.driver
        # get_driver._driver.find_element = Mock(return_value=self.web_element)

        # TODO: write correct test setup
        driver = patch('autoui.driver.get_driver')
        driver.start()
        print get_driver
        print get_driver()
        driver.stop()

    def tearDown(self):
        self.driver.stop()

    def test_basic(self):
        class Page(object):
            locator = Find(Element, ID('value'))

        web_element_instance = Page().locator
        assert isinstance(web_element_instance, Element)
        assert web_element_instance._element is self.web_element
        # assert get_driver.

    def test_incorrect_locator_type__pass_instance(self):
        with self.assertRaises(AutoUIException) as e:
            class Page(object):
                locator = Find(self.web_element, 'value')
        assert e.exception.message == "`locator` must be instance of class `Locator`, got `str`"

    def test_incorrect_locator_type__pass_class(self):
        with self.assertRaises(AutoUIException) as e:
            class Page(object):
                locator = Find(self.web_element, str)
        assert e.exception.message == "`locator` must be instance of class `Locator`, got `str`"

    def test_do_pass_nothing(self):
        with self.assertRaises(TypeError) as e:
            class Page:
                locator = Find()

    def test_without_locator(self):
        class EmptySection:
            pass

        class Page:
            empty_section = Find(EmptySection)

        empty_page_instance = Page.empty_section
        assert isinstance(empty_page_instance, EmptySection)


class TestFindElement(TestCase):
    def setUp(self):
        self.web_element = Mock()
        get_driver._driver = Mock()
        get_driver._driver.find_element = Mock(return_value=self.web_element)

    def test_button_click(self):
        class Page(object):
            locator = Find(Button, XPath('.'))

        Page.locator.click()
        assert self.web_element.click.called
