from unittest import TestCase

from mock import Mock, call
from nose.tools import eq_

from autoui.base import BaseSection, FillableSection
from autoui.driver import get_driver
from autoui.elements.abstract import Element
from autoui.elements.common import Button, Input
from autoui.exceptions import AutoUIException
from autoui.find import Find
from autoui.locators import XPath


class TestFind(TestCase):
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
        # Basic test to assure that very simple structure works

        class CustomElement(Element):
            pass

        class Page(object):
            locator = Find(CustomElement, self.xpath)

        web_element_instance = Page().locator
        assert isinstance(web_element_instance, Element)
        assert web_element_instance._element is self.web_element
        self.driver.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

    def test_incorrect_locator_type__pass_instance(self):
        with self.assertRaises(AutoUIException) as e:
            class Page(object):
                locator = Find(Element, 'value')
        eq_(e.exception.message, "`locator` must be instance of class `Locator`, got `str`")

    def test_incorrect_locator_type__pass_class(self):
        with self.assertRaises(AutoUIException) as e:
            class Page(object):
                locator = Find(Element, str)
        eq_(e.exception.message, "`locator` must be instance of class `Locator`, got `str`")

    def test_element_is_not_class(self):
        with self.assertRaises(AutoUIException) as e:
            class Page(object):
                locator = Find(Element(), self.xpath)
        eq_(e.exception.message, "`element` must be class")

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
        self.driver.assert_not_called()

    def test_default_locator(self):
        class CustomSection(object):
            locator = self.xpath

        class Page(object):
            custom_section = Find(CustomSection)

        custom_section = Page.custom_section
        assert isinstance(custom_section, CustomSection)
        assert custom_section._element is self.web_element
        self.driver.find_element.assert_called_once_with(self.xpath.by, self.xpath.value)

    def test_search_with_driver(self):
        class Section1(BaseSection):
            search_with_driver = True

        class Section2(BaseSection):
            section1 = Find(Section1, XPath('section1'))

        class Page(object):
            section2 = Find(Section2, XPath('section2'))

        section1_instance = Page.section2.section1
        assert isinstance(section1_instance, Section1)
        assert section1_instance._element is self.web_element
        self.driver.find_element.assert_has_calls([
            call('xpath', 'section2'),
            call('xpath', 'section1'),
        ])
        self.web_element.find_element.assert_not_called()

    def test_section_fill(self):
        class Section(FillableSection):
            el1 = Find(Input, XPath('xpath_1'))
            el2 = Find(Input, XPath('xpath_2'))

        class Page(BaseSection):
            section = Find(Section)

        Page.section.fill({'el1': 'some text'})
        self.driver.find_element.assert_called_once_with('xpath', 'xpath_1')
        assert self.web_element.clear.called
        self.web_element.send_keys.assert_called_once_with('some text')

        Section().fill({'el2': 'some another text'})
        self.driver.find_element.assert_called_with('xpath', 'xpath_2')
        assert self.web_element.clear.called
        self.web_element.send_keys.assert_called_with('some another text')

    def test_init_args_and_kwargs(self):
        class Section:
            def __init__(self, arg, key=None):
                self.arg = arg

        class Page:
            section = Find(Section, args=['value'], kwargs={'key': 'value'})

        section = Page.section
        eq_(Page.__dict__['section'].args, ['value'], )
        eq_(Page.__dict__['section'].kwargs, {'key': 'value'})
        eq_(section.arg, 'value')
        assert isinstance(section, Section)

    def test_element_without_locator(self):
        with self.assertRaises(AutoUIException) as e:
            class A:
                button = Find(Button)

        eq_(e.exception.message, 'If element is subclass of `Element`, locator must be present')

    def test_inherited_fillable_sections(self):
        # prepare

        class Section2(FillableSection):
            s2_el1 = Find(Input, XPath('s2_el1'))
            s2_el2 = Find(Input, XPath('s2_el2'))

            def __init__(self, a, b=None):
                pass

        class Section1(FillableSection):
            locator = XPath('section1')
            section2 = Find(Section2, args=[1], kwargs={'b': 2}, locator=XPath('section2'))
            s1_el1 = Find(Input, XPath('s1_el1'))

        class Page:
            section1 = Find(Section1)

        section1 = Page.section1
        assert isinstance(section1, Section1)
        assert section1._element is self.web_element

        section1.fill({
            's1_el1': 's1_el1_value',
            'section2': {
                's2_el1': 's2_el1_value',
                's2_el2': 's2_el2_value',
            }
        })

        self.driver.find_element.assert_has_calls([call('xpath', 'section1')])

        self.web_element.find_element.assert_has_calls([
            call('xpath', 's1_el1'),
            call('xpath', 'section2')
        ], any_order=True)

        self.web_element_inh.assert_has_calls([
            call.clear(),
            call.send_keys('s1_el1_value'),
        ])

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

    def test_stop_propagation(self):
        class Section2(FillableSection):
            locator = XPath('section2')
            s2_el1 = Find(Input, XPath('s2_el1'))
            s2_el2 = Find(Input, XPath('s2_el2'))

        class Section1(FillableSection):
            locator = XPath('section1')
            stop_propagation = True
            section2 = Find(Section2)
            s1_el1 = Find(Input, XPath('s1_el1'))

        class Page:
            section1 = Find(Section1)

        section1 = Page.section1
        assert isinstance(section1, Section1)

        section1.fill({
            's1_el1': 's1_el1_value',
            'section2': {
                's2_el1': 's2_el1_value',
                's2_el2': 's2_el2_value',
            }
        })

        self.driver.find_element.assert_has_calls([call('xpath', 'section1')])

        self.web_element.find_element.assert_has_calls([
            call('xpath', 's1_el1'),
        ])

        self.web_element_inh.assert_has_calls([
            call.clear(),
            call.send_keys('s1_el1_value')
        ])

        self.web_element_inh.find_element.assert_not_called()
