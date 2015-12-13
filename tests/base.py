from unittest import TestCase

from mock import Mock
from selenium.webdriver.remote.webelement import WebElement

from autoui.driver import get_driver
from autoui.locators import XPath


class BaseTestCase(TestCase):
    def setUp(self):
        self.xpath = XPath('.')
        self.driver = Mock(name='driver')

        self.web_element = Mock(name='web_element')
        self.web_element._spec_class = WebElement
        self.web_element_inh = Mock(name='web_element_inh')
        self.web_element_inh._spec_class = WebElement
        self.web_element_inh_2 = Mock(name='web_element_inh_2')
        self.web_element_inh_2._spec_class = WebElement
        self.web_element_inh_3 = Mock(name='web_element_inh_3')
        self.web_element_inh_3._spec_class = WebElement

        self.web_element.find_element = Mock(return_value=self.web_element_inh)
        self.web_element_inh.find_element = Mock(return_value=self.web_element_inh_2)
        self.web_element_inh_2.find_element = Mock(return_value=self.web_element_inh_3)

        get_driver._driver = self.driver
        get_driver._driver.find_element = Mock(return_value=self.web_element)
        get_driver._driver.find_elements = Mock(return_value=[self.web_element, ])

    def tearDown(self):
        get_driver._driver = None
