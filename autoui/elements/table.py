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
