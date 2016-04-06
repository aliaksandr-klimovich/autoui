from nose.tools import eq_
from selenium.common.exceptions import TimeoutException

from autoui.base_page import BasePage
from autoui.driver import get_driver
from autoui.elements.simple import Button
from autoui.locators import ID
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

    def test_wait_until_visible_and_invisible(self):
        class Page(object):
            url = self.url
            button1 = Button(ID('b-01'))
            button2 = Button(ID('b-02'))

        page = Page()

        button1 = page.button1
        button1.find().click()

        button2 = page.button2
        button2.wait_until_visible()
        eq_(button2.find().name, 'Text')

        button1.click()

        button2.wait_until_invisible()

    def test_negative_wait_until_visible(self):
        class Page(BasePage):
            url = self.url
            button1 = Button(ID('b-01'))
            button2 = Button(ID('b-02'))

        page = Page()
        page.get()

        button1 = page.button1
        button1.find().click()

        button2 = page.button2
        with self.assertRaises(TimeoutException) as e:
            button2.wait_until_visible(timeout=1)

    def test_negative_wait_until_invisible(self):
        class Page(BasePage):
            url = self.url
            button1 = Button(ID('b-01'))
            button2 = Button(ID('b-02'))

        page = Page()
        page.get()

        with self.assertRaises(TimeoutException) as e:
            page.button1.find().wait_until_invisible(timeout=1)
