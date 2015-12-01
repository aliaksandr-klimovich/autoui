from autoui.driver import get_driver


class BasePage(object):
    url = None

    @classmethod
    def get(cls, url=None):
        url = cls.url if cls.url else url
        get_driver().get(url)
