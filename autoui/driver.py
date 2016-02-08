from selenium import webdriver


def get_driver():
    """
    Simple singleton to obtain web driver.
    For now the support of this functionality is not a goal.
    :return: instance of driver
    """
    if hasattr(get_driver, '_driver') and get_driver._driver is not None:
        return get_driver._driver
    get_driver._driver = webdriver.Chrome()
    return get_driver._driver
