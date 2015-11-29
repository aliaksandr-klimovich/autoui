from autoui.base import BasePage
from autoui.elements.common import Button, Input

from autoui.locators import XPath, ID


class YaPage(BasePage):
    url = "http://ya.ru"
    input = Input(ID("text"))
    find = Button(XPath('//button[@type="submit"]'))

    def find_text(self, text):
        self.input.type(text)
        self.find.click()


if __name__ == "__main__":
    ya_page = YaPage()
    ya_page.get()
    ya_page.find_text("autoui")
