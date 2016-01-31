from inspect import isclass
from warnings import warn

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement

from autoui.driver import get_driver
from autoui.exceptions import InvalidLocator, InvalidWebElementInstance, DebugException
from autoui.locators import Locator


class Element(object):
    web_element = None
    locator = None
    search_with_driver = False

    def __init__(self, locator=None, search_with_driver=search_with_driver, mixins=None):
        if locator is not None:
            self.locator = locator
            self._validate_locator()

        if search_with_driver is not None:
            self.search_with_driver = search_with_driver

        if mixins:
            bases = [self.__class__]
            bases.extend(mixins)
            bases = tuple(bases)
            self.__class__ = type(self.__class__.__name__, bases, {})

    def __get__(self, instance, owner):
        self._instance = instance
        self._owner = owner
        return self

    def find(self):
        finder = self._get_finder()
        try:
            self.web_element = finder.find_element(*self.locator.get())
        except StaleElementReferenceException:
            try:
                if hasattr(self._instance, '_instance') and hasattr(self._instance, '_owner'):
                    self._instance.find()
                else:
                    raise DebugException('Need to investigate current problem')
                self.web_element = finder.find_element(*self.locator.get())
            except:
                raise
        return self

    def _validate_locator(self):
        if not isinstance(self.locator, Locator):
            raise InvalidLocator('`locator` must be instance of class `Locator`, got `{}`'.format(
                self.locator.__name__ if isclass(self.locator) else self.locator.__class__.__name__))

    def _get_finder(self):
        if self._instance is not None and isinstance(self._instance, Element) and \
                hasattr(self._instance, 'web_element'):
            if not isinstance(self._instance.web_element, WebElement):
                warn('`web_element` instance not subclasses `WebElement` in `{}` object at runtime'.format(
                    self._instance.__class__.__name__, self._instance), InvalidWebElementInstance)
            elif not (hasattr(self, 'search_with_driver') and self.search_with_driver is True):
                return self._instance.web_element
        return get_driver()

    def _validate_search_with_driver(self):
        t = type(self.search_with_driver)
        if t is not bool:
            raise TypeError('`search_with_driver` must be of `bool` type, got `{}`'.format(t.__name__))
