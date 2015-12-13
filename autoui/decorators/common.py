from functools import wraps

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

DEFAULT_TIMEOUT = 30


class until_presence_of_element_located(object):
    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self.timeout = timeout

    def __call__(self, _find):
        @wraps(_find)
        def wrapper(finder, locator):
            return WebDriverWait(finder, self.timeout). \
                until(expected_conditions.presence_of_element_located(locator.get()))

        return wrapper
