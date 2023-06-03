"""
TODO: dal.user module docstring
"""

from sqlalchemy import (
        select, insert, update as sa_update, delete as sa_delete)
from sqlalchemy.exc import NoResultFound

from jormungand.core import db
from jormungand.core.exceptions import DataNotFoundError
from jormungand.core.logging import get_logger

logger = get_logger(__name__)

# COLUMNS_LIST = ['id', 'user'_'role', 'username', 'password', 'email',
#         'avatar'_'url']


def get_by_id(id_):
    with db.get_db_connection() as conn:
        table = db.get_table(db.TN_USERS)
        stmt = select(table).where(table.c.id == id_)
        result = conn.execute(stmt).mappings().one_or_none()
        try:
            return dict(result)
        except TypeError:
            raise DataNotFoundError(f"no user with id {id_} in database")


def get_all():
    with db.get_db_connection() as conn:
        table = db.get_table(db.TN_USERS)
        stmt = select(table)
        result = conn.execute(stmt).mappings().all()
        try:
            return list(dict(mapping) for mapping in result)
        except TypeError:
            raise DataNotFoundError("no users in database")


def add_one(data: dict) -> dict:
    """Adds one user"""
    table = db.get_table(db.TN_USERS)
    with db.get_db_connection() as conn:
        stmt = insert(table).values(data).returning(table)
        result = conn.execute(stmt, data).mappings().one()
        return dict(result)


def add_many(data: list[dict]) -> list[dict]:
    input_user_names = [entry["username"] for entry in data]
    table = db.get_table(db.TN_USERS)
    with db.get_db_connection() as conn:
        stmt = (
                select(table.c.username)
                .where(table.c.username.in_(input_user_names))
                )
        result = conn.execute(stmt).all()
        existing_usernames = set(row[0] for row in result)
        new_usernames = set(input_user_names) - existing_usernames
        new_users_data = [
                entry for entry in data
                if entry["username"] in new_usernames
                ]
        if new_users_data != []:
            stmt = insert(table).values(new_users_data).returning(table)
            result = conn.execute(stmt).mappings().all()
            new_users_data = [dict(row) for row in result]
        return new_users_data


def update(data: dict) -> dict:
    table = db.get_table(db.TN_USERS)
    with db.get_db_connection() as conn:
        stmt = (sa_update(table).where(table.c.id == data["id"]).values(data)
                .returning(table))
        try:
            result = conn.execute(stmt).mappings().one()
        except NoResultFound:
            raise DataNotFoundError(
                    f"no user with id {data['id']} in database")
        return dict(result)


def delete(user_id: int):
    table = db.get_table(db.TN_USERS)
    with db.get_db_connection() as conn:
        stmt = sa_delete(table).where(table.c.id == user_id).returning(table)
        try:
            result = conn.execute(stmt).mappings().one()
        except NoResultFound:
            raise DataNotFoundError(
                    f"no user with id {user_id} in database")
        return dict(result)
