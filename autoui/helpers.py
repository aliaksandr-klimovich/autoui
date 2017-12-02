from datetime import timedelta, datetime
from functools import wraps, partial
from time import sleep

from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

from autoui.exceptions import PropertyInstantiateException


class PropertyMeta(type):
    def __init__(cls, name, bases=None, namespace=None):
        cls._initial_state = {k: v for k, v in namespace.items() if not k.startswith('_') and not callable(v)}
        super().__init__(name, bases, namespace)

    def __iter__(cls):
        d = {k: v for k, v in cls.__dict__.items() if not k.startswith('_') and not callable(v)}
        for k, v in d.items():
            yield {k: v}


class Property(metaclass=PropertyMeta):
    def __new__(cls, *args, **kwargs):
        raise PropertyInstantiateException('Do not instantiate property class, it is not permitted')

    @classmethod
    def reset(cls):
        for k, v in cls._initial_state.items():
            setattr(cls, k, v)


def perform_delayed_cycle(total_delay, sleep_delay, exceptions=(AssertionError,)):
    """
    Description:
        Decorator for cycling execution of function that uses assertions multiple times

        :param total_delay: delay to wait function to return something
        :param sleep_delay: sleep time between function calls
        :param exceptions: exceptions to ignore to continue cycling

    Usage:
        @perform_delayed_cycle(timedelta(minutes=3), timedelta(seconds=30))
        def function():
            some_bool_arg = get_some_bool_arg()
            assert some_bool_arg is True

        In this case will be performed validation multiple times until some_bool_arg becomes True.
        Every 30 seconds function will be executed once and once again until timeout.
        After timeout (5 minutes later from start) will try to execute function without catching an exception.

    Restrictions:
        Decorated functions should raise (exceptions) in critical section
    """

    assert isinstance(total_delay, timedelta)
    assert isinstance(sleep_delay, timedelta)

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            end_time = datetime.today() + total_delay
            while datetime.today() < end_time:
                try:
                    return function(*args, **kwargs)
                except exceptions:
                    sleep(sleep_delay.total_seconds())
            else:
                return function(*args, **kwargs)

        return wrapper

    return decorator


with_wait_element = partial(perform_delayed_cycle,
                            exceptions=(AssertionError,
                                        NoSuchElementException,
                                        StaleElementReferenceException))
