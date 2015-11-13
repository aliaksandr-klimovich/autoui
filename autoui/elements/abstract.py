from abc import ABCMeta, abstractmethod


class Element(object):
    """
    Base abstract class for elements.
    _element is WebElement, founded by Find class.
    """
    __metaclass__ = ABCMeta
    _element = None


class Clickable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def click(self):
        pass


class Fillable(object):
    @abstractmethod
    def fill(self):
        pass
