import re
import warnings
from unittest import TestCase

from mock import Mock
from nose.tools import eq_

from autoui.base import BaseSection
from autoui.driver import get_driver
from autoui.elements.abstract import Element
from autoui.elements.common import Button
from autoui.exceptions import AutoUIException, AutoUIWarning
from autoui.find import Find
from autoui.locators import XPath


class TestFind(TestCase):
    repr_name_parser = re.compile(r"<Mock .*? ?name='(.*?)' .*")

    def setUp(self):
        self.xpath = XPath('.')
        self.driver = Mock(name='driver')
        self.web_element = Mock(name='web_element')
        self.find_element = Mock(name='find_element', return_value=self.web_element)
        get_driver._driver = self.driver
        get_driver._driver.find_element = self.find_element

    def tearDown(self):
        get_driver._driver = None

    def test_basic(self):
        class CustomElement(Element):
            pass

        class Page(object):
            locator = Find(CustomElement, self.xpath)

        web_element_instance = Page().locator
        assert isinstance(web_element_instance, Element)
        assert web_element_instance._element is self.web_element
        self.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

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
                locator = Find(Element(), self.xpath)
        assert e.exception.message == "`element` must be class"

    def test_pass_nothing(self):
        with self.assertRaises(TypeError):
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
            locator = Find(Button, self.xpath)

        Page.locator.click()
        assert self.web_element.click.called

    def test_default_locator(self):
        class CustomSection(object):
            locator = self.xpath

        class Page(object):
            custom_section = Find(CustomSection)

        custom_section = Page.custom_section
        assert isinstance(custom_section, CustomSection)
        assert custom_section._element is self.web_element
        self.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

    def test_linked_name(self):
        class Page(object):
            custom_section = Find(Element, self.xpath, name='custom_section_name')

        web_element_instance = Page.custom_section
        eq_(web_element_instance._name, 'custom_section_name')
        assert isinstance(web_element_instance, Element)
        self.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

    def test_linked_name_with_non_element_class(self):
        class VeryCustomElement(object):
            pass

        class Page(object):
            custom_section = Find(VeryCustomElement, name='custom_section_name')

        with self.assertRaises(AttributeError):
            with warnings.catch_warnings(record=True) as w:
                Page.custom_section._name
        assert issubclass(w[0].category, AutoUIWarning)
        self.web_element.assert_not_called()
        self.find_element.assert_not_called()

    def test_search_with_driver(self):
        class Section1(BaseSection):
            search_with_driver = True

        class Section2(BaseSection):
            section_1 = Find(Section1, self.xpath)

        class Page(object):
            section = Find(Section2, self.xpath)

        section_1_instance = Page.section.section_1
        assert isinstance(section_1_instance, Section1)
        self.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)
