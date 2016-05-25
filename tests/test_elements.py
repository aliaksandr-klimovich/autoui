from collections import OrderedDict

from mock import Mock, call
from nose.tools import eq_
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement

from autoui.elements.abstract import Element, Elements
from autoui.elements.element import VElement
from autoui.elements.simple import Input, Button
from autoui.elements.mixins import Filling
from autoui.exceptions import InvalidLocator
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
        element_instance = page.element()
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

        element_instance = Page.element()
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

        Page().custom_section.find()
        self.driver.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)
        eq_(Page().custom_section.locator, self.xpath)

    def test_incorrect_locator_type__pass_instance(self):
        with self.assertRaises(InvalidLocator) as e:
            class Page(object):
                locator = Element('value')

    def test_incorrect_locator_type__pass_class(self):
        with self.assertRaises(InvalidLocator) as e:
            class Page(object):
                locator = Element(str)

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
            class Page(object):
                locator = Element()

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
        section2.section3.find()
        self.web_element.find_element.assert_not_called()

    def test_search_with_driver__as_argument_to_element(self):
        class Section1(Element):
            pass

        class Section2(Element):
            section1 = Section1(ID('section1'), search_with_driver=True)

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
        self.web_element.find_element.assert_not_called()

    def test_search_with_driver__attribute_defined_in_parent_section(self):
        class Section1(Element):
            pass

        class Section2(Element):
            section1 = Section1(ID('section1'))
            section1.search_with_driver = True

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
        self.web_element.find_element.assert_not_called()

    def test_search_with_driver__search_continue_on_stopped_element(self):
        class Section1(Element):
            pass  # search_with_driver = False

        class Section2(Element):
            section1 = Section1(ID('section1'))
            search_with_driver = True

        class Page(object):
            section2 = Section2(ID('section2'))

        page = Page()
        section2 = page.section2()
        section1 = section2.section1()
        assert isinstance(section1, Section1)
        assert section1.web_element is self.web_element_inh
        self.driver.find_element.assert_has_calls([call('id', 'section2'), ])
        self.web_element.find_element.assert_has_calls([call('id', 'section1'), ])

    def test_inherited_fillable_elements(self):
        class Section2(Element, Filling):
            s2_el1 = Input(XPath('s2_el1'))
            s2_el2 = Input(XPath('s2_el2'))

        class Section1(Element, Filling):
            locator = XPath('section1')
            section2 = Section2(XPath('section2'))
            s1_el1 = Input(XPath('s1_el1'))

        class Page(object):
            section1 = Section1()

        # basic test
        section1 = Page().section1()
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
        ], any_order=True)

        # self.web_element_inh.get_attribute.return_value = 's1_el1_value'
        # self.web_element_inh_2.get_attribute.side_effect = ['s2_el1_value', 's2_el2_value']
        # state = section1.get_state()
        # eq_(dict_to_fill, state)
        # TODO: get rid of side_effect because the order of filling elements is not defined

    def test_stop_propagation(self):
        class Section2(Element, Filling):
            locator = XPath('section2')
            s2_el1 = Input(XPath('s2_el1'))
            s2_el2 = Input(XPath('s2_el2'))

        class Section1(Element, Filling):
            locator = XPath('section1')
            stop_propagation = True
            section2 = Section2()
            s1_el1 = Input(XPath('s1_el1'))

        class Page:
            section1 = Section1()

        section1 = Page().section1()
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

    # def test_replace_web_element_of_instance_at_runtime(self):
    #     class Section(Element):
    #         element = Element(ID('1'))
    #
    #     class Page(object):
    #         section = Section(ID('2'))
    #
    #     page = Page()
    #     section = page.section.find()
    #     section.web_element = 1
    #     # `section.web_element = None` will give no effect because of parent realization
    #     # (https://github.com/alex-klimovich/autoui/issues/21)
    #     with self.assertRaises(AttributeError):
    #         with catch_warnings(record=True) as w:
    #             section.element.find()
    #
    #     assert issubclass(w[-1].category, InvalidWebElementInstance)
    #     eq_(str(w[-1].message), '`web_element` not subclasses `WebElement` in `Section` object at runtime')

    def test_search_with_driver_must_be_of_bool_type(self):
        class Section(Element):
            search_with_driver = None
        with self.assertRaises(TypeError) as e:
            class Page(object):
                section = Section(XPath(''))

    def test_stale_element_exception(self):
        web_element_1 = Mock(return_value=self.web_element_inh, name='web_element_1', spec=WebElement)
        web_element_2 = Mock(return_value=self.web_element_inh, name='web_element_2', spec=WebElement)

        self.web_element.find_element.side_effect = [
            web_element_1,
            StaleElementReferenceException(),
            web_element_2]

        class Section(Element):
            locator = XPath('section_locator')
            element = Element(XPath('element_locator'))

            def test_element(self):
                el1 = self.element()
                eq_(el1.web_element, web_element_1)
                el2 = self.element()
                eq_(el2.web_element, web_element_2)

        class Page(object):
            section = Section()

        Page().section().test_element()

    # def test_instance_creation_in_runtime__not_instance(self):
    #     class ParentElement(Element):
    #         locator = XPath('.')
    #
    #     class ChildElement(Element):
    #         locator = XPath('.')
    #
    #     with self.assertRaises(AssertionError) as err:
    #         child_element = ChildElement(parent=ParentElement)
    #     assert err.exception.message == '`parent` should be instance'

    # def test_instance_creation_in_runtime__not_instance_of_Element(self):
    #     class ParentElement(object):
    #         pass
    #
    #     class ChildElement(Element):
    #         locator = XPath('.')
    #
    #     with self.assertRaises(AssertionError) as err:
    #         child_element = ChildElement(parent=ParentElement())
    #     assert err.exception.message == '`parent` should be instance of Element(s) class'

    def test_instance_creation_at_runtime(self):
        class ParentElement(Element):
            locator = ID('ParentElement')

        class ChildElement(Element):
            locator = ID('ChildElement')

        parent_element = ParentElement()
        # without finding parent
        child_element = ChildElement(parent=parent_element)
        child_element()
        assert parent_element.web_element is None
        assert child_element.web_element is self.web_element
        assert child_element._instance is parent_element
        assert child_element._owner is ParentElement
        self.driver.find_element.assert_called_once_with(*ID('ChildElement').get())
        self.web_element.assert_not_called()

        parent_element.find()
        child_element.find()
        assert parent_element.web_element is self.web_element
        assert child_element.web_element is self.web_element_inh
        assert child_element._instance is parent_element
        assert child_element._owner is ParentElement
        self.web_element.find_element.assert_called_once_with(*ID('ChildElement').get())

    def test_velement(self):
        class ChildElement(VElement):
            locator = ID('ChildElement')

        class ParentElement(VElement):
            locator = ID('ParentElement')
            child_element = ChildElement()

        # parent_element = ParentElement()()
        # child_element = parent_element.child_element()
        # todo: implement visibility change for quick testing


class TestElements(BaseTestCase):
    def test_declaration(self):
        class Sections(Elements):
            locator = ID('1')

        class Page(object):
            sections = Sections()

    def test_page_with_custom_elements(self):
        class Buttons(Elements):
            locator = ID('1')
            base_class = Button

        class Page(object):
            buttons = Buttons()

        page = Page()
        s = page.buttons()
        eq_(s.elements, [self.web_element, ])
        assert isinstance(s.elements[0], Button)
        assert isinstance(s, Buttons)
        self.driver.find_elements.assert_called_once_with(*ID('1').get())


class TestMixins(BaseTestCase):
    def setUp(self):
        super(TestMixins, self).setUp()

        class Mixin1(object):
            test_mixin_1 = None

        class Mixin2(object):
            test_mixin_2 = None

        self.Mixin1 = Mixin1
        self.Mixin2 = Mixin2

    def test_mixins_are_class_bases(self):
        # python way =)
        class Section(self.Mixin1, self.Mixin2, Element):
            pass

        class Page(object):
            section = Section(ID('1'))

        element_instance = Page().section()
        assert element_instance.web_element is self.web_element
        assert hasattr(element_instance, 'test_mixin_1')
        assert hasattr(element_instance, 'test_mixin_2')
