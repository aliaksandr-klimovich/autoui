from datetime import timedelta

from autoui.helpers import Property


class Config(Property):
    TIMEOUT = timedelta(seconds=30)
    POLL_FREQUENCY = timedelta(seconds=0.5)
