from nose.tools import eq_

from autoui.driver import get_driver
from autoui.elements.table import Table
from autoui.locators import CSS
from tests.base import BaseTestCaseWithServer
from tests.test_app.web_server import base_url


class TestTable(BaseTestCaseWithServer):
    url = base_url + '/table'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        get_driver().get(cls.url)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        get_driver().quit()

    def setUp(self):
        get_driver().refresh()

    def test_get_headers(self):
        class TestTable(Table):
            locator = CSS('table')

        table = TestTable()()
        table_header = table.get_headers_str()
        eq_(table_header, ['Name', 'IP', 'Time', 'Started', 'Status'])

    def test_get_body(self):
        class TestTable(Table):
            locator = CSS('table')

        table = TestTable()()
        table_body = table.get_body_str()
        expected = [['name1', '127.0.0.1', '0 days, 6:37:32', 'Thu, 18 Feb 2016 09:05:15', 'up'],
                    ['name2', '127.0.0.2', '0 days, 0:24:59', 'Thu, 18 Feb 2016 15:15:26', 'down'],
                    ['name3', '127.0.0.3', '0 days, 7:43:54', 'Thu, 18 Feb 2016 07:57:12', 'down'],
                    ['name4', '127.0.0.4', '0 days, 8:18:11', 'Thu, 18 Feb 2016 07:15:12', 'down'],
                    ['name5', '127.0.0.5', '0 days, 6:44:37', 'Thu, 18 Feb 2016 08:55:45', 'down'],
                    ['name6', '127.0.0.6', '0 days, 8:17:46', 'Thu, 18 Feb 2016 07:17:13', 'down']]
        eq_(table_body, expected)

    def test_refresh(self):
        class MyTable(Table):
            locator = CSS('table')

        MyTable()()
        get_driver().refresh()
        MyTable()()
