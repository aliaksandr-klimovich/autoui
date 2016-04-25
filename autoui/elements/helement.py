from autoui.elements.abstract import Element
from autoui.elements.mixins import WaitingAndScrollingElement


class HElement(Element):
    def __init__(self, locator=None, search_with_driver=None, mixins=None, parent=None):
        local_mixins = (WaitingAndScrollingElement, )
        if mixins:
            local_mixins = mixins + local_mixins
        super(HElement, self).__init__(locator=locator, search_with_driver=search_with_driver,
                                       mixins=local_mixins, parent=parent)
