from unittest import TestCase

from mock import Mock, call

from nose.tools import eq_

from autoui.base import BaseSection
from autoui.driver import get_driver
from autoui.elements.abstract import Element
from autoui.exceptions import InvalidLocatorException
from autoui.locators import XPath


class TestElement(TestCase):
    def setUp(self):
        self.xpath = XPath('.')
        self.driver = Mock(name='driver')

        self.web_element = Mock(name='web_element')
        self.web_element_inh = Mock(name='web_element_inh')
        self.web_element_inh_2 = Mock(name='web_element_inh_2')
        self.web_element_inh_3 = Mock(name='web_element_inh_3')

        self.web_element.find_element = Mock(return_value=self.web_element_inh)
        self.web_element_inh.find_element = Mock(return_value=self.web_element_inh_2)
        self.web_element_inh_2.find_element = Mock(return_value=self.web_element_inh_3)

        get_driver._driver = self.driver
        get_driver._driver.find_element = Mock(return_value=self.web_element)

    def tearDown(self):
        get_driver._driver = None

    def test_basic(self):
        class CustomElement(Element):
            pass

        class Page(object):
            locator = CustomElement(self.xpath)

        element_instance = Page().locator
        assert isinstance(element_instance, Element)
        assert element_instance.web_element is self.web_element
        self.driver.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

    def test_incorrect_locator_type__pass_instance(self):
        with self.assertRaises(InvalidLocatorException) as e:
            class Page(object):
                locator = Element('value')
        eq_(e.exception.message, "`locator` must be instance of class `Locator`, got `str`")

    def test_incorrect_locator_type__pass_class(self):
        with self.assertRaises(InvalidLocatorException) as e:
            class Page(object):
                locator = Element('value')
        eq_(e.exception.message, "`locator` must be instance of class `Locator`, got `str`")

    def test_pass_nothing(self):
        with self.assertRaises(InvalidLocatorException) as e:
            class Page:
                locator = Element()

        eq_(e.exception.message, "`locator` must be instance of class `Locator`, got `NoneType`")

    def test_default_locator(self):
        class CustomSection(Element):
            locator = self.xpath

        class Page(object):
            custom_section = CustomSection()

        custom_section = Page.custom_section
        assert isinstance(custom_section, CustomSection)
        assert custom_section.web_element is self.web_element
        self.driver.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

    def test_search_with_driver(self):
        class Section1(BaseSection):
            search_with_driver = True

        class Section2(BaseSection):
            section1 = Section1(XPath('section1'))

        class Page(object):
            section2 = Section2(XPath('section2'))

        section1_instance = Page.section2.section1
        assert isinstance(section1_instance, Section1)
        assert section1_instance.web_element is self.web_element
        self.driver.find_element.assert_has_calls([
            call('xpath', 'section2'),
            call('xpath', 'section1'),
        ])
        self.web_element.find_element.assert_not_called()

    def test_search_with_driver2(self):
        class Section1(BaseSection):
            pass

        class Section2(BaseSection):
            section1 = Section1(XPath('section1'))
            section1.search_with_driver = True

        class Page(object):
            section2 = Section2(XPath('section2'))

        section1_instance = Page.section2.section1
        assert isinstance(section1_instance, Section1)
        assert section1_instance.web_element is self.web_element
        self.driver.find_element.assert_has_calls([
            call('xpath', 'section2'),
            call('xpath', 'section1'),
        ])
        self.web_element.find_element.assert_not_called()
