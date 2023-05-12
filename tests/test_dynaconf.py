from jormungand import settings


def test_dynaconf_is_in_testing_env():
    assert settings.env_name == 'testing'

