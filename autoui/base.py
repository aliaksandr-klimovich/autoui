from autoui.driver import get_driver
from autoui.exception import AutoUIException


class BasePage(object):
    @classmethod
    def get(cls, url=None):
        url = cls.url if cls.url else url
        get_driver().get(url)


class BaseSectionMeta(type):
    def __new__(mcl, name, bases, nmspc):
        if '_element' in nmspc and name != 'BaseSection':
            raise AutoUIException('`_element` attribute in classes that inherit `BaseSection` is reserved by framework')
        return type.__new__(mcl, name, bases, nmspc)


class BaseSection(object):
    """
    Inherit sections from this class that contains elements.
    Note, you can inherit from ``object``.
    Remember, that ``_element`` attribute is reserved.
    """
    __metaclass__ = BaseSectionMeta
    _element = None
    _search_with_driver = False
