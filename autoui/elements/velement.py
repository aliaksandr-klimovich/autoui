from autoui.elements.abstract import Element
from autoui.elements.mixins import WaitingAndScrollingElement


class VElement(Element):
    # A "visible" element
    def __init__(self, locator=None, search_with_driver=None, mixins=None, parent=None):
        local_mixins = (WaitingAndScrollingElement, )
        if mixins:
            local_mixins = mixins + local_mixins
        super().__init__(locator=locator, search_with_driver=search_with_driver,
                                       mixins=local_mixins, parent=parent)
