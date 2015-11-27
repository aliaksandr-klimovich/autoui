from unittest import TestCase
from autoui.elements.table import _HTMLTableParser


class TestElements(TestCase):
    pass


class TestStringTable(TestCase):
    def test_parser_basic(self):
        s = """
            <table>
                <thead>
                    <tr>
                        <th>Month</th>
                        <th>Savings</th>
                    </tr>
                </thead>
                <tfoot>
                    <tr>
                        <td>Sum</td>
                        <td>$180</td>
                    </tr>
                </tfoot>
                <tbody>
                    <tr>
                        <td>January</td>
                        <td>$100</td>
                    </tr>
                    <tr>
                        <td>February</td>
                        <td>$80</td>
                    </tr>
                </tbody>
            </table>"""
        s = s.replace(' ', '').replace('\n', '')
        _HTMLTableParser().feed(s)
