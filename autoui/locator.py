from selenium.webdriver.common.by import By

from autoui.exception import AutoUIException


class Locator(object):
    """
    Common Locator object.
    Do not instantiate it.
    Use derived classes.
    """

    def __init__(self, by, value):
        type_by, type_value = type(by), type(value)
        if type_by is not str:
            raise AutoUIException('`by` must be str type, got {}'.format(type_by))
        if type_value is not str:
            raise AutoUIException('`value` must be str type, got {}'.format(type_value))

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
