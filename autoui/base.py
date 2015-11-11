from autoui.driver import get_driver


class BasePageMeta(type):
    def __new__(mcl, name, bases, nmspc):
        return type.__new__(mcl, name, bases, nmspc)


class BasePage(object):
    __metaclass__ = BasePageMeta

    @classmethod
    def get(cls, url=None):
        url = cls.url if cls.url else url
        get_driver().get(url)


class BaseSection(object):
    pass
