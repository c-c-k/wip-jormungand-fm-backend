"""
TODO: DOC: tests/utils/data.py
"""

from copy import deepcopy
from datetime import datetime, timedelta
from logging import getLogger

from sqlalchemy import (
        Engine, insert, select, Table)

from jormungand.core import db

logger = getLogger(__name__)

DATASET_TEMPLATE = {
    'users': {
        'customer_user_1': {
            'user_id': 51,
            'user_role': int(db.UserRole.CUSTOMER),
            'username': 'customer_user_1',
            'password': 'pass',
            'email': 'customer_user_1@email_1.com',
            'avatar_url': 'user_avatars/customer_user_1.png',
        },
        'admin_user_1': {
            'user_id': 71,
            'user_role': int(db.UserRole.ADMINISTRATOR),
            'username': 'admin_user_1',
            'password': 'pass',
            'email': 'admin_user_1@email_1.com',
            'avatar_url': 'user_avatars/admin_user_1.png',
        },
    },
    'countries': {
        'country_1': {
            'country_id': 61,
            'name': 'country_1',
            'flag_url': 'country_1.png',
        },
    },
    'airline_companies': {
        'airline_company_1': {
            'user_id': 61,
            'country_id': 61,
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
            'flight_id': 1,
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
            'ticket_id': 1,
            'flight_id': 1,
            'customer_id': 51,
        },
    },
}


def _copy_dataset(dataset: dict, remove_apk: bool = True) -> dict:
    _dataset = deepcopy(dataset)
    if remove_apk:
        for table_name, table_entries in _dataset.items():
            table = db.get_table(table_name)
            for column in table.columns:
                if column.primary_key and column.autoincrement:
                    apk_column = column.name
                    break
            else:
                apk_column = None
            for entry in table_entries.values():
                entry.pop(apk_column, None)
    return _dataset


# def _add_full_user_data(
#         # TODO: finish add full user data, then use it for the admin tests.
#         dataset: dict, merge_name: str, merge_tables: list[str | Table]
#         ):
#     merge_tables = [db.get_table(table, name_only=True) for table in merge



def db_load_dataset(
        engine_: Engine, dataset: dict, *, remove_apk: bool = True,
        load_to_db: bool = True, return_copy: bool = True,
        add_merge: tuple[str, list[str | Table]] = None
        ) -> dict | None:
    """Load a test dataset into a temporary testing database

    .. IMPORTANT::

            For each test/set of tests that uses a given temporary database
            instance it is essential to only use either test/program side
            generated ids or database auto-generated ids.
            Mixing the two can result in the sqlalchemy/postgres engine
            going out-of-sync with the database and auto-generating ids
            that were already created by the test/program code and thus
            resulting in IntegrityErrors on the id field.
    """
    dataset = _copy_dataset(dataset, remove_apk)
    if not load_to_db:
        return dataset
    used_table_names = sorted(
            dataset.keys(),
            key=db.table_name_sort_key)
    with engine_.begin() as conn:
        for table_name in used_table_names:
            table = db.get_table(table_name)
            for entry in dataset[table_name].values():
                stmt = insert(table).values(entry).returning(table)
                result = conn.execute(stmt).mappings().one()
                entry.update(result)
    return dataset


def get_data_from_dataset(
        dataset: dict, table: Table | str, copy_data:bool = False) -> dict:
    table = db.get_table(table)
    data = dataset[table.name]
    if copy_data:
        data = deepcopy(data)
    return data


def table_entry_count(engine_: Engine, table: str | Table) -> int:
    table = db.get_table(table)
    with engine_.begin() as conn:
        stmt = select(table)
        result = conn.execute(stmt).all()
        return len(result)


def data_in_table(
        engine_: Engine, data: list[dict] | dict, table: str | Table,
        reverse: bool = False
        ):
    table = db.get_table(table)
    if isinstance(data, dict):
        data = [data]
    with engine_.begin() as conn:
        for entry in data:
            stmt = select(table).filter_by(**entry)
            result = conn.execute(stmt).all()
            if reverse:
                assert len(result) == 0, f"entry in {table.name}: {entry}"
            else:
                assert len(result) == 1, f"entry not in {table.name}: {entry}"


def dataset_in_db(engine_: Engine, dataset: dict):
    used_table_names = dataset.keys()
    for table_name in used_table_names:
        data = dataset[table_name].values()
        data_in_table(engine_, data, table_name)
