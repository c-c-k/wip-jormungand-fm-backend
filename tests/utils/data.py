"""
TODO: DOC: tests/utils/data.py
"""

from datetime import datetime, timedelta
from logging import getLogger

from sqlalchemy import (
        Engine, insert, select, Table)

from jormungand.core import db

logger = getLogger(__name__)

DATASET_TEMPLATE = {
    'users': {
        'customer_user_1': {
            'user_role': int(db.UserRole.CUSTOMER),
            'username': 'customer_user_1',
            'password': 'pass',
            'email': 'customer_user_1@email_1.com',
            'avatar_url': 'user_avatars/customer_user_1.png',
        },
        'airline_user_1': {
            'user_role': int(db.UserRole.AIRLINE_COMPANY),
            'username': 'airline_user_1',
            'password': 'pass',
            'email': 'airline_user_1@email_1.com',
            'avatar_url': 'user_avatars/airline_user_1.png',
        },
        'admin_user_1': {
            'user_role': int(db.UserRole.ADMINISTRATOR),
            'username': 'admin_user_1',
            'password': 'pass',
            'email': 'admin_user_1@email_1.com',
            'avatar_url': 'user_avatars/admin_user_1.png',
        },
    },
    'countries': {
        'country_1': {
            'name': 'country_1',
            'flag_url': 'country_1.png',
        },
    },
    'airline_companies': {
        'airline_company_1': {
            'country_id': 61,
            'user_id': 61,
            'name': 'airline_company_1',
        },
    },
    'customers': {
        'customer_1': {
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
            'user_id': 71,
            'first_name': 'administrator_1_first_name',
            'last_name': 'administrator_1_last_name',
        },
    },
    'flights': {
        'flight_template_dt_now': {
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
            'flight_id': 1,
            'customer_id': 51,
        },
    },
}


def db_load_dataset(engine_: Engine, dataset: dict):
    # IMPORTANT: entries in the input dataset must not contain
    #            values for auto incrementing primary keys as
    #            this would interfere with the sqlalchemy auto
    #            increment mechanism.
    used_table_names = sorted(
            dataset.keys(),
            key=db.table_name_sort_key)
    with engine_.begin() as conn:
        for table_name in used_table_names:
            table = db.get_table_by_name(table_name)
            for entry in dataset[table_name].values():
                stmt = insert(table).values(entry).returning(table)
                result = conn.execute(stmt).mappings().one()
                entry.update(result)


def data_in_table(
        engine_: Engine, data: list[dict] | dict, table: str | Table):
    if isinstance(table, str):
        table = db.get_table_by_name(table)
    if isinstance(data, dict):
        data = [data]
    with engine_.begin() as conn:
        for entry in data:
            stmt = select(table).filter_by(**entry)
            result = conn.execute(stmt).all()
            assert len(result) == 1, f"entry not in {table.name}: {entry}"


def dataset_in_db(engine_: Engine, dataset: dict):
    used_table_names = dataset.keys()
    for table_name in used_table_names:
        data = dataset[table_name].values()
        data_in_table(engine_, data, table_name)
