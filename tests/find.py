import re
from unittest import TestCase

from mock import Mock
from nose.tools import eq_

from autoui.base import BaseSection, FillableSection
from autoui.driver import get_driver
from autoui.elements.abstract import Element
from autoui.elements.common import Button, Input
from autoui.exceptions import AutoUIException
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

    def test_default_locator(self):
        class CustomSection(object):
            locator = self.xpath

        class Page(object):
            custom_section = Find(CustomSection)

        custom_section = Page.custom_section
        assert isinstance(custom_section, CustomSection)
        assert custom_section._element is self.web_element
        self.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

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

    def test_section_fill(self):
        class Section(FillableSection):
            el1 = Find(Input, XPath('xpath_1'))
            el2 = Find(Input, XPath('xpath_2'))

        class Page(BaseSection):
            section = Find(Section)

        Page.section.fill({'el1': 'some text'})
        self.find_element.assert_called_with('xpath', 'xpath_1')
        assert self.web_element.clear.called
        self.web_element.send_keys.assert_called_with('some text')
        
        Section().fill({'el2': 'some another text'})
        self.find_element.assert_called_with('xpath', 'xpath_2')
        assert self.web_element.clear.called
        self.web_element.send_keys.assert_called_with('some another text')

    def test_init_args_and_kwargs(self):
        class Section:
            def __init__(self, arg):
                self.arg = arg
        
        class Page:
            section = Find(Section, args=('value',))
        
        section = Page.section
        eq_(section.arg, 'value')
        assert isinstance(section, Section)

    def test_element_without_locator(self):
        with self.assertRaises(AutoUIException) as e:
            class A:
                button = Find(Button)

        eq_(e.exception.message, 'If element is subclass of `Element`, locator must be present')
