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

        cl = super(BaseSectionMeta, mcl).__new__(mcl, name, bases, nmspc)

        _names = []
        for attr in nmspc:
            cl_dict = cl.__dict__
            if isinstance(cl_dict[attr], Find):
                _names.insert(0, attr)
        cl._names = _names

        return cl


class BaseSection(object):
    """
    Inherit sections from this class that contains elements.
    Note, you can inherit from ``object``.
    Remember, that ``_element`` attribute is reserved.

    Set ``search_with_driver`` to ``True`` if you want to find your section with driver.

    Specify ``locator`` if you want to use default locator to find your section.
    If ``locator`` is used in Find declaration - it will be used first.

    ``_names`` derived from ``BaseSectionMeta``.
    It may be useful if you have to obtain names of elements that are located this ``Find`` class.
    However it does not guarantee receiving names of dynamic elements.
    """
    __metaclass__ = BaseSectionMeta
    _element = None
    _names = None
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
    """
    Realizes special section to fill it with one simple dict
    """
    stop_propagation = False

    def fill(self, dict_to_fill):
        """
        Recursively fills all section and inherited section if not ``stop_propagation`` is flagged.

        :param dict_to_fill: should be ``dict`` with names of class attributes that matches elements with ``Find``
        """
        _dict = self.__class__.__dict__
        _names = self._get_names()

        for _k, _v in dict_to_fill.items():
            if _v is not None and _k in _names:
                elcl = _dict[_k].element
                if issubclass(elcl, FillableSection) and self.stop_propagation is True:
                    continue
                if issubclass(elcl, Fillable):
                    _dict[_k].__get__(self, self.__class__).fill(_v)


class BasePage(BaseSection):
    @classmethod
    def get(cls, url=None):
        url = cls.url if cls.url else url
        get_driver().get(url)
