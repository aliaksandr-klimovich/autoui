from autoui.base import BasePage
from autoui.elements.common import Links

from autoui.locators import XPath


class MinskTheBy(BasePage):
    url = "http://minsk.the.by/"
    links = Links(XPath('//a'))

    def get_all_links(self):
        return self.links.hrefs


if __name__ == "__main__":
    minsk_the_by = MinskTheBy()
    minsk_the_by.get()
    print minsk_the_by.get_all_links()
