from inspect import isclass
from warnings import warn

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement

from autoui.driver import get_driver
from autoui.exceptions import InvalidLocator, InvalidWebElementInstance, AttributeNotPermitted, DebugException
from autoui.locators import Locator


class _Abstract(type):
    def __new__(mcl, name, bases, nmspc):
        if name != 'Element' \
                and any([True if base.__name__ == 'Element' else False for base in bases]) \
                and 'web_element' in nmspc:
            raise AttributeNotPermitted('`web_element` attribute is reserved by framework, '
                                        'error found in `{}` class'.format(name))
        if name != 'Elements' \
                and any([True if base.__name__ == 'Elements' else False for base in bases]) \
                and 'web_elements' in nmspc:
            raise AttributeNotPermitted('`web_elements` attribute is reserved by framework, '
                                        'error found in `{}` class'.format(name))
        # if name != 'Fillable' \
        #         and any([True if base.__name__ == 'Fillable' else False for base in bases]) \
        #         and not ('fill' in nmspc and 'get_state' in nmspc):
        #     raise MethodNotOverridden('you must override all abstract methods in class `{}` of `Fillable`'.format(
        #         name))
        return type.__new__(mcl, name, bases, nmspc)


class Element(object):
    __metaclass__ = _Abstract
    web_element = None
    locator = None
    search_with_driver = False

    def __init__(self, locator=None, decorators=()):
        """
        :param locator: obligatory instance of class ``Locator``
        """
        # check to not override default locator
        if locator is not None:
            self.locator = locator
        self._validate_locator()

        for decorator in decorators[::-1]:
            self._find = decorator(self._find)

    def __get__(self, instance, owner):
        self._instance = instance
        self._owner = owner

        finder = self._get_finder(instance, owner)

        try:
            web_element = self._find(finder, self.locator)
        except StaleElementReferenceException:
            try:
                if hasattr(instance, '_instance') and hasattr(instance, '_owner'):
                    instance.__get__(instance._instance, instance._owner)
                else:
                    raise DebugException("Need to investigate current problem")
                web_element = self._find(finder, self.locator)
            except:
                raise

        self.web_element = web_element
        return self

    def _find(self, finder, locator):
        """
        must return web element
        :param finder: web element or driver
        :param locator: instance of class Locator
        """
        return finder.find_element(*locator.get())

    def _validate_locator(self):
        if not isinstance(self.locator, Locator):
            raise InvalidLocator('`locator` must be instance of class `Locator`, got `{}`'.format(
                self.locator.__name__ if isclass(self.locator) else self.locator.__class__.__name__))

    def _get_finder(self, instance, owner):
        self._validate_search_with_driver()
        if instance is not None and isinstance(instance, Element) and hasattr(instance, 'web_element'):
            if not isinstance(instance.web_element, WebElement):
                warn('`web_element` instance not subclasses `WebElement` in `{}` object at runtime'.format(
                    instance.__class__.__name__, instance), InvalidWebElementInstance)
            elif not (hasattr(self, 'search_with_driver') and self.search_with_driver is True):
                return instance.web_element
        return get_driver()

    def _validate_search_with_driver(self):
        t = type(self.search_with_driver)
        if t is not bool:
            raise TypeError('`search_with_driver` must be of `bool` type, got `{}`'.format(t.__name__))


class Elements(Element):
    web_elements = None

    def __get__(self, instance, owner):
        finder = self._get_finder(instance, owner)
        web_elements = finder.find_elements(*self.locator.get())
        self.web_elements = web_elements
        return self


class Fillable(object):
    """
    Subclass it to make element fillable.
    Do not forget override ``fill`` and ``get_state`` methods.
    This methods should be compatible,
    i.e. data, obtained with ``get_state`` method, should be capable to pass to ``fill`` method without exceptions.
    """
    stop_propagation = False

    def _get_names(self):
        """
        Returns names (strings) of class and instance attributes that are instance of ``Element`` class.
        """
        names = set()
        for element_name in self.__class__.__dict__:
            if isinstance(self.__class__.__dict__[element_name], Element):
                names.add(element_name)
        for element_name in self.__dict__:
            if isinstance(self.__dict__[element_name], Element) and element_name not in ('_instance', '_owner'):
                names.add(element_name)
        return names

    def fill(self, data, stop=False):
        """
        Recursively fills all elements with data.
        :param data: dictionary to fill with keys as elements names and values as fillable data
        :param stop: reserved for recursion stop
        """
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
        :return:  dict with state data, compatible with ``fill`` method
        """
        if stop:
            return
        _names = self._get_names()
        state = {}
        for name in _names:
            if self.stop_propagation:
                # do not add anything on enter in stopped element
                s = getattr(self, name).get_state(stop=True)
                if s is not None:
                    state[name] = s
            else:
                state[name] = getattr(self, name).get_state()
        return state
