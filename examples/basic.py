from autoui.base import BasePage
from autoui.elements.common import Input, Button
from autoui.find import Find
from autoui.locators import ID, XPath


class YandexPage(BasePage):
    url = "http://ya.ru"
    input = Find(Input, ID("text"))
    find = Find(Button, XPath('//button[@type="submit"]'))

    @classmethod
    def find_text(self, text):
        self.input.type(text)
        self.find.click()


if __name__ == "__main__":
    YandexPage.get()
    YandexPage.input.type("text")
    YandexPage.find.click()

