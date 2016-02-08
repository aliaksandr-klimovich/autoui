from unittest import TestCase

from nose.tools import eq_

from autoui.helpers import Property, PropertyInstantiateException

from tests.test_helpers_functions import get_config_attribute, change_config
from tests.test_helpers_global_config import GlobalConfig


class TestProperty(TestCase):
    def test_reset(self):
        class Config(Property):
            A = True

        eq_(Config.A, True)

        Config.A = False
        eq_(Config.A, False)

        Config.reset()
        eq_(Config.A, True)

    def test_instantiate_exception(self):
        class Config(Property):
            pass
        with self.assertRaises(PropertyInstantiateException) as e:
            Config()
        eq_(e.exception.message, 'Do not instantiate property class, it is not permitted')


class TestGlobalProperty(TestCase):
    def test_change_value_from_another_module(self):
        eq_(GlobalConfig.A, True)
        eq_(get_config_attribute(), True)

        change_config()
        eq_(GlobalConfig.A, False)
        eq_(get_config_attribute(), False)

        GlobalConfig.reset()
        eq_(GlobalConfig.A, True)
        eq_(get_config_attribute(), True)