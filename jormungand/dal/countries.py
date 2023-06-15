"""Data access functionality related to countries.

"""

from sqlalchemy import (
        Connection, Table, select, insert, text,
        update as sa_update, delete as sa_delete)
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError

from . import base
from jormungand.core import db
from jormungand.core.logging import get_logger

logger = get_logger(__name__)

_TABLE_NAME = db.TN_COUNTRIES
_ID_C_NAME = "country_id"


def countries_init_data(data: list[dict]):
    """Remove all existing countries data from the db and add new data instead.

    :data: The new countries data that is to be inserted into the database.
    :returns: None
    """
    base.init_table_data(_TABLE_NAME, data)


def countries_get_code_to_id_map() -> dict[str, int]:
    """Get a mapping of country codes to their db primary keys.

    :returns: dictionary {<country_code>: <country_id>}
    """
    table = db.get_table(_TABLE_NAME)
    with db.get_db_connection() as conn:
        stmt = select(table.c['code'], table.c['country_id'])
        result = conn.execute(stmt).all()
        return {code: pk for code, pk in result}


# def get_by_id(id_):
#     return base.get_by_id(_TABLE_NAME, _ID_C_NAME, id_)


# def get_all():
#     return base.get_all(_TABLE_NAME)


# def add_one(data: dict) -> dict:
#     return base.add_one(_TABLE_NAME, _ID_C_NAME, data)


# def countries_add_many(data: list[dict]) -> list[dict]:
#     return base.safe_add_many(_TABLE_NAME, _ID_C_NAME, data)


# def update(data: dict) -> dict:
#     return base.update(_TABLE_NAME, _ID_C_NAME, data)
