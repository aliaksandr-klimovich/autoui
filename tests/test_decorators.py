from unittest import skip

from mock import Mock, call
from nose.tools import eq_
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from autoui.decorators.abstract import fillable
from autoui.decorators.common import *
from autoui.driver import get_driver
from autoui.elements.abstract import Element
from autoui.elements.common import Input
from autoui.locators import XPath
from tests.base import BaseTestCase


class TestUntil(BaseTestCase):
    def setUp(self):
        super(TestUntil, self).setUp()

        # do not forget that raises `StopIteration` on third pass
        get_driver._driver.find_element = Mock(side_effect=[NoSuchElementException(), self.web_element])

    def tearDown(self):
        super(TestUntil, self).tearDown()

    def test_until_presence_of_element_located(self):
        class Page(object):
            element = Element(XPath('.//'), (until_presence_of_element_located(0.1, 0.2), ))

        p = Page()
        with self.assertRaises(TimeoutException):
            p.element

        class Page(object):
            element = Element(XPath('.//'), (until_presence_of_element_located(0.2, 0.1), ))

        p = Page()
        e = p.element
        assert e.web_element is self.web_element

    def test_until_visibility_of_element_located(self):
        self.web_element.is_displayed.return_value = True

        class Page(object):
            element = Element(XPath('.//'), (until_visibility_of_element_located(0.1, 0.2), ))

        p = Page()
        with self.assertRaises(TimeoutException):
            p.element

        class Page(object):
            element = Element(XPath('.//'), (until_visibility_of_element_located(0.2, 0.1), ))

        p = Page()
        e = p.element
        assert e.web_element is self.web_element

    def test_until_invisibility_of_element_located(self):
        # prepare
        self.web_element.is_displayed.return_value = True
        get_driver._driver.find_element = Mock(side_effect=[self.web_element])

        # test
        class Page(object):
            element = Element(XPath('.//'), (until_invisibility_of_element_located(0.1, 0.2), ))

        p = Page()
        with self.assertRaises(TimeoutException):
            p.element

        # prepare
        self.web_element.is_displayed.return_value = False
        get_driver._driver.find_element = Mock(side_effect=[self.web_element])

        # test
        class Page(object):
            element = Element(XPath('.//'), (until_invisibility_of_element_located(0.2, 0.1), ))

        p = Page()
        e = p.element
        assert e.web_element is self.web_element


class TestFillableDecorator(BaseTestCase):
    # same as in `Element` test
    # but with decorator `fillable`
    def test_inherited_fillable_elements(self):
        @fillable
        class Section2(Element):
            s2_el1 = Input(XPath('s2_el1'))
            s2_el2 = Input(XPath('s2_el2'))

        @fillable
        class Section1(Element):
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
