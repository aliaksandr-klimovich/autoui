from tests.test_helpers_global_config import GlobalConfig


def change_config():
    GlobalConfig.A = False


def get_config_attribute():
    return GlobalConfig.A
