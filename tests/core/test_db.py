from copy import deepcopy

import pytest
from sqlalchemy import Engine, text, select

from jormungand.core import db
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
            'user_role': int(db.UserRole.CUSTOMER),
            'username': 'user',
            'password': 'pass',
            'email': 'user@email.com',
        },
    }
}


def test_get_engine(func_db):
    """Test that get_engine correctly gets an engine

    Test that as per sqlalchemy recommendations only one engine is used
    Test that the engine uses a test database
    """
    assert isinstance(func_db, Engine)
    assert func_db is db.get_db_engine()
    assert 'test' in str(func_db.url)


def test_engine_uses_psycopg2(func_db):
    """Test that sqlalchemy uses psycopg2 as a backend

    This test is meant to be a reminder that this project
    is not currently tested against different DBMS and drivers
    and might thus contain some functionality that is specifically
    dependent on psycopg2.
    """
    assert func_db.driver == 'psycopg2'


def test_init_db_init_roles(func_db):
    with func_db.begin() as conn:
        table = db.get_table_by_name(db.TN_USER_ROLES)
        db_user_roles = conn.execute(select(table)).all()
        assert len(db_user_roles) == len(db.UserRole)
        for role_id, role_name in db_user_roles:
            assert db.UserRole[role_name].value == role_id


def test_dataset_testing_helper_utils(func_db):
    with func_db.begin() as conn:
        dataset = DATASET_TEST_SETUP_DATASET
        setup_dataset(conn, dataset)
        compare_dataset_all(conn, dataset)
        table = db.get_table_by_name(db.TN_USERS)
        entry = deepcopy(dataset[table.name]['user'])
        entry['username'] = 'wrong name'
        stmt = select(table).filter_by(**entry)
        result = conn.execute(stmt).all()
        assert len(result) == 0
        
