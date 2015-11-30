from unittest import TestCase

from mock import Mock, call
from nose.tools import eq_

from autoui.driver import get_driver
from autoui.elements.abstract import Element, Elements, Fillable
from autoui.elements.common import Input
from autoui.exceptions import InvalidLocatorException, AttributeNotPermittedException
from autoui.locators import XPath


class BaseTestCase(TestCase):
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


class TestElement(BaseTestCase):
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
        eq_(e.exception.message, '`locator` must be instance of class `Locator`, got `str`')

    def test_incorrect_locator_type__pass_class(self):
        with self.assertRaises(InvalidLocatorException) as e:
            class Page(object):
                locator = Element('value')
        eq_(e.exception.message, '`locator` must be instance of class `Locator`, got `str`')

    def test_pass_nothing(self):
        with self.assertRaises(InvalidLocatorException) as e:
            class Page:
                locator = Element()

        eq_(e.exception.message, '`locator` must be instance of class `Locator`, got `NoneType`')

    def test_default_locator(self):
        class CustomSection(Element):
            locator = self.xpath

        class Page(object):
            custom_section = CustomSection()

        custom_section = Page.custom_section
        assert isinstance(custom_section, CustomSection)
        assert custom_section.web_element is self.web_element
        self.driver.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

    # def test_search_with_driver(self):
    #     class Section1(BaseSection):
    #         search_with_driver = True
    #
    #     class Section2(BaseSection):
    #         section1 = Section1(XPath('section1'))
    #
    #     class Page(object):
    #         section2 = Section2(XPath('section2'))
    #
    #     section1_instance = Page.section2.section1
    #     assert isinstance(section1_instance, Section1)
    #     assert section1_instance.web_element is self.web_element
    #     self.driver.find_element.assert_has_calls([
    #         call('xpath', 'section2'),
    #         call('xpath', 'section1'),
    #     ])
    #     self.web_element.find_element.assert_not_called()
    #
    # def test_search_with_driver2(self):
    #     class Section1(BaseSection):
    #         pass
    #
    #     class Section2(BaseSection):
    #         section1 = Section1(XPath('section1'))
    #         section1.search_with_driver = True
    #
    #     class Page(object):
    #         section2 = Section2(XPath('section2'))
    #
    #     section1_instance = Page.section2.section1
    #     assert isinstance(section1_instance, Section1)
    #     assert section1_instance.web_element is self.web_element
    #     self.driver.find_element.assert_has_calls([
    #         call('xpath', 'section2'),
    #         call('xpath', 'section1'),
    #     ])
    #     self.web_element.find_element.assert_not_called()

    def test_not_permitted_attribute(self):
        with self.assertRaises(AttributeNotPermittedException):
            class Section(Element):
                web_element = None

    def test_inherited_fillable_elements(self):
        class Section2(Element, Fillable):
            s2_el1 = Input(XPath('s2_el1'))
            s2_el2 = Input(XPath('s2_el2'))

        class Section1(Element, Fillable):
            locator = XPath('section1')
            section2 = Section2(XPath('section2'))
            s1_el1 = Input(XPath('s1_el1'))

        class Page(object):
            section1 = Section1()

        # basic test
        section1 = Page.section1
        assert isinstance(section1, Section1)
        assert section1.web_element is self.web_element

        dict_to_fill = {
            's1_el1': 's1_el1_value',
            'section2': {
                's2_el1': 's2_el1_value',
                's2_el2': 's2_el2_value',
            }
        }
        section1.fill(dict_to_fill)

        # section1 must be found with driver
        self.driver.find_element.assert_has_calls([call('xpath', 'section1')])

        # section2 and items of section1 must be found with web element of section1
        self.web_element.find_element.assert_has_calls([
            call('xpath', 's1_el1'),
            call('xpath', 'section2')
        ], any_order=True)

        self.web_element_inh.assert_has_calls([
            call.clear(),
            call.send_keys('s1_el1_value'),
        ])

        # items of section2 must be found with web element of section2
        self.web_element_inh.find_element.assert_has_calls([
            call('xpath', 's2_el1'),
            call('xpath', 's2_el2'),
        ], any_order=True)

        self.web_element_inh_2.assert_has_calls([
            call.clear(),
            call.send_keys('s2_el1_value'),
            call.clear(),
            call.send_keys('s2_el2_value')
        ])

        self.web_element_inh.get_attribute.return_value = 's1_el1_value'
        self.web_element_inh_2.get_attribute.side_effect = ['s2_el1_value', 's2_el2_value']

        state = section1.get_state()
        eq_(dict_to_fill, state)

    def test_stop_propagation(self):
        class Section2(Element, Fillable):
            locator = XPath('section2')
            s2_el1 = Input(XPath('s2_el1'))
            s2_el2 = Input(XPath('s2_el2'))

        class Section1(Element, Fillable):
            locator = XPath('section1')
            stop_propagation = True
            section2 = Section2()
            s1_el1 = Input(XPath('s1_el1'))

        class Page:
            section1 = Section1()

        section1 = Page.section1
        assert isinstance(section1, Section1)

        dict_to_fill = {
            's1_el1': 's1_el1_value',
            'section2': {
                's2_el1': 's2_el1_value',
                's2_el2': 's2_el2_value',
            }
        }

        section1.fill(dict_to_fill)

        self.driver.find_element.assert_has_calls([call('xpath', 'section1')])

        self.web_element.find_element.assert_has_calls([
            call('xpath', 's1_el1'),
        ])

        self.web_element_inh.assert_has_calls([
            call.clear(),
            call.send_keys('s1_el1_value')
        ])

        self.web_element_inh.find_element.assert_not_called()

        self.web_element_inh.get_attribute.return_value = 's1_el1_value'
        self.web_element_inh_2.get_attribute.side_effect = ['s2_el1_value', 's2_el2_value']

        state = section1.get_state()

        result_dict = {'s1_el1': 's1_el1_value'}
        eq_(result_dict, state)


class TestElements(BaseTestCase):
    def test_not_permitted_attribute(self):
        with self.assertRaises(AttributeNotPermittedException):
            class Section(Elements):
                web_elements = None
