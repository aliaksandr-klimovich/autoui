from mock import Mock
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from autoui.decorators.common import until_presence_of_element_located
from autoui.driver import get_driver
from autoui.elements.abstract import Element
from autoui.locators import XPath
from tests.base import BaseTestCase


class TestDecorators(BaseTestCase):
    def setUp(self):
        super(TestDecorators, self).setUp()
        get_driver._driver.find_element = Mock(side_effect=[NoSuchElementException(), self.web_element])

    def tearDown(self):
        super(TestDecorators, self).tearDown()

    def test_until(self):
        class Page(object):
            element = Element(XPath('.//'), (until_presence_of_element_located(0.1), ))

        p = Page()
        with self.assertRaises(TimeoutException):
            p.element

        class Page(object):
            element = Element(XPath('.//'), (until_presence_of_element_located(0.7), ))

        p = Page()
        e = p.element
        assert e.web_element is self.web_element
