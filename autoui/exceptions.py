class AutoUIException(Exception):
    pass


class AutoUIWarning(Warning):
    pass


class InvalidLocator(AutoUIException):
    pass


class InvalidWebElementInstance(AutoUIWarning):
    pass


class DebugException(AutoUIException):
    pass


class PropertyInstantiateException(Exception):
    pass
