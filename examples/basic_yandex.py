from datetime import timedelta

from autoui.base_page import BasePage
from autoui.elements.simple import Button, Input
from autoui.elements.element import VDElement
from autoui.locators import XPath, ID


class VDInput(Input, VDElement):
    pass


class VDButton(Button, VDElement):
    pass


class YaPage(BasePage):
    url = 'http://ya.ru'

    input = VDInput(ID('text'), timeout=timedelta(seconds=34))
    find = VDButton(XPath('//button[@type="submit"]'))

    def find_text(self, text):
        self.input.type(text)
        self.find.click(with_js=True)


if __name__ == '__main__':
    YaPage().get().find_text('autoui')
