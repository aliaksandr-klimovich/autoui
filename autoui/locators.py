from selenium.webdriver.common.by import By

from autoui.exceptions import AutoUIException


class _Locator(object):
    """
    Common Locator object.
    Do not instantiate it.
    Use derived classes.
    """

    def __init__(self, value):
        if type(value) is not str:
            raise AutoUIException('Value must be str type')
        self.value = value


class ID(_Locator):
    def __init__(self, value):
        self.by = By.ID
        super(ID, self).__init__(value)


class XPath(_Locator):
    def __init__(self, value):
        self.by = By.XPATH
        super(XPath, self).__init__(value)


class LinkText(_Locator):
    def __init__(self, value):
        self.by = By.LINK_TEXT
        super(LinkText, self).__init__(value)


class PartialLinkText(_Locator):
    def __init__(self, value):
        self.by = By.PARTIAL_LINK_TEXT
        super(PartialLinkText, self).__init__(value)


class Name(_Locator):
    def __init__(self, value):
        self.by = By.NAME
        super(Name, self).__init__(value)


class TagName(_Locator):
    def __init__(self, value):
        self.by = By.TAG_NAME
        super(TagName, self).__init__(value)


class ClassName(_Locator):
    def __init__(self, value):
        self.by = By.CLASS_NAME
        super(ClassName, self).__init__(value)


class CSS(_Locator):
    def __init__(self, value):
        self.by = By.CSS_SELECTOR
        super(CSS, self).__init__(value)
