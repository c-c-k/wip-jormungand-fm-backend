from jormungand import config


def test_dynaconf_is_in_testing_env():
    assert config.env_name == 'testing'

