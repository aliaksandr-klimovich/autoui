from autoui.exceptions import PropertyInstantiateException


class PropertyMeta(type):
    def __init__(cls, name, bases=None, namespace=None):
        cls._initial_state = {k: v for k, v in namespace.items() if not k.startswith('_') and not callable(v)}
        super(PropertyMeta, cls).__init__(name, bases, namespace)
    
    def __iter__(cls):
        d = {k: v for k, v in cls.__dict__.items() if not k.startswith('_') and not callable(v)}
        for k, v in d.items():
            yield {k: v}


class Property(object):
    __metaclass__ = PropertyMeta

    def __new__(cls, *args, **kwargs):
        raise PropertyInstantiateException('Do not instantiate property class, it is not permitted')

    @classmethod
    def reset(cls):
        for k, v in cls._initial_state.items():
            setattr(cls, k, v)
