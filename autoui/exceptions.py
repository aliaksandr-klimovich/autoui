class AutoUIException(Exception):
    pass


class AutoUIWarning(Warning):
    pass


class InvalidLocator(AutoUIException):
    pass


class AttributeNotPermitted(AutoUIException):
    pass


class InvalidWebElementInstance(AutoUIWarning):
    pass
