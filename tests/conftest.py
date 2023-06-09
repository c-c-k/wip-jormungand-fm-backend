from logging import getLogger

import pytest

from jormungand.core.config import config
from jormungand.core.logging import load_logging_configuration
from jormungand.core import db
from tests.utils import create_temp_db_engine

logger = getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    config.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(scope="session", autouse=True)
def set_test_logging(set_test_settings):
    """Set global logging configuration for tests"""
    load_logging_configuration()


@pytest.fixture()
def tmp_db():
    db.set_level_sqlalchemy_loggers("WARN")
    with create_temp_db_engine() as engine:
        db.load_db_engine(engine)
        db.init_db(confirm_init_db=True)
        db.set_level_sqlalchemy_loggers("DEBUG")
        yield engine
