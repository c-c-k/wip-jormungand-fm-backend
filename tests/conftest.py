import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from jormungand.utils.config import config
from jormungand.utils.logging import load_logging_configuration
from jormungand.dal.db import get_db_engine, init_db

_cleanup_db_engine = None

# .. note::
#       the following doesn't work because postgresql doesn't 
#       allow dropping a database from within a stored procedure.
#
# CLEANUP_DB_STORED_PROCEDURE = """
# CREATE OR REPLACE PROCEDURE cleanup_test_db(_test_db_name text)
# LANGUAGE SQL
# AS $$
#     DROP DATABASE IF EXISTS _test_db_name (FORCE);
#     CREATE DATABASE _test_db_name;
# $$;
# """.strip()


def _init_cleanup_db_engine():
    global _cleanup_db_engine
    _cleanup_db_engine = create_engine(
            URL.create(**config['cleanup_database']),
            isolation_level='AUTOCOMMIT')
# .. note::
#       the following doesn't work because postgresql doesn't 
#       allow dropping a database from within a stored procedure.
#
    # with _cleanup_db_engine.connect() as conn:
    #     query = text(CLEANUP_DB_STORED_PROCEDURE)
    #     conn.execute(query)
    #     conn.commit()


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
def db(set_test_settings):
    _cleanup_test_db(config['database.database'])
    init_db()
    yield get_db_engine()


