from selenium.webdriver.remote.webelement import WebElement

from autoui.driver import get_driver
from autoui.exception import AutoUIException
from autoui.locator import Locator


class Find(object):
    def __init__(self, element=WebElement, locator=None,
                 element_init_args=None, element_init_kwargs=None):

        self.element = element
        self.element_init_args = element_init_args if element_init_args else []
        self.element_init_kwargs = element_init_kwargs if element_init_kwargs else {}

        if locator is not None:
            if not isinstance(locator, Locator):
                raise AutoUIException('`locator` must be instance of derived class from class `Locator`, '
                                      'got {}'.format(type(locator)))
            self.by = locator.by
            self.value = locator.value

    def __get__(self, instance, owner):
        finder = get_driver()
        element = finder.find_element(self.by, self.value)
        new_element = self.element(*self.element_init_args, **self.element_init_kwargs)
        new_element._element = element
        return new_element
