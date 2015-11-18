from unittest import TestCase

from nose.tools import eq_

from autoui.base import BaseSection
from autoui.elements.common import Input
from autoui.exceptions import AutoUIException
from autoui.find import Find


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
            el1 = Find(Input)
            el2 = Find(Input)

        eq_(Section._get_names(), ['el1', 'el2'])
