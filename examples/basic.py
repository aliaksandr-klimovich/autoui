from autoui.base import BasePage
from autoui.elements.common import Input, Button
from autoui.find import Find
from autoui.locators import ID, XPath


class YaPage(BasePage):
    url = "http://ya.ru"
    input = Find(Input, ID("text"))
    find = Find(Button, XPath('//button[@type="submit"]'))

    @classmethod
    def find_text(cls, text):
        cls.input.type(text)
        cls.find.click()


if __name__ == "__main__":
    YaPage.get()
    YaPage.find_text("autoui")
