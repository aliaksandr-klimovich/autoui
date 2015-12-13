# class PropertyMeta(type):
#     def __init__(cls, name, bases=None, namespace=None):
#         cls._state = {k: v for k, v in namespace.items() if not k.startswith('_')}
#         super(PropertyMeta, cls).__init__(name, bases, namespace)
#
#
# class Property(object):
#     __metaclass__ = PropertyMeta
#
#     @classmethod
#     def reset(cls):
#         for k, v in cls._state.items():
#             setattr(cls, k, v)
