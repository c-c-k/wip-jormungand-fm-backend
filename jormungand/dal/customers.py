"""
TODO: dal.user module docstring
"""

from . import base
from jormungand.core import db
from jormungand.core.logging import get_logger

logger = get_logger(__name__)

TABLE_NAME = db.TN_CUSTOMERS
ID_C_NAME = "user_id"


def get_by_id(id_):
    return base.get_by_id(TABLE_NAME, ID_C_NAME, id_)


def get_all():
    return base.get_all(TABLE_NAME)


def add_one(data: dict) -> dict:
    return base.add_one(TABLE_NAME, ID_C_NAME, data)


def add_many(data: list[dict]) -> list[dict]:
    return base.add_many(TABLE_NAME, ID_C_NAME, data)


def update(data: dict) -> dict:
    return base.update(TABLE_NAME, ID_C_NAME, data)


def delete(id_: int):
    return base.delete(TABLE_NAME, ID_C_NAME, id_)
