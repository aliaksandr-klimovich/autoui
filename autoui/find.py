from inspect import isclass

from autoui.driver import get_driver
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

        self.element_init_args = args if args else []
        self.element_init_kwargs = kwargs if kwargs else {}

        self._validate_locator(locator)
        self.locator = locator

    def __get__(self, instance, owner):
        new_element = self.element(*self.element_init_args, **self.element_init_kwargs)

        if self.locator:
            finder = self._get_finder(instance, owner)
            new_element._element = finder.find_element(self.locator.by, self.locator.value)
        elif 'locator' in self.element.__dict__:
            self._validate_locator(self.element.locator)
            finder = self._get_finder(instance, owner)
            new_element._element = finder.find_element(self.element.locator.by, self.element.locator.value)
        return new_element

    @staticmethod
    def _get_finder(instance, owner):
        if instance is not None and '_element' in instance.__dict__ \
                and not (hasattr(owner, 'search_with_driver') and owner.search_with_driver is True):
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
        if not isinstance(locator, Locator) and locator is not None:
            raise AutoUIException('`locator` must be instance of class `Locator`, got `{}`'.format(
                locator.__name__ if isclass(locator) else locator.__class__.__name__))
