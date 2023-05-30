from logging import getLogger

import pytest
from sqlalchemy import create_engine, text, Engine

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


@pytest.fixture(scope='function')
def func_db():
    with create_temp_db_engine() as engine:
        db.load_db_engine(engine)
        db.init_db()
        yield engine


@pytest.fixture(scope='class')
def cls_db():
    with create_temp_db_engine() as engine:
        db.load_db_engine(engine)
        db.init_db()
        yield engine


@pytest.fixture(scope='module')
def module_db():
    with create_temp_db_engine() as engine:
        db.load_db_engine(engine)
        db.init_db()
        yield engine


@pytest.fixture(scope='session')
def session_db():
    with create_temp_db_engine() as engine:
        db.load_db_engine(engine)
        db.init_db()
        yield engine
