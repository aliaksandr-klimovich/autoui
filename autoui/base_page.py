from autoui.driver import get_driver


class BasePage:
    """
    Base Page for examples.
    For now the support of this functionality is not a goal.
    """
    url = None

    def get(self, url=None):
        url = self.url or url
        get_driver().get(url)
        return self
