from autoui.elements.abstract import Element, Fillable, Clickable


class Text(Element):
    @property
    def text(self):
        return self._element.text


class Button(Element, Clickable):
    def click(self):
        self._element.click()


class Input(Element, Fillable):
    def type(self, text):
        self._element.clear()
        self._element.send_keys(text)

    def fill(self, data):
        self.type(data)

    def get_state(self):
        return self._element.get_attribute('value')
