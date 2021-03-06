from copy import copy
from inspect import isclass

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement

from autoui.config import Config
from autoui.driver import get_driver
from autoui.exceptions import InvalidLocator, DebugException
from autoui.helpers import with_wait_element
from autoui.locators import Locator


class _CommonElement:
    """
    Class contains common part of two classes: Element and Elements.
    Do not use this class out of this module.
    """
    locator = None
    search_with_driver = False

    def __init__(self, locator=None, search_with_driver=None, parent=None):
        """
        :param locator: instance of Locator
        :param search_with_driver: bool type parameter representing how web element will be found
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

    def find(self):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
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
        @with_wait_element(timeout, poll_frequency)
        def find():
            Element.find(self)
            # TODO: Can a TimeoutException appear here?
            assert self.web_element.is_displayed(), \
                'Web element is not visible during {} seconds'.format(timeout.total_seconds())

        find()

    def wait_until_invisible(self, timeout=Config.TIMEOUT, poll_frequency=Config.POLL_FREQUENCY):
        @with_wait_element(timeout, poll_frequency)
        def find():
            Element.find(self)
            assert not self.web_element.is_displayed(), \
                'Web element s not visible during {} seconds'.format(timeout.total_seconds())

        find()

    def get_locators(self):
        pass


class Elements(_CommonElement):
    """
    Describes multiple elements,
    access found elements through `self.elements` list
    """
    base_class = None

    def __init__(self, locator=None, base_class=None, search_with_driver=None, base_class_kwargs=None):
        super().__init__(locator, search_with_driver)
        self.elements = []
        if base_class:
            self.base_class = base_class
        self.base_class_kwargs = base_class_kwargs

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

        # remove elements from previous sessions
        self.elements = []

        # wrap web_elements
        for web_element in web_elements:
            element = self.base_class(locator=self.base_class.locator or self.locator,
                                      parent=self)
            for pr in element.__class__.__dict__:
                instance = getattr(element, pr, None)
                if isinstance(instance, Elements):
                    if self.base_class_kwargs is None:
                        instance = instance.__class__()  # __init__ of `Elements` subclass is empty!
                    else:
                        instance = instance.__class__(**self.base_class_kwargs)
                    instance.__get__(element, element.__class__)
                    setattr(element, pr, instance)
            element.web_element = web_element
            self.elements.append(element)

    def wait_until_all_visible(self, timeout=Config.TIMEOUT, poll_frequency=Config.POLL_FREQUENCY):
        map(lambda element: element.wait_until_visible(timeout, poll_frequency), self.elements)

    def wait_until_all_invisible(self, timeout=Config.TIMEOUT, poll_frequency=Config.POLL_FREQUENCY):
        map(lambda element: element.wait_until_invisible(timeout, poll_frequency), self.elements)

    def __getitem__(self, item):
        return self.elements[item]
