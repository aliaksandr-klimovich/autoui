from time import sleep

from autoui.base import BasePage, BaseSection
from autoui.elements.common import Input
from autoui.find import Find
from autoui.locators import XPath


class HeaderSection(BaseSection):
    locator = XPath('//div[contains(@class, "header") and @role="banner"]')
    search = Find(Input, XPath('.//input[@type="text" and @name="q"]'))

    def type(self):
        self.search.type('autoui')
        sleep(2)
        self.search.type('autoui once again!')


class GitHubPage(BasePage):
    url = 'https://github.com/'
    header = Find(HeaderSection)


if __name__ == '__main__':
    GitHubPage.get()
    GitHubPage.header.type()
