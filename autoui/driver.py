from selenium import webdriver


def get_driver():
    if hasattr(get_driver, '_driver'):
        return get_driver._driver
    get_driver._driver = webdriver.Chrome()
    return get_driver._driver
