from autoui.base import BasePage, BaseSection
from autoui.element.common import Input
from autoui.find import Find
from autoui.locator import XPath


class HeaderSection(BaseSection):
    search = Find(Input, XPath('.//input[@type="text" and @name="q"]'))

    def type(self):
        # search with HeaderSection._element
        self.search.type('autoui')
        self.search.type('autoui once again!')


class GitHubPage(BasePage):
    url = 'https://github.com/'
    header = Find(HeaderSection, XPath('//div[contains(@class, "header") and @role="banner"]'))


if __name__ == '__main__':
    GitHubPage.get()
    GitHubPage.header.type()
