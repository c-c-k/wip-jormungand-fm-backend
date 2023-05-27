import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from jormungand.core.config import config
from jormungand.core.logging import load_logging_configuration
from jormungand.core.db import init_db, get_db_connection

_cleanup_db_engine = None


def _init_cleanup_db_engine():
    global _cleanup_db_engine
    _cleanup_db_engine = create_engine(
            URL.create(**config['cleanup_database']),
            isolation_level='AUTOCOMMIT')


def _cleanup_test_db(test_db_name):
    if _cleanup_db_engine is None:
        _init_cleanup_db_engine()
    with _cleanup_db_engine.begin() as conn:
        # TODO: add some sort of manual counter sql injection 
        #       validation to test_db_name
        conn.execute(
                text(f'DROP DATABASE IF EXISTS {test_db_name} (FORCE);'),
                )
        conn.execute(text(f'CREATE DATABASE {test_db_name};'))
        conn.commit()


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    config.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(scope="session", autouse=True)
def set_test_logging(set_test_settings):
    """Set global logging configuration for tests"""
    load_logging_configuration()


@pytest.fixture
def db_conn(set_test_settings):
    _cleanup_test_db(config['database.database'])
    init_db()
    yield get_db_connection()
 

