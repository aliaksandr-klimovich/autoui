from abc import ABCMeta, abstractmethod


class Element(object):
    """
    Base abstract class for elements.
    ``_element`` is ``WebElement``, being found by ``Find`` class.
    """
    __metaclass__ = ABCMeta
    _element = None

    def __init__(self, _name=None):
        """
        :param _name: used by ``Find`` to implement element names
        """
        self._name = _name


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
