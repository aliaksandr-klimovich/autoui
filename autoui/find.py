from inspect import isclass

from autoui.base import BaseSection
from autoui.driver import get_driver
from autoui.exception import AutoUIException
from autoui.locator import Locator


class Find(object):
    def __init__(self, element, locator=None,
                 element_init_args=None, element_init_kwargs=None):

        if not isclass(element):
            raise AutoUIException('`element` must be class')
        self.element = element
        self.element_init_args = element_init_args if element_init_args else []
        self.element_init_kwargs = element_init_kwargs if element_init_kwargs else {}

        if locator is None:
            self.locator = None
        else:
            self._validate_locator(locator)
            self.locator = locator

    def __get__(self, instance, owner):
        new_element = self.element(*self.element_init_args, **self.element_init_kwargs)

        def get_finder():
            if issubclass(owner, BaseSection) and owner._search_with_driver is False and hasattr(instance, '_element'):
                finder = instance._element
            else:
                finder = get_driver()
            return finder

        if self.locator:
            finder = get_finder()
            new_element._element = finder.find_element(self.locator.by, self.locator.value)
        elif hasattr(self.element, 'locator'):
            self._validate_locator(self.element.locator)
            finder = get_finder()
            new_element._element = finder.find_element(self.element.locator.by, self.element.locator.value)
        return new_element

    def _validate_locator(self, locator):
        if not isinstance(locator, Locator):
            raise AutoUIException('`locator` must be instance of class `Locator`, got `{}`'.format(
                locator.__name__ if isclass(locator) else locator.__class__.__name__))
