from selenium import webdriver


def get_driver():
    if hasattr(get_driver, 'driver'):
        return get_driver.driver
    get_driver.driver = webdriver.Firefox()
    return get_driver.driver
