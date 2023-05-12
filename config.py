"""Project Dynaconf based settings loading module

For details, see https://www.dynaconf.com/configuration
"""

import os

from dynaconf import Dynaconf

settings = Dynaconf(
    core_loaders=['YAML'],
    root_path=os.path.dirname(os.path.realpath(__file__)),
    settings_files=['settings.yaml', '.secrets.yaml'],
    environments=True,
    envvar_prefix="JORMUNGAND",
    env_switcher='ENV_FOR_JORMUNGAND',
    load_dotenv=True,
)
