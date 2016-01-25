from functools import wraps

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

DEFAULT_TIMEOUT = 30
POLL_FREQUENCY = 0.5


class AbstractWaiter(object):
    def __init__(self, timeout=DEFAULT_TIMEOUT, poll_frequency=POLL_FREQUENCY):
        """
        Be careful with timeout, for nested decorator is end time from first entrance to most outer decorator
        """
        self.timeout = timeout
        self.poll_frequency = poll_frequency

    def __call__(self, _find):
        """
        Decorated _find method of Element class

        :param _find: by default if _find method from Element class,
                      but is there are more than one decorator,
                      than _find is other decorator
        :return: wrapper of _find method or other decorator
        """
        @wraps(_find)
        def wrapper(finder, locator):
            return _find(finder, locator)
        return wrapper


class wait_until_element_is_visible(AbstractWaiter):
    def __init__(self, action, timeout=DEFAULT_TIMEOUT, poll_frequency=POLL_FREQUENCY):
        super(wait_until_element_is_visible, self).__init__(timeout, poll_frequency)
        assert action in ('after', 'replace')
        self.action = action

    def __call__(self, _find):
        @wraps(_find)
        def wrapper(finder, locator):
            result = WebDriverWait(finder, self.timeout, self.poll_frequency). \
                until(expected_conditions.visibility_of_element_located(locator.get()),
                    'Searchable by `{}` element with `{}` is not visible during {} seconds'.format(
                        locator,
                        finder.__class__.__name__,
                        self.timeout
                    ))
            if self.action == 'replace':
                return result
            if self.action == 'after':
                return _find(finder, locator)
        return wrapper


class wait_until_element_is_invisible(AbstractWaiter):
    def __init__(self, action, timeout=DEFAULT_TIMEOUT, poll_frequency=POLL_FREQUENCY):
        super(wait_until_element_is_invisible, self).__init__(timeout, poll_frequency)
        assert action in ('after', 'replace')
        self.action = action

    def __call__(self, _find):
        @wraps(_find)
        def wrapper(finder, locator):
            result = WebDriverWait(finder, self.timeout, self.poll_frequency). \
                until(expected_conditions.invisibility_of_element_located(locator.get()),
                    'Searchable by `{}` element with `{}` is still visible during {} seconds'.format(
                        locator,
                        finder.__class__.__name__,
                        self.timeout
                    ))
            if self.action == 'replace':
                return result
            if self.action == 'after':
                return _find(finder, locator)
        return wrapper
