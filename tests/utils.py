"""
TODO: DOC: tests/dataset.py
"""

import contextlib
from datetime import datetime, timedelta
from logging import getLogger
from random import randint

import pytest
from sqlalchemy import (
        create_engine, Engine, text, insert, select, exists)
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError

from jormungand.core.config import config
from jormungand.core.logging import load_logging_configuration
from jormungand.core import db

logger = getLogger(__name__)

_cleanup_db_engine: Engine | None = None

DATASET_TEMPLATE = {
    'users': {
        'customer_user_1': {
            'id': 51,
            'user_role': int(db.UserRole.CUSTOMER),
            'username': 'customer_user_1',
            'password': 'pass',
            'email': 'customer_user_1@email_1.com',
            'avatar_url': 'user_avatars/customer_user_1.png',
        },
        'airline_user_1': {
            'id': 61,
            'user_role': int(db.UserRole.AIRLINE_COMPANY),
            'username': 'airline_user_1',
            'password': 'pass',
            'email': 'airline_user_1@email_1.com',
            'avatar_url': 'user_avatars/airline_user_1.png',
        },
        'admin_user_1': {
            'id': 71,
            'user_role': int(db.UserRole.ADMINISTRATOR),
            'username': 'admin_user_1',
            'password': 'pass',
            'email': 'admin_user_1@email_1.com',
            'avatar_url': 'user_avatars/admin_user_1.png',
        },
    },
    'countries': {
        'country_1': {
            'id': 61,
            'name': 'country_1',
            'flag_url': 'country_1.png',
        },
    },
    'airline_companies': {
        'airline_company_1': {
            'id': 61,
            'country_id': 61,
            'user_id': 61,
            'name': 'airline_company_1',
        },
    },
    'customers': {
        'customer_1': {
            'id': 51,
            'user_id': 51,
            'first_name': 'customer_1_first_name',
            'last_name': 'customer_1_last_name',
            'address': 'country A, city B, street C 5551',
            'phone_number': '111 111 1111111',
            'credit_card_number': '4000000000000010',
        },
    },
    'administrators': {
        'administrator_1': {
            'id': 71,
            'user_id': 71,
            'first_name': 'administrator_1_first_name',
            'last_name': 'administrator_1_last_name',
        },
    },
    'flights': {
        'flight_template_dt_now': {
            'id': 1,
            'airline_company_id': 61,
            'origin_country_id': 81,
            'destination_country_id': 881,
            'departure_time': datetime.now(),
            'landing_time': (datetime.now() + timedelta(hours=1)),
            'remaining_tickets': 40,
        },
    },
    'tickets': {
        'ticket_template': {
            'id': 1,
            'flight_id': 1,
            'customer_id': 51,
        },
    },
}


def _init_cleanup_db_engine():
    global _cleanup_db_engine
    _cleanup_db_engine = create_engine(
        URL.create(
            database=config['cleanup_database_name'], **config['test_db']),
        isolation_level='AUTOCOMMIT')


@contextlib.contextmanager
def create_temp_db_engine():
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
                raise
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


class TempDBClassScope:
    @pytest.fixture(scope="class")
    def _engine(self):
        with create_temp_db_engine() as engine_:
            db.load_db_engine(engine_)
            db.init_db()
            yield engine_


class TempDBMethodScope:
    @pytest.fixture(scope="function")
    def _engine(self, func_db):
        yield func_db



def setup_dataset(conn, dataset: dict):
    used_table_names = sorted(
            dataset.keys(),
            key=db.table_name_sort_key)
    for table_name in used_table_names:
        table = db.get_table_by_name(table_name)
        conn.execute(
            insert(table), tuple(dataset[table_name].values()))


def compare_dataset_all(conn, dataset: dict):
    used_table_names = dataset.keys()
    for table_name in used_table_names:
        table = db.get_table_by_name(table_name)
        for entry in dataset[table_name].values():
            stmt = select(table).filter_by(**entry)
            result = conn.execute(stmt).all()
            assert len(result) == 1
