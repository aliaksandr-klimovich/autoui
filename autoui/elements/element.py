from autoui.elements.abstract import Element
from autoui.elements.mixins import Descriptive, WaitingAndScrollingElement


class VElement(WaitingAndScrollingElement, Element):
    """
    A visible element
    """


class DElement(Descriptive, Element):
    """
    Descriptive element
    """


class VDElement(WaitingAndScrollingElement, Descriptive, Element):
    """
    Visible and descriptive element
    """
