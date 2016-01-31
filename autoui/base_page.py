from autoui.driver import get_driver


class BasePage(object):
    """
    Base Page for examples.
    For now the support of this functionality is not a goal.
    """
    url = None

    @classmethod
    def get(cls, url=None):
        url = cls.url if cls.url else url
        get_driver().get(url)
