from unittest import TestCase
from warnings import catch_warnings

from mock import Mock, call
from nose.tools import eq_
from selenium.common.exceptions import StaleElementReferenceException

from autoui.elements.abstract import Element
from autoui.elements.implemented import Input
from autoui.exceptions import InvalidLocator, InvalidWebElementInstance
from autoui.locators import XPath, ID
from tests.base import BaseTestCase


class TestElement(BaseTestCase):
    def test_declaration(self):
        class CustomElement(Element):
            element = Element(ID('1'))

        class Section(Element):
            element = Element(ID('2'))
            custom_element = CustomElement(ID('3'))

        class Page(object):
            section = Section(ID('4'))
            element = Element(ID('5'))
            custom_element = CustomElement(ID('6'))

    def test_find(self):
        class Page(object):
            element = Element(self.xpath)

        page = Page()
        element_instance = page.element.find()
        assert isinstance(element_instance, Element)
        assert element_instance.web_element is self.web_element
        assert element_instance._instance is page
        assert element_instance._owner is Page
        assert element_instance.locator is self.xpath
        assert element_instance.search_with_driver is False
        self.driver.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

    def test_find__no_instance(self):
        class Page(object):
            element = Element(self.xpath)

        element_instance = Page.element.find()
        assert isinstance(element_instance, Element)
        assert element_instance.web_element is self.web_element
        assert element_instance._instance is None
        assert element_instance._owner is Page
        assert element_instance.locator is self.xpath
        assert element_instance.search_with_driver is False
        self.driver.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

    def test_call(self):
        class Page(object):
            element = Element(self.xpath)

        page = Page()
        element_instance = page.element()
        assert isinstance(element_instance, Element)
        assert element_instance.web_element is self.web_element
        assert element_instance._instance is page
        assert element_instance._owner is Page
        assert element_instance.locator is self.xpath
        assert element_instance.search_with_driver is False
        self.driver.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

    def test_default_locator(self):
        class CustomSection(Element):
            locator = self.xpath

        class Page(object):
            custom_section = CustomSection()

        Page().custom_section()
        self.driver.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

    def test_incorrect_locator_type__pass_instance(self):
        with self.assertRaises(InvalidLocator) as e:
            class Page(object):
                locator = Element('value')
        eq_(e.exception.message, '`locator` must be instance of class `Locator`, got `str`')

    def test_incorrect_locator_type__pass_class(self):
        with self.assertRaises(InvalidLocator) as e:
            class Page(object):
                locator = Element(str)
        eq_(e.exception.message, '`locator` must be instance of class `Locator`, got `str`')

    def test_from_2_locators_first_of_instance_is_used(self):
        class Section(Element):
            locator = XPath('1')

        class Page(object):
            section = Section(XPath('2'))

        page = Page()
        section = page.section
        eq_(section.locator.value, '2')

    def test_pass_nothing(self):
        with self.assertRaises(InvalidLocator) as e:
            class Page:
                locator = Element()

        eq_(e.exception.message, '`locator` must be instance of class `Locator`, got `NoneType`')

    def test_search_with_driver__as_class_property(self):
        class Section1(Element):
            search_with_driver = True

        class Section3(Section1):
            pass

        class Section2(Element):
            section1 = Section1(ID('section1'))
            section3 = Section3(ID('section3'))

        class Page(object):
            section2 = Section2(ID('section2'))

        page = Page()
        section2 = page.section2()
        section1 = section2.section1()
        assert isinstance(section1, Section1)
        assert section1.web_element is self.web_element
        self.driver.find_element.assert_has_calls([
            call('id', 'section2'),
            call('id', 'section1'),
        ])
        section2.section3()
        self.web_element.find_element.assert_not_called()

# ------------------------------------------

    def test_search_with_driver__as_argument_to_element(self):
        class Section1(Element):
            pass

        class Section2(Element):
            section1 = Section1(XPath('section1'), search_with_driver=True)

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

    def test_search_with_driver__attribute_defined_in_parent_section(self):
        class Section1(Element):
            pass

        class Section2(Element):
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

    def test_search_with_driver__search_continue_on_stopped_element(self):
        class Section1(Element):
            pass  # search_with_driver = False

        class Section2(Element):
            section1 = Section1(XPath('section1'))
            search_with_driver = True

        class Page(object):
            section2 = Section2(XPath('section2'))

        section1 = Page.section2.section1
        assert isinstance(section1, Section1)
        assert section1.web_element is self.web_element_inh
        self.driver.find_element.assert_has_calls([call('xpath', 'section2'), ])
        self.web_element.find_element.assert_has_calls([call('xpath', 'section1'), ])

    def test_search_with_driver__non_element_instances_will_use_driver(self):
        class Page(object):
            e = Element(XPath(''))

        s = Page()
        e = s.e

        m = Mock()
        e.__get__(m, Mock)
        assert e.web_element is self.web_element

    def test_not_permitted_attribute(self):
        with self.assertRaises(AttributeNotPermitted):
            class Section(Element):
                web_element = None

    def test_not_permitted_attribute_from_elements_not_affected(self):
        class Section(Element):
            web_elements = None

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

    def test_replace_web_element_of_instance_at_runtime(self):
        class Section(Element):
            element = Element(XPath('1'))

        class Page(object):
            section = Section(XPath('2'))

        page = Page()
        section = page.section
        section.web_element = None
        with catch_warnings(record=True) as w:
            e = section.element

        assert issubclass(w[-1].category, InvalidWebElementInstance)
        eq_(str(w[-1].message), '`web_element` instance not subclasses `WebElement` in `Section` object at runtime')

    def test_search_with_driver_must_be_of_bool_type(self):
        class Section(Element):
            search_with_driver = None

        class Page(object):
            section = Section(XPath(''))

        with self.assertRaises(TypeError) as e:
            s = Page.section

        eq_(e.exception.message, '`search_with_driver` must be of `bool` type, got `NoneType`')

    def test_stale_element_exception(self):
        web_element_1 = Mock(return_value=self.web_element_inh, name='web_element_1')
        web_element_2 = Mock(return_value=self.web_element_inh, name='web_element_2')

        self.web_element.find_element.side_effect = [
            web_element_1,
            StaleElementReferenceException(),
            web_element_2]

        class Section(Element):
            locator = XPath('section_locator')
            element = Element(XPath('element_locator'))

            def test_element(self):
                el1 = self.element
                eq_(el1.web_element, web_element_1)
                el2 = self.element
                eq_(el2.web_element, web_element_2)

        class Page(object):
            section = Section()

        page = Page()
        page.section.test_element()


class TestElements(BaseTestCase):
    def test_declaration(self):
        class Sections(Elements):
            pass

        sections = Sections(XPath(''))

    def test_page_with_custom_elements(self):
        l = XPath('.')

        class Sections(Elements):
            pass

        class Page(object):
            sections = Sections(l)

        page = Page()
        s = page.sections
        eq_(s.web_elements, [self.web_element, ])
        self.driver.find_elements.assert_called_once_with(l.by, l.value)

    def test_not_permitted_attribute(self):
        with self.assertRaises(AttributeNotPermitted):
            class Section(Elements):
                web_elements = None

    def test_not_permitted_attribute_from_element_not_affected(self):
        class Section(Elements):
            web_element = None

    def test_finding_elements_with_elements(self):
        class InnerStructure(Elements):
            pass

        class OuterStructure(Elements):
            inner_structure = InnerStructure(XPath(''))

        class Page(object):
            outer_structure = OuterStructure(XPath(''))

        # override _get_finder method ?
        # won't fix, it is normal thing that i can find elements only with single element
        # and if i want to find elements with elements i should implement
        # this feature by myself in custom elements
        page = Page()
        with catch_warnings(record=True) as w:
            s = page.outer_structure.inner_structure

        assert issubclass(w[-1].category, InvalidWebElementInstance)


class TestCustomElements(BaseTestCase):
    pass


class TestAbstract(TestCase):
    pass


class TestElementV3(BaseTestCase):
    def test_find(self):
        class Mixin1(object):
            def some_method(self):
                print 'hello from Mixin1'

        class Mixin2(object):
            pass

        class Page(object):
            element = Element(ID('1'), mixins=(Mixin1, Mixin2))
        element_instance = Page().element.find()
        assert element_instance.web_element is self.web_element
        element_instance.some_method()
