"""Helper utils for data in db related tests.

The expected dataset format is::

    {
        "<table name>":
            <data>[,]
            [...]
    }

The expected data format is::

    {
        <entry id>: {
            "<field(column) name>": <field(column) value>[,]
            [...]
        }[,]
        [...]
    }

.. NOTE:: The <entry id> should usually be an integer that is equal
    to the given/expected row id of the entry in db table.

Example::

DATASET_EXAMPLE = {
    'users': {
        '1': {
            'user_id': 1,
            'user_role': int(db.UserRole.CUSTOMER),
            'username': 'customer_user_1',
            'password': 'pass',
            'email': 'customer_user_1@email_1.com',
            'avatar_url': 'user_avatars/customer_user_1.png',
        },
        '2': {
            'user_id': 2,
            'user_role': int(db.UserRole.CUSTOMER),
            'username': 'customer_user_2',
            'password': 'pass',
            'email': 'customer_user_2@email_2.com',
            'avatar_url': 'user_avatars/customer_user_2.png',
        },
    },
    'customers': {
        '1': {
            'user_id': 1,
            'first_name': 'customer_1_first_name',
            'last_name': 'customer_1_last_name',
            'address': 'country A, city B, street C 5551',
            'phone_number': '111 111 1111111',
            'credit_card_number': '4000000000000010',
        },
    },
}
"""

from copy import deepcopy
from logging import getLogger

from sqlalchemy import (
        Engine, insert, select, Table)

from jormungand.core import db

logger = getLogger(__name__)


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


def db_load_dataset(
        engine_: Engine, dataset: dict, *, remove_apk: bool = True,
        load_to_db: bool = True, return_copy: bool = True,
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

    :engine_: The sqlalchemy engine that can be used to access the temp db.
    :dataset: The dataset to be loaded into the temp db.
    :remove_apk: If set to True all fields marked as autoincrementing
        primary keys in the db schema are removed from the dataset
        prior to inserting it into the db.
    :load_to_db: If set to False the dataset won't be inserted into the db
        i.e. it will only be copied and returned (remove_apk=True will
        still take affect but return_copy=False will be ignored).
    :return_copy: If set to False a copy of the dataset will not be
        returned (this is ignored if load_to_db=False).
    :returns: A copy of the dataset or None if return_copy=False.
        .. NOTE:: If remove_apk was set to true or the dataset did not
            have the primary key fields set in the first place the returned
            dataset will contain the primary keys automaticaly generated
            by the db.
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
    if return_copy:
        return dataset


def get_data_from_dataset(
        dataset: dict, table: Table | str, copy_data: bool = False) -> dict:
    """Extract the data of a specific table from a dataset.

    :dataset: The dataset from which to extract the table.
    :table: The table for which data is to be extracted.
    :copy_data: If set to true the data will be deep copied before returning.
    :returns: A dictionary containing the data of the specified table.
    """
    table = db.get_table(table)
    data = dataset[table.name]
    if copy_data:
        data = deepcopy(data)
    return data


def table_entry_count(engine_: Engine, table: str | Table) -> int:
    """Count the number of rows in the given table.

    :engine_: The sqlalchemy engine that can be used to access the temp db.
    :table: The table for which the number of rows is to be counted.
    :returns: The number of rows in the given table.
    """
    table = db.get_table(table)
    with engine_.begin() as conn:
        stmt = select(table)
        result = conn.execute(stmt).all()
        return len(result)


def data_in_table(
        engine_: Engine, data: list[dict] | dict, table: str | Table,
        reverse: bool = False
        ):
    """Check if the given data is present in the given table.

    .. NOTE:: This function directly performs assertion checks on each
        entry in the data, it does not return anything.

    :engine_: The sqlalchemy engine that can be used to access the temp db.
    :data: An entry or a list of entries to be checked for in the table.
        .. NOTE:: An entry must be a dict with keys matching the table rows.
    :table: The table in in which the data is to be checked.
    :reverse: If set to true the function logic will be reversed i.e. it
        will check that the entries are not in the table.
    :returns: None.
    """
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
    """Check if the given dataset is present in the db.

    This function is a wrapper that calls data_in_table for each table in the dataset.

    :engine_: The sqlalchemy engine that can be used to access the temp db.
    :dataset: The dataset that is to be checked against the db.
    :returns: None.
    """
    used_table_names = dataset.keys()
    for table_name in used_table_names:
        data = dataset[table_name].values()
        data_in_table(engine_, data, table_name)
