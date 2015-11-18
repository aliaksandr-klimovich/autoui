from abc import ABCMeta

from autoui.driver import get_driver
from autoui.elements.abstract import Fillable
from autoui.exceptions import AutoUIException
from autoui.find import Find


class BaseSectionMeta(ABCMeta):
    def __new__(mcl, name, bases, nmspc):
        if '_element' in nmspc and name != 'BaseSection':
            raise AutoUIException('`_element` attribute in classes that inherit `BaseSection` is reserved by framework')
        if 'search_with_driver' in nmspc and type(nmspc['search_with_driver']) is not bool:
            raise AutoUIException('`search_with_driver` class attribute must be of `bool` type')
        return super(BaseSectionMeta, mcl).__new__(mcl, name, bases, nmspc)


class BaseSection(object):
    """
    Inherit sections from this class that contains elements.
    Note, you can inherit from ``object``.
    Remember, that ``_element`` attribute is reserved.

    Set ``search_with_driver`` to ``True`` if you want to find your section with driver.

    Specify ``locator`` if you want to use default locator to find your section.
    If ``locator`` is used in Find declaration - it will be used first.
    """
    __metaclass__ = BaseSectionMeta
    _element = None
    search_with_driver = False
    locator = None

    @classmethod
    def _get_names(cls):
        names = []
        _dict = cls.__dict__
        for element_name in _dict:
            if isinstance(_dict[element_name], Find):
                names.insert(0, element_name)
        return names


class FillableSection(BaseSection, Fillable):
    def fill(self, dict_to_fill):
        _dict = self.__class__.__dict__
        _names = self._get_names()
        for _k, _v in dict_to_fill.items():
            if _k in _names:
                el = _dict[_k].__get__(self, self.__class__)
                if isinstance(el, Fillable):
                    el.fill(_v)


class BasePage(BaseSection):
    @classmethod
    def get(cls, url=None):
        url = cls.url if cls.url else url
        get_driver().get(url)
