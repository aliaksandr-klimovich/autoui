from autoui.driver import get_driver
from autoui.exceptions import AutoUIException


class BasePage(object):
    @classmethod
    def get(cls, url=None):
        url = cls.url if cls.url else url
        get_driver().get(url)


class BaseSectionMeta(type):
    def __new__(mcl, name, bases, nmspc):
        if '_element' in nmspc and name != 'BaseSection':
            raise AutoUIException('`_element` attribute in classes that inherit `BaseSection` is reserved by framework')
        if 'search_with_driver' in nmspc and type(nmspc['search_with_driver']) is not bool:
            raise AutoUIException('`search_with_driver` class attribute must be of `bool` type')
        return type.__new__(mcl, name, bases, nmspc)


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
