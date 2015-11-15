from inspect import isclass

from selenium.webdriver.common.by import By

from autoui.exception import AutoUIException


class Locator(object):
    def __init__(self, by, value):
        if type(by) is not str:
            raise AutoUIException('`by` must be `str` type, got `{}`'.format(
                by.__name__ if isclass(by) else by.__class__.__name__))
        if type(value) is not str:
            raise AutoUIException('`value` must be `str` type, got `{}`'.format(
                value.__name__ if isclass(value) else value.__class__.__name__))

        self.by = by
        self.value = value


class ID(Locator):
    def __init__(self, value):
        super(ID, self).__init__(By.ID, value)


class XPath(Locator):
    def __init__(self, value):
        super(XPath, self).__init__(By.XPATH, value)


class LinkText(Locator):
    def __init__(self, value):
        super(LinkText, self).__init__(By.LINK_TEXT, value)


class PartialLinkText(Locator):
    def __init__(self, value):
        super(PartialLinkText, self).__init__(By.PARTIAL_LINK_TEXT, value)


class Name(Locator):
    def __init__(self, value):
        super(Name, self).__init__(By.NAME, value)


class TagName(Locator):
    def __init__(self, value):
        super(TagName, self).__init__(By.TAG_NAME, value)


class ClassName(Locator):
    def __init__(self, value):
        super(ClassName, self).__init__(By.CLASS_NAME, value)


class CSS(Locator):
    def __init__(self, value):
        super(CSS, self).__init__(By.CSS_SELECTOR, value)
