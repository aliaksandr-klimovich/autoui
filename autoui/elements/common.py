from autoui.elements.abstract import Element, Elements, Fillable


class Button(Element):
    def click(self):
        self.web_element.click()


class Buttons(Elements):
    pass


class Link(Element):
    @property
    def href(self):
        return self.web_element.get_attribute('href')


class Links(Elements):
    def get_hyper_references(self):
        return [element.get_attribute('href') for element in self.web_elements]


class Input(Element, Fillable):
    def type(self, text):
        self.web_element.clear()
        self.web_element.send_keys(text)

    def fill(self, data, stop=False):
        self.type(data)

    def get_state(self, stop=False):
        return self.web_element.get_attribute('value')

    def send_keys(self, data):
        self.web_element.send_keys(data)
