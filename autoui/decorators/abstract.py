from types import MethodType

from autoui.elements.abstract import Fillable


def fillable(cls):
    # need to be refactored
    setattr(cls, 'fill', MethodType(Fillable.fill.im_func, None, cls))
    setattr(cls, 'get_state', MethodType(Fillable.get_state.im_func, None, cls))
    setattr(cls, '_get_names', MethodType(Fillable._get_names.im_func, None, cls))
    if not hasattr(cls, 'stop_propagation'):
        setattr(cls, 'stop_propagation', False)
    return cls
