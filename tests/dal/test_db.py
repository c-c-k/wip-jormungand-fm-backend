from sqlalchemy import Engine, text

from jormungand.dal import db


def test_get_engine():
    """Test that get_engine correctly gets an engine

    Test that as per sqlalchemy recommendations only one engine is used
    Test that the engine uses a test database
    """
    engine = db.get_db_engine()
    assert isinstance(engine, Engine)
    assert engine is db.get_db_engine()
    assert 'test' in str(engine.url)


def test_engine_uses_psycopg2():
    """Test that sqlalchemy uses psycopg2 as a backend

    This test is meant to be a reminder that this project
    is not currently tested against different DBMS and drivers
    and might thus contain some functionality that is specifically
    dependent on psycopg2.
    """
    engine = db.get_db_engine()
    assert engine.driver == 'psycopg2'

