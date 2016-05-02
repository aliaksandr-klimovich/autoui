from autoui.elements.abstract import Element, Elements
from autoui.locators import CSS


class Th(Element):
    pass


class Ths(Elements):
    locator = CSS('th')
    base_class = Th


class Thead(Element):
    locator = CSS('thead')
    ths = Ths()


class Td(Element):
    pass


class Tds(Elements):
    locator = CSS('td')
    base_class = Td


class Tr(Element):
    tds = Tds()


class Trs(Elements):
    locator = CSS('tr')
    base_class = Tr


class Tbody(Element):
    locator = CSS('tbody')
    trs = Trs()


class Table(Element):
    thead = Thead()
    tbody = Tbody()

    def find(self):
        """
        find all elements to use them later in methods
        """
        super().find()
        self.thead().ths()
        map(lambda element: element.tds(), self.tbody().trs().elements)
        return self

    def get_headers(self):
        return self.thead.ths.elements

    def get_headers_str(self):
        return [th.web_element.text for th in self.thead.ths.elements]

    # TODO: implement more functionality
