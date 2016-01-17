from functools import wraps

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

DEFAULT_TIMEOUT = 30
POLL_FREQUENCY = 0.5


class CommonWaiter(object):
    def __init__(self, timeout=DEFAULT_TIMEOUT, poll_frequency=POLL_FREQUENCY):
        self.timeout = timeout
        self.poll_frequency = poll_frequency


class until_presence_of_element_located(CommonWaiter):
    def __call__(self, _find):
        @wraps(_find)
        def wrapper(finder, locator):
            return WebDriverWait(finder, self.timeout, self.poll_frequency). \
                until(expected_conditions.presence_of_element_located(locator.get()))
        return wrapper


class until_visibility_of_element_located(CommonWaiter):
    def __call__(self, _find):
        @wraps(_find)
        def wrapper(finder, locator):
            # TODO: fix bug. visibility_of_element_located returns bool, _find must return web element
            return WebDriverWait(finder, self.timeout, self.poll_frequency). \
                until(expected_conditions.visibility_of_element_located(locator.get()))
        return wrapper


class until_invisibility_of_element_located(CommonWaiter):
    def __call__(self, _find):
        @wraps(_find)
        def wrapper(finder, locator):
            # TODO: fix bug. invisibility_of_element_located returns bool, _find must return web element
            return WebDriverWait(finder, self.timeout, self.poll_frequency). \
                until(expected_conditions.invisibility_of_element_located(locator.get()))
        return wrapper
