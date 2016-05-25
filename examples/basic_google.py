from autoui.base_page import BasePage
from autoui.elements.simple import Input, Button
from autoui.locators import CSS, XPath


class GooglePage(BasePage):
    url = 'http://google.com'
    search_line = Input(CSS('#lst-ib'))

    google_search_button = Button(XPath('.//input[@name="btnK"]'))


if __name__ == '__main__':
    google_page = GooglePage().get()
    google_page.search_line().send_keys('autoui')
    google_page.google_search_button().click(with_js=True)
