from autoui.base import BasePage
from autoui.elements.common import Button
from autoui.locators import ID
from autoui.waiters import wait_until_element_is_visible, wait_until_element_is_invisible


class TestPage(BasePage):
    url = 'http://127.0.0.1:8000/page.html'
    button01 = Button(ID('b-01'))
    button02 = Button(ID('b-02'), (wait_until_element_is_invisible('after', timeout=1),
                                   wait_until_element_is_visible('after', timeout=2.5)))


if __name__ == '__main__':
    test_page = TestPage()
    test_page.get()  # TODO: start simple http server from here
    test_page.button01.click()
    print test_page.button02.name
