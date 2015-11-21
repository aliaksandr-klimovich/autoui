from inspect import isclass

from autoui.driver import get_driver
from autoui.elements.abstract import Element
from autoui.exceptions import AutoUIException
from autoui.locators import Locator


class Find(object):
    def __init__(self, element, locator=None, args=None, kwargs=None):
        """
        :param element: class of element to locate
        :param locator: instance of ``Locator`` class, return value is instance of element if no locator specified
        :param args: initialization arguments for ``element``
        :param kwargs: initialization keywords for ``element``
        :return: instance of ``element`` class with special attributes
        """

        self._validate_element(element)
        self.element = element

        self._validate_locator(locator)
        self.locator = locator

        if issubclass(element, Element) and locator is None:
            raise AutoUIException('If element is subclass of `Element`, locator must be present')

        self.args = args if args else []
        self.kwargs = kwargs if kwargs else {}

    def __get__(self, instance, owner):
        new_element = self.element(*self.args, **self.kwargs)

        if self.locator:
            finder = self._get_finder(instance, owner)
            new_element._element = finder.find_element(self.locator.by, self.locator.value)
        elif hasattr(self.element, 'locator') and self.element.locator is not None:
            self._validate_locator(self.element.locator)
            finder = self._get_finder(instance, owner)
            new_element._element = finder.find_element(self.element.locator.by, self.element.locator.value)
        return new_element

    def _get_finder(self, instance, owner):
        if instance is not None and '_element' in instance.__dict__ \
                and not (hasattr(self.element, 'search_with_driver') and self.element.search_with_driver is True):
            finder = instance._element
        else:
            finder = get_driver()
        return finder

    @staticmethod
    def _validate_element(element):
        if not isclass(element):
            raise AutoUIException('`element` must be class')

    @staticmethod
    def _validate_locator(locator):
        if locator is not None and not isinstance(locator, Locator):
            raise AutoUIException('`locator` must be instance of class `Locator`, got `{}`'.format(
                locator.__name__ if isclass(locator) else locator.__class__.__name__))
