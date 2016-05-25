from selenium import webdriver



def get_driver():
    """
    Simple singleton to obtain web driver.
    For now the support of this functionality is not a goal.
    :return: instance of Chrome driver
    """
    if hasattr(get_driver, '_driver') and get_driver._driver is not None:
        try:
            get_driver._driver.title
        except:
            try:
                get_driver._driver.quit()
            except:
                pass
        else:
            return get_driver._driver
    get_driver._driver = webdriver.Chrome()
    return get_driver._driver
