from abc import ABCMeta
from inspect import isclass

from autoui.driver import get_driver
from autoui.exceptions import InvalidLocatorException, AttributeNotPermittedException
from autoui.locators import Locator


class ElementMeta(ABCMeta):
    def __new__(mcl, name, bases, nmspc):
        if 'web_element' in nmspc and name != 'Element' and Element in bases:
            print bases, nmspc
            raise AttributeNotPermittedException('`web_element` attribute is reserved by framework')
        if 'web_elements' in nmspc and name != 'Elements' and Elements in bases:
            print bases, nmspc
            raise AttributeNotPermittedException('`web_elements` attribute is reserved by framework')
        return super(ElementMeta, mcl).__new__(mcl, name, bases, nmspc)


class Element(object):
    __metaclass__ = ElementMeta
    web_element = None
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
    web_elements = None

    def __get__(self, instance, owner):
        finder = self._get_finder(instance, owner)
        web_elements = finder.find_elements(self.locator.by, self.locator.value)
        self.web_elements = web_elements
        return self


class Fillable:
    stop_propagation = False

    def _get_names(self):
        names = set()
        for element_name in self.__class__.__dict__:
            if isinstance(self.__class__.__dict__[element_name], Element):
                names.add(element_name)
        for element_name in self.__dict__:
            if isinstance(self.__dict__[element_name], Element):
                names.add(element_name)
        return names

    def fill(self, data, stop=False):
        if stop:
            return
        _names = self._get_names()
        for _k, _v in data.items():
            if _v is not None and _k in _names:
                if self.stop_propagation:
                    getattr(self, _k).fill(_v, stop=True)
                else:
                    getattr(self, _k).fill(_v)

    def get_state(self, stop=False):
        """
        :return:  dict with data to check state or pass to ``fill`` method
        """
        if stop:
            return
        _names = self._get_names()
        state = {}
        for name in _names:
            if self.stop_propagation:
                s = getattr(self, name).get_state(stop=True)
                if s is not None:
                    state[name] = s
            else:
                state[name] = getattr(self, name).get_state()
        return state
