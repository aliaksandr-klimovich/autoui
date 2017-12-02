from selenium import webdriver


def get_driver():
    """
    Simple singleton to obtain web driver.
    For now the support of this functionality is not a goal.
    :return: instance of Safari driver
    """
    if hasattr(get_driver, '_driver') and get_driver._driver is not None:
        try:
            getattr(get_driver._driver, 'title')
        except AttributeError:
            try:
                get_driver._driver.quit()
            except:
                raise
        else:
            return get_driver._driver
    get_driver._driver = webdriver.Safari()
    return get_driver._driver
