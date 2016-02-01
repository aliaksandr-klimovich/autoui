from inspect import isclass
from warnings import warn

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from autoui.config import Config
from autoui.driver import get_driver
from autoui.exceptions import InvalidLocator, InvalidWebElementInstance, DebugException
from autoui.locators import Locator


class Element(object):
    locator = None
    search_with_driver = False

    def __init__(self, locator=None, search_with_driver=None, mixins=None):
        self.web_element = None
        self._instance = None
        self._owner = None

        if locator:
            self.locator = locator
        self._validate_locator()

        if search_with_driver:
            self.search_with_driver = search_with_driver
        self._validate_search_with_driver()

        if mixins:
            bases = [self.__class__]
            bases.extend(mixins)
            bases = tuple(bases)
            self.__class__ = type(self.__class__.__name__, bases, {})

    def __get__(self, instance, owner):
        self._instance = instance
        self._owner = owner
        return self

    def __call__(self):
        return self.find()

    def find(self):
        finder = self._get_finder()
        try:
            self.web_element = finder.find_element(*self.locator.get())
        except StaleElementReferenceException:
            # try to find parent element
            try:
                if hasattr(self._instance, '_instance') and hasattr(self._instance, '_owner'):
                    self._instance.find()
                else:
                    raise DebugException('Need to investigate current problem')
                # find element one again after parent is found
                self.web_element = finder.find_element(*self.locator.get())
            except:
                raise
        self._validate_web_element()
        return self

    def _get_finder(self):
        if isinstance(self._instance, Element) and self.search_with_driver is False:
            self._validate_web_element_of_instance()
            return self._instance.web_element
        return get_driver()

    def _validate_web_element(self):
        assert isinstance(self.web_element, WebElement), \
            '`web_element` not subclasses `WebElement` in `{}` object at runtime'.format(
                self.__class__.__name__)

    def _validate_web_element_of_instance(self):
        if not isinstance(self._instance.web_element, WebElement):
            warn('`web_element` not subclasses `WebElement` in `{}` object at runtime'.format(
                self._instance.__class__.__name__, self._instance), InvalidWebElementInstance)

    def _validate_locator(self):
        if not isinstance(self.locator, Locator):
            raise InvalidLocator('`locator` must be instance of class `Locator`, got `{}`'.format(
                self.locator.__name__ if isclass(self.locator) else self.locator.__class__.__name__))

    def _validate_search_with_driver(self):
        t = type(self.search_with_driver)
        if t is not bool:
            raise TypeError('`search_with_driver` must be of `bool` type, got `{}`'.format(t.__name__))

    def wait_until_visible(self, timeout=Config.TIMEOUT, poll_frequency=Config.POLL_FREQUENCY):
        finder = self._get_finder()
        WebDriverWait(finder, timeout, poll_frequency). \
            until(expected_conditions.visibility_of_element_located(self.locator.get()),
                  'Searchable by `{}` element with `{}` is not visible during {} seconds'.format(
                      self.locator,
                      finder.__class__.__name__,
                      timeout
                  ))

    def wait_until_invisible(self, timeout=Config.TIMEOUT, poll_frequency=Config.POLL_FREQUENCY):
        finder = self._get_finder()
        WebDriverWait(finder, timeout, poll_frequency). \
            until(expected_conditions.invisibility_of_element_located(self.locator.get()),
                  'Searchable by `{}` element with `{}` is still visible during {} seconds'.format(
                      self.locator,
                      finder.__class__.__name__,
                      timeout
                  ))
