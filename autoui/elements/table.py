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
    # As the tr element can have multiple td elements and
    # each tr element is part of trs object, it will not be initialized
    # as class property, so, need to create instances of tr
    # class in the __init__ method.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tds = Tds()
        self.tds.__get__(self, self.__class__)


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
        # find all elements to use them later in methods
        super().find()
        self.thead().ths()
        self.tbody().trs()
        for tr in self.tbody.trs:
            tr.tds()
        return self

    def get_headers(self):
        headers = self.thead.ths.elements
        return headers

    def get_headers_str(self):
        ths = []
        for th in self.thead.ths.elements:
            text = th.web_element.text
            ths.append(text)
        return ths

    def get_body_str(self):
        trs = []
        for tr in self.tbody.trs.elements:
            tds = []
            for td in tr.tds.elements:
                text = td.web_element.text
                tds.append(text)
            trs.append(tds)
        return trs
