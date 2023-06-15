"""Data access functionality related to countries.

"""

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
