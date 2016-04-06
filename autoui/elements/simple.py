from selenium.webdriver.support.select import Select as SeleniumSelect

from autoui.elements.abstract import Element, Elements
from autoui.elements.mixins import Fillable


class Text(Element):
    @property
    def text(self):
        return self.web_element.text


class Button(Element):
    def click(self):
        self.web_element.click()

    @property
    def name(self):
        return self.web_element.text


class Buttons(Elements):
    base_class = Button


class Link(Element):
    @property
    def href(self):
        return self.web_element.get_attribute('href')


class Links(Elements):
    base_class = Link

    @property
    def hrefs(self):
        return [element.web_element.get_attribute('href') for element in self.elements]


class Input(Element, Fillable):
    def fill(self, data, stop=False):
        self.type(data)

    def get_state(self, stop=False):
        return self.web_element.get_attribute('value')

    def send_keys(self, data):
        self.web_element.send_keys(data)

    def type(self, text):
        if text is not None:
            self.web_element.clear()
            self.web_element.send_keys(text)


class Image(Element):
    @property
    def size(self):
        return self.web_element.size

    @property
    def width(self):
        return self.web_element.size['width']

    @property
    def height(self):
        return self.web_element.size['height']


class Select(Element, Fillable):
    def find(self):
        super(Select, self).find()
        self.selenium_select = SeleniumSelect(self.web_element)

    def select_by_visible_text(self, text):
        self.selenium_select.select_by_visible_text(text)

    def fill(self, data, stop=False):
        self.select_by_visible_text(data)

    def get_state(self, stop=False):
        return self.selenium_select.first_selected_option.text


class Checkbox(Element, Fillable):
    def is_checked(self):
        return self.web_element.is_selected()

    def check(self):
        if not self.is_checked():
            self.web_element.click()

    def uncheck(self):
        if self.is_checked():
            self.web_element.click()

    def fill(self, data, stop=False):
        if data:
            self.check()
        else:
            self.uncheck()

    def get_state(self, stop=False):
        return self.is_checked()
