from unittest import TestCase
from autoui.base import BaseSection
from autoui.exception import AutoUIException


class TestBaseSection(TestCase):
    def test_declaration(self):
        class Section(BaseSection):
            pass

    def test_raises_exception_with_element(self):
        with self.assertRaises(AutoUIException):
            class Section(BaseSection):
                _element = None
