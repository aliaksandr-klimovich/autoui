import re
from unittest import TestCase

from mock import Mock

from autoui.driver import get_driver
from autoui.element.abstract import Element
from autoui.element.common import Button
from autoui.exception import AutoUIException
from autoui.find import Find
from autoui.locator import ID, XPath


class TestFind(TestCase):
    repr_name_parser = re.compile(r"<Mock .*? ?name='(.*?)' .*")

    def setUp(self):
        self.driver = Mock(name='driver')
        self.web_element = Mock(name='web_element')
        self.find_element = Mock(name='find_element', return_value=self.web_element)
        get_driver._driver = self.driver
        get_driver._driver.find_element = self.find_element

    def tearDown(self):
        get_driver._driver = None

    def test_basic(self):
        id = ID('value')

        class CustomElement(Element):
            pass

        class Page(object):
            locator = Find(CustomElement, id)

        web_element_instance = Page().locator
        assert isinstance(web_element_instance, Element)
        assert web_element_instance._element is self.web_element
        self.find_element.assert_called_once_with(id.by, id.value)

    def test_incorrect_locator_type__pass_instance(self):
        with self.assertRaises(AutoUIException) as e:
            class Page(object):
                locator = Find(Element, 'value')
        assert e.exception.message == "`locator` must be instance of class `Locator`, got `str`"

    def test_incorrect_locator_type__pass_class(self):
        with self.assertRaises(AutoUIException) as e:
            class Page(object):
                locator = Find(Element, str)
        assert e.exception.message == "`locator` must be instance of class `Locator`, got `str`"

    def test_element_is_not_class(self):
        with self.assertRaises(AutoUIException) as e:
            class Page(object):
                locator = Find(Element(), XPath('.'))
        assert e.exception.message == "`element` must be class"

    def test_pass_nothing(self):
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

    def test_button_click(self):
        class Page(object):
            locator = Find(Button, XPath('.'))

        Page.locator.click()
        assert self.web_element.click.called

    def test_default_locator(self):
        xpath = XPath('.')

        class CustomSection(object):
            locator = xpath

        class Page(object):
            custom_section = Find(CustomSection)

        custom_section = Page.custom_section
        assert isinstance(custom_section, CustomSection)
        assert custom_section._element is self.web_element
        self.find_element.assert_called_once_with(xpath.by, xpath.value)
