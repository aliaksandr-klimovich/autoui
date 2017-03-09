from selenium import webdriver


def get_driver():
    """
    Simple singleton to obtain web driver.
    For now the support of this functionality is not a goal.
    :return: instance of Chrome driver
    """
    if hasattr(get_driver, 'driver') and get_driver.driver is not None:
        try:
            getattr(get_driver.driver, 'title')
        except AttributeError:
            try:
                get_driver.driver.quit()
            except:
                pass
        else:
            return get_driver.driver
    get_driver.driver = webdriver.Chrome()
    return get_driver.driver
