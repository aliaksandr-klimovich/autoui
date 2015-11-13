from autoui.base import BasePage
from autoui.element.common import Input, Button
from autoui.find import Find
from autoui.locator import ID, XPath


class YaPage(BasePage):
    url = "http://ya.ru"
    input = Find(Input, ID("text"))
    find = Find(Button, XPath('//button[@type="submit"]'))

    @classmethod
    def find_text(self, text):
        self.input.type(text)
        self.find.click()


if __name__ == "__main__":
    YaPage.get()
    YaPage.input.type("text")
    YaPage.find.click()

