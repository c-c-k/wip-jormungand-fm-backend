from logging import getLogger
from random import randint

import pytest
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError

from jormungand.core.config import config
from jormungand.core.logging import load_logging_configuration
from jormungand.core import db

logger = getLogger(__name__)

_cleanup_db_engine: Engine | None = None


def _init_cleanup_db_engine():
    global _cleanup_db_engine
    _cleanup_db_engine = create_engine(
        URL.create(
            database=config['cleanup_database_name'], **config['test_db']),
        isolation_level='AUTOCOMMIT')


@pytest.fixture
def temp_db_engine(set_test_settings, set_test_logging):
    global _temp_db_count
    if _cleanup_db_engine is None:
        _init_cleanup_db_engine()
    with _cleanup_db_engine.begin() as conn:
        create_attempts = 1
        max_create_attempts = 5
        while True:
            try:
                temp_db_name = f"tempdb_{randint(0,65535)}"
                conn.execute(text(f'CREATE DATABASE {temp_db_name};'))
            except OperationalError:
                if create_attempts <= max_create_attempts:
                    logger.error(
                        "failed to create temporary database with name:"
                        f" {temp_db_name} "
                        f", attempt {create_attempts}/{max_create_attempts}"
                    )
                    continue
                logger.error(
                    "failed to create temporary database with name:"
                    f" {temp_db_name} failed {max_create_attempts}"
                    " attempts, aborting!"
                )
                break
            else:
                break
        engine_ = create_engine(
            URL.create(database=temp_db_name, **config['test_db']),
            echo=False, echo_pool=False)
        yield engine_
        engine_.dispose()
        conn.execute(
                text(f'DROP DATABASE IF EXISTS {temp_db_name} (FORCE);'),
                )


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    config.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(scope="session", autouse=True)
def set_test_logging(set_test_settings):
    """Set global logging configuration for tests"""
    load_logging_configuration()


@pytest.fixture
def db_engine(temp_db_engine):
    db.load_db_engine(temp_db_engine)
    db.init_db()
    yield temp_db_engine

