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
        super(TestTable, cls).setUpClass()
        get_driver().get(cls.url)

    @classmethod
    def tearDownClass(cls):
        super(TestTable, cls).tearDownClass()
        get_driver().quit()

    def setUp(self):
        get_driver().refresh()

    def test_table(self):
        class TestTable(Table):
            locator = CSS('table')

        table = TestTable()()
        table_str = table.get_headers_str()
        eq_(table_str, ['Name', 'IP', 'Time', 'Started', 'Status'])

        # TODO: assertions
