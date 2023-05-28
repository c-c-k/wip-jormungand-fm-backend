from sqlalchemy import Engine, text, select

from jormungand.core.db import get_db_engine, UserRole, Tables


def test_get_engine(db_engine):
    """Test that get_engine correctly gets an engine

    Test that as per sqlalchemy recommendations only one engine is used
    Test that the engine uses a test database
    """
    assert isinstance(db_engine, Engine)
    assert db_engine is get_db_engine()
    assert 'test' in str(db_engine.url)


def test_engine_uses_psycopg2(db_engine):
    """Test that sqlalchemy uses psycopg2 as a backend

    This test is meant to be a reminder that this project
    is not currently tested against different DBMS and drivers
    and might thus contain some functionality that is specifically
    dependent on psycopg2.
    """
    assert db_engine.driver == 'psycopg2'


def test_init_db_init_roles(db_engine):
    with db_engine.begin() as conn:
        table = Tables.user_roles
        db_user_roles = conn.execute(select(table)).all()
        assert len(db_user_roles) == len(UserRole)
        for role_id, role_name in db_user_roles:
            assert UserRole[role_name].value == role_id

