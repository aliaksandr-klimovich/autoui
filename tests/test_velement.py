from autoui.base_page import BasePage
from autoui.driver import get_driver
from autoui.elements.simple import Input, Button
from autoui.locators import ID
from autoui.locators import XPath
from tests.base import BaseTestCaseWithServer
from tests.test_app.web_server import base_url


class TestWaiters(BaseTestCaseWithServer):
    url = base_url + '/waiters'

    @classmethod
    def setUpClass(cls):
        super(TestWaiters, cls).setUpClass()
        get_driver().get(cls.url)

    @classmethod
    def tearDownClass(cls):
        super(TestWaiters, cls).tearDownClass()
        get_driver().quit()

    def setUp(self):
        get_driver().refresh()

    def test_01(self):
        pass