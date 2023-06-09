"""Project Dynaconf based configuration loading module

For details, see https://www.dynaconf.com/configuration
"""

from dynaconf import Dynaconf

config = Dynaconf(
    core_loaders=['YAML'],
    settings_files=['settings.yaml', 'logging_settings.yaml', '.secrets.yaml'],
    environments=True,
    envvar_prefix="JORMUNGAND",
    env_switcher='ENV_FOR_JORMUNGAND',
    load_dotenv=True,
)
