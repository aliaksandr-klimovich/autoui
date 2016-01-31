from autoui.exceptions import PropertyInstantiateException


class PropertyMeta(type):
    def __init__(cls, name, bases=None, namespace=None):
        cls._initial_state = {k: v for k, v in namespace.items() if not k.startswith('_')}
        super(PropertyMeta, cls).__init__(name, bases, namespace)


class Property(object):
    __metaclass__ = PropertyMeta

    def __new__(cls, *args, **kwargs):
        raise PropertyInstantiateException('Do not instantiate property class, it is not permitted')

    @classmethod
    def reset(cls):
        for k, v in cls._initial_state.items():
            setattr(cls, k, v)
