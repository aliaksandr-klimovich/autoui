from autoui.element.abstract import Element, Fillable, Clickable


class Button(Element, Clickable):
    def click(self):
        self._element.click()


class Input(Element, Fillable):
    def type(self, text):
        self._element.clear()
        self._element.send_keys(text)

    def fill(self):
        pass
