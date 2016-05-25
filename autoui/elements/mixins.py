from autoui.config import Config
from autoui.driver import get_driver
from autoui.elements.abstract import Element


class _CommonFilling:
    stop_propagation = False

    def _get_names(self):
        """
        Returns names (strings) of class and instance attributes that are instance of ``Element`` class.
        """
        names = set()
        for element_name in self.__class__.__dict__:
            if isinstance(self.__class__.__dict__[element_name], Element):
                names.add(element_name)
        for element_name in self.__dict__:
            if isinstance(self.__dict__[element_name], Element) and element_name not in ('_instance', '_owner'):
                names.add(element_name)
        return names


class Readable(_CommonFilling):
    def get_state(self, stop=False):
        """
        :return:  dict with state data, compatible with ``fill`` method
        :param stop: reserved for stop recursion
        """
        if stop:
            return
        _names = self._get_names()
        state = {}
        for name in _names:
            if self.stop_propagation:
                s = getattr(self, name)().get_state(stop=True)
                if s is not None:
                    state[name] = s
            else:
                state[name] = getattr(self, name)().get_state()
        return state


class Settable(_CommonFilling):
    def fill(self, data, stop=False):
        """
        Recursively fills all elements with data.
        :param data: dictionary to fill with keys as elements names and values as fillable data
        :param stop: reserved for stop recursion
        """
        if stop:
            return
        _names = self._get_names()
        for _k, _v in data.items():
            if _v is not None and _k in _names:
                if self.stop_propagation:
                    getattr(self, _k)().fill(_v, stop=True)
                else:
                    getattr(self, _k)().fill(_v)


class Filling(Readable, Settable):
    """
    Mixin class ``Filling`` for ``Element`` class.
    Those methods should be compatible,
    i.e. data, obtained with ``get_state`` method, should be capable to pass to ``fill`` method without exceptions.
    """


class WaitingElement:
    def __init__(self, *args, timeout=Config.TIMEOUT, poll_frequency=Config.POLL_FREQUENCY, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = timeout
        self.poll_frequency = poll_frequency

    def find(self, timeout=None, poll_frequency=None):
        self.wait_until_visible(timeout=timeout if timeout else self.timeout,
                                poll_frequency=poll_frequency if poll_frequency else self.poll_frequency)


class ScrollingElement:
    def find(self, *args, **kwargs):
        super().find(*args, **kwargs)
        self.scroll_to_element()

    def scroll_to_element(self):
        get_driver().execute_script('return arguments[0].scrollIntoView();', self.web_element)


class WaitingAndScrollingElement(ScrollingElement, WaitingElement):
    """
    Combines scrolling and waiting functions.
    First waiting function is executing (super call from scrolling) and then scrolling is executing.
    """


class Clicking:
    def click(self, with_js=False):
        if with_js:
            get_driver().execute_script('return arguments[0].click();', self.web_element)
        else:
            self.web_element.click()


class Descriptive:
    def __get__(self, instance, owner):
        super().__get__(instance, owner)
        self.find()
        return self
