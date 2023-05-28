from copy import deepcopy

import pytest
from sqlalchemy import Engine, text, select

from jormungand.core.db import get_db_engine, UserRole, Tables
from tests.utils import setup_dataset, compare_dataset_all

DATASET_TEST_SETUP_DATASET = {
    'airline_companies': {
        'airline_company': {
            'id': 1,
            'country_id': 1,
            'user_id': 1,
            'name': 'airline_company',
        },
    },
    'countries': {
        'country': {
            'id': 1,
            'name': 'country',
        },
    },
    'users': {
        'user': {
            'id': 1,
            'user_role': int(UserRole.CUSTOMER),
            'username': 'user',
            'password': 'pass',
            'email': 'user@email.com',
        },
    }
}


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


@pytest.mark.current
def test_dataset_testing_helper_utils(db_engine):
    with db_engine.begin() as conn:
        dataset = DATASET_TEST_SETUP_DATASET
        setup_dataset(conn, dataset)
        compare_dataset_all(conn, dataset)
        table = Tables.users
        entry = deepcopy(dataset[table.name]['user'])
        entry['username'] = 'wrong name'
        stmt = select(table).filter_by(**entry)
        result = conn.execute(stmt).all()
        assert len(result) == 0
        
