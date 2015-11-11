from selenium.webdriver.common.by import By


def ID(value):
    return By.ID, value


def XPath(value):
    return By.XPATH, value


def LinkText(value):
    return By.LINK_TEXT, value


def PartialLinkText(value):
    return By.PARTIAL_LINK_TEXT, value


def Name(value):
    return By.NAME, value


def TagName(value):
    return By.TAG_NAME, value


def ClassName(value):
    return By.CLASS_NAME, value


def CSS(value):
    return By.CSS_SELECTOR, value
