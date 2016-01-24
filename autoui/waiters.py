from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

DEFAULT_TIMEOUT = 30
POLL_FREQUENCY = 0.5


class AbstractWaiter(object):
    def __init__(self, timeout=DEFAULT_TIMEOUT, poll_frequency=POLL_FREQUENCY):
        self.timeout = timeout
        self.poll_frequency = poll_frequency

    def wrapper(self, finder, locator):
        return finder.find_element(locator.get())

    def __call__(self, _find):
        return self.wrapper


class until_presence_of_element_located(AbstractWaiter):
    def wrapper(self, finder, locator):
        return WebDriverWait(finder, self.timeout, self.poll_frequency). \
            until(expected_conditions.presence_of_element_located(locator.get()),
                  message='')
        # TODO: add formatted exception message


class until_visibility_of_element_located(AbstractWaiter):
    def wrapper(self, finder, locator):
        class visibility_of_element_located(object):
            def __init__(self, locator):
                self.locator = locator

            def __call__(self, finder):
                try:
                    element = expected_conditions._find_element(finder, self.locator)
                    if expected_conditions._element_if_visible(element):
                        return element
                except StaleElementReferenceException:
                    return False

        return WebDriverWait(finder, self.timeout, self.poll_frequency). \
            until(visibility_of_element_located(locator.get()),
                  'Searchable by `{}` element with `{}` is not visible during {} seconds'.format(
                      locator,
                      finder.__class__.__name__,
                      self.timeout
                  ))


class until_invisibility_of_element_located(AbstractWaiter):
    """
    Warning! This wrapper does not return `WebElement`!
    """
    def wrapper(self, finder, locator):

        WebDriverWait(finder, self.timeout, self.poll_frequency). \
            until(expected_conditions.invisibility_of_element_located(locator.get()),
                  message='')
        # TODO: add formatted exception message
