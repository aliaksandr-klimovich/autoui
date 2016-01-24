from selenium import webdriver


def get_driver():
    """
    Simple singleton to obtain web driver.
    For now the support of this functionality is not a goal.
    :return: instance of driver
    """
    if hasattr(get_driver, '_driver'):
        return get_driver._driver
    get_driver._driver = webdriver.Chrome()
    return get_driver._driver
