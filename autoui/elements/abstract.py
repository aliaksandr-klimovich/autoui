from abc import ABCMeta, abstractmethod


class Element(object):
    """
    Base abstract class for elements.
    ``_element`` is ``WebElement``, being found by ``Find`` class.
    """
    __metaclass__ = ABCMeta
    _element = None


class Clickable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def click(self):
        pass


class Fillable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def fill(self):
        pass
