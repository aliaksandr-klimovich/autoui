class AutoUIException(Exception):
    pass


class AutoUIWarning(Warning):
    pass


class InvalidLocator(AutoUIException):
    pass


class AttributeNotPermitted(AutoUIException):
    pass


class MethodNotOverridden(AutoUIException):
    pass


class InvalidWebElementInstance(AutoUIWarning):
    pass


class DebugException(AutoUIException):
    """
    for debug purposes
    """
    pass
