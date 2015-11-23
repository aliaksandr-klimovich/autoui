from unittest import TestCase

from nose.tools import eq_

from autoui.base import BaseSection
from autoui.elements.common import Input
from autoui.exceptions import AutoUIException
from autoui.find import Find
from autoui.locators import XPath


class TestBaseSection(TestCase):
    def test_declaration(self):
        class Section(BaseSection):
            pass

    def test_raises_exception_with_element(self):
        with self.assertRaises(AutoUIException):
            class Section(BaseSection):
                _element = None

    def test_get_names(self):
        class Section(BaseSection):
            el1 = Find(Input, XPath('.'))
            el2 = Find(Input, XPath('.'))

        eq_(Section._get_names(), ['el2', 'el1'])
        eq_(Section._names, ['el1', 'el2'])

    def test_search_with_driver_not_bool(self):
        with self.assertRaises(AutoUIException) as e:
            class Section(BaseSection):
                search_with_driver = 'True'
        eq_(e.exception.message, '`search_with_driver` class attribute must be of `bool` type')
