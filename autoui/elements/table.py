from HTMLParser import HTMLParser
from autoui.elements.abstract import Element, Fillable


class _HTMLTableParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.thead = []
        self.th = False

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'th':
            self.th = True

    def handle_data(self, data):
        if self.th:
            self.thead.append(data)
            print '<th>' + data + '</th>'

    def handle_endtag(self, tag):
        if tag == 'th':
            self.th = False


class StringTable(Element, Fillable):
    def fill(self, data):
        pass

    def get_state(self):
        pass
