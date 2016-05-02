from copy import copy
from inspect import isclass

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from autoui.config import Config
from autoui.driver import get_driver
from autoui.exceptions import InvalidLocator, DebugException
from autoui.locators import Locator


class _CommonElement:
    """
    Class contains common part of two classes: Element and Elements.
    Do not use this class out of this module.
    """
    locator = None
    search_with_driver = False
    mixins = None

    def __init__(self, locator=None, search_with_driver=None, mixins=None, parent=None):
        """
        :param locator: instance of Locator
        :param search_with_driver: bool type parameter representing how web element will be found
        :param mixins: tuple containing classes
        :param parent: instance to which attach current element
        """
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
            self.mixins = mixins
        if self.mixins:
            self.__class__ = type(self.__class__.__name__, self.mixins + (self.__class__,), {})

        if parent:
            if isclass(parent):
                self._owner = parent
            else:
                self._instance = parent
                self._owner = parent.__class__

    def __get__(self, instance, owner):
        self._instance = instance
        self._owner = owner
        return self

    def __call__(self):
        self.find()
        return self

    def _get_finder(self):
        # every element can be found 2 ways: using driver and using founded element
        if isinstance(self._instance, Element) and self.search_with_driver is False:
            if self._instance.web_element:
                return self._instance.web_element
        return get_driver()

    def _validate_locator(self):
        if not isinstance(self.locator, Locator):
            raise InvalidLocator('`locator` must be instance of class `Locator`, got `{}`'.format(
                self.locator.__name__ if isclass(self.locator) else self.locator.__class__.__name__))

    def _validate_search_with_driver(self):
        t = type(self.search_with_driver)
        if t is not bool:
            raise TypeError('`search_with_driver` must be of `bool` type, got `{}`'.format(t.__name__))

    def _validate_web_element(self):
        assert isinstance(self.web_element, WebElement), \
            '`web_element` not subclasses `WebElement` in `{}` object at runtime'.format(
                self.__class__.__name__)


class Element(_CommonElement):
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
                # find element once again after parent is found
                self.web_element = finder.find_element(*self.locator.get())
            except:
                raise
        self._validate_web_element()

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

    def get_locators(self):
        pass


class Elements(_CommonElement):
    """
    Describes multiple elements,
    access found elements through `self.elements` list
    """
    base_class = None
    base_class_mixins = None

    def __init__(self, locator=None, base_class=None, search_with_driver=None, mixins=None, base_class_mixins=None):
        super().__init__(locator, search_with_driver, mixins)
        self.elements = []
        if base_class:
            self.base_class = base_class
        if base_class_mixins:
            self.base_class_mixins = base_class_mixins

    def find(self):
        finder = self._get_finder()
        try:
            web_elements = finder.find_elements(*self.locator.get())
        except StaleElementReferenceException:
            try:
                if hasattr(self._instance, '_instance') and hasattr(self._instance, '_owner'):
                    self._instance.find()
                else:
                    raise DebugException('Need to investigate current problem')
                # find elements once again after parent is found
                web_elements = finder.find_elements(*self.locator.get())
            except:
                raise
        # wrap web_elements
        for web_element in web_elements:
            element = web_element
            element.web_element = copy(web_element)
            if self.base_class_mixins:
                element.__class__ = type(self.base_class.__name__, (self.base_class,) + self.base_class_mixins, {})
            else:
                element.__class__ = self.base_class
            element._instance = self
            element._owner = self.__class__
            self.elements.append(element)

        return self

    def wait_until_all_visible(self, timeout=Config.TIMEOUT, poll_frequency=Config.POLL_FREQUENCY):
        pass

    def wait_until_all_invisible(self, timeout=Config.TIMEOUT, poll_frequency=Config.POLL_FREQUENCY):
        pass
