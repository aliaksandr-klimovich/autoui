from autoui.base_page import BasePage
from autoui.elements.simple import Button, Input
from autoui.locators import XPath, ID


class YaPage(BasePage):
    url = 'http://ya.ru'

    input = Input(ID('text'))
    find = Button(XPath('//button[@type="submit"]'))

    def find_text(self, text):
        self.input().type(text)
        self.find().click()


if __name__ == '__main__':
    YaPage().get().find_text('autoui')
