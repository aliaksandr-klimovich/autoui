from inspect import isclass
from warnings import warn

from autoui.base import BaseSection
from autoui.driver import get_driver
from autoui.element.abstract import Element
from autoui.exception import AutoUIException, AutoUIWarning
from autoui.locator import Locator


class Find(object):
    def __init__(self, element, locator=None, name=None,
                 args=None, kwargs=None):
        """
        :param element: class of element to locate
        :param locator: instance of ``Locator`` class, return value is instance of element if no locator specified
        :param name: will become ``_name`` attribute of returned element instance,
                     element must be instance of ``Element`` class
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

        self.element_name = name

    def __get__(self, instance, owner):
        if self.element_name:
            if issubclass(self.element, Element):
                self.element_init_kwargs.update({'_name': self.element_name})
            else:
                warn('You passed `{}` name to Find '
                     'but passed element `{}` is not subclass of `Element` class, '
                     'so getting attribute from returned element may raise exception, '
                     'observe `Element` implementation'.format(
                         self.element_name, self.element.__name__), AutoUIWarning)
        new_element = self.element(*self.element_init_args, **self.element_init_kwargs)

        def get_finder():
            if issubclass(owner, BaseSection) and owner.search_with_driver is False and '_element' in instance.__dict__:
                finder = instance._element
            else:
                finder = get_driver()
            return finder

        if self.locator:
            finder = get_finder()
            new_element._element = finder.find_element(self.locator.by, self.locator.value)
        elif 'locator' in self.element.__dict__:
            self._validate_locator(self.element.locator)
            finder = get_finder()
            new_element._element = finder.find_element(self.element.locator.by, self.element.locator.value)
        return new_element

    def _validate_element(self, element):
        if not isclass(element):
            raise AutoUIException('`element` must be class')

    def _validate_locator(self, locator):
        if not isinstance(locator, Locator) and locator is not None:
            raise AutoUIException('`locator` must be instance of class `Locator`, got `{}`'.format(
                locator.__name__ if isclass(locator) else locator.__class__.__name__))
