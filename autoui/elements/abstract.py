from abc import abstractmethod, ABCMeta
from inspect import isclass

from autoui.driver import get_driver
from autoui.exceptions import InvalidLocatorException
from autoui.locators import Locator


class Element(object):
    __metaclass__ = ABCMeta
    locator = None
    search_with_driver = None

    def __init__(self, locator=None):
        """
        :param locator: obligatory instance of class ``Locator``
        """

        if locator is not None:
            self.locator = locator
        self._validate_locator()

    def __get__(self, instance, owner):
        finder = self._get_finder(instance, owner)
        web_element = finder.find_element(self.locator.by, self.locator.value)
        self.web_element = web_element
        return self

    def _validate_locator(self):
        if not isinstance(self.locator, Locator):
            raise InvalidLocatorException('`locator` must be instance of class `Locator`, got `{}`'.format(
                self.locator.__name__ if isclass(self.locator) else self.locator.__class__.__name__))

    def _get_finder(self, instance, owner):
        if instance is not None and hasattr(instance, 'web_element') and instance.web_element \
                and not (hasattr(self, 'search_with_driver') and self.search_with_driver is True):
            finder = instance.web_element
        else:
            finder = get_driver()
        return finder


class Elements(Element):
    __metaclass__ = ABCMeta

    def __get__(self, instance, owner):
        finder = self._get_finder(instance, owner)
        web_elements = finder.find_elements(self.locator.by, self.locator.value)
        self.web_elements = web_elements
        return self


class Fillable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def fill(self, data):
        pass

    @abstractmethod
    def get_state(self):
        pass
