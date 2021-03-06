from inspect import isclass

from selenium.webdriver.common.by import By


class Locator:
    def __init__(self, by, value):
        if type(by) is not str:
            raise TypeError('`by` must be `str` type, got `{}`'.format(
                by.__name__ if isclass(by) else by.__class__.__name__))
        if type(value) is not str:
            raise TypeError('`value` must be `str` type, got `{}`'.format(
                value.__name__ if isclass(value) else value.__class__.__name__))

        self.by = by
        self.value = value

    def __str__(self):
        return self.by + '=' + self.value

    def get(self):
        return self.by, self.value


class XPath(Locator):
    def __init__(self, value):
        super().__init__(By.XPATH, value)


class CSS(Locator):
    def __init__(self, value):
        super().__init__(By.CSS_SELECTOR, value)


class ID(Locator):
    def __init__(self, value):
        super().__init__(By.ID, value)


class ClassName(Locator):
    def __init__(self, value):
        super().__init__(By.CLASS_NAME, value)


class TagName(Locator):
    def __init__(self, value):
        super().__init__(By.TAG_NAME, value)


class Name(Locator):
    def __init__(self, value):
        super().__init__(By.NAME, value)


class LinkText(Locator):
    def __init__(self, value):
        super().__init__(By.LINK_TEXT, value)


class PartialLinkText(Locator):
    def __init__(self, value):
        super().__init__(By.PARTIAL_LINK_TEXT, value)
