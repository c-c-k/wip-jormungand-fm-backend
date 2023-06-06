"""
TODO: dal.user module docstring
"""

from sqlalchemy import (
        select, insert, update as sa_update, delete as sa_delete)
from sqlalchemy.exc import NoResultFound, IntegrityError

from jormungand.core import db
from jormungand.core.exceptions import (
        DataNotFoundError, DuplicateKeyError, InvalidDataError)
from jormungand.core.logging import get_logger

logger = get_logger(__name__)


def get_by_id(user_id):
    with db.get_db_connection() as conn:
        table = db.get_table(db.TN_ADMINISTRATORS)
        stmt = select(table).where(table.c.user_id == user_id)
        result = conn.execute(stmt).mappings().one_or_none()
        try:
            return dict(result)
        except TypeError:
            raise DataNotFoundError(
                    f"no administrator with id {user_id} in database")


def get_all():
    with db.get_db_connection() as conn:
        table = db.get_table(db.TN_ADMINISTRATORS)
        stmt = select(table)
        result = conn.execute(stmt).mappings().all()
        try:
            return list(dict(mapping) for mapping in result)
        except TypeError:
            raise DataNotFoundError("no users in database")


def add_one(data: dict) -> dict:
    """Adds one administrator"""
    table = db.get_table(db.TN_ADMINISTRATORS)
    with db.get_db_connection() as conn:
        stmt = insert(table).values(data).returning(table)
        try:
            result = conn.execute(stmt, data).mappings().one()
        except IntegrityError as e:
            if "duplicate key" in e.args[0]:
                raise DuplicateKeyError(
                        f"Administrator with id {data['user_id']}"
                        "already exists")
            else:
                raise InvalidDataError(e.args[0])
        return dict(result)


def add_many(data: list[dict]) -> list[dict]:
    input_user_ids = [entry["user_id"] for entry in data]
    table = db.get_table(db.TN_ADMINISTRATORS)
    with db.get_db_connection() as conn:
        stmt = (
                select(table.c.user_id)
                .where(table.c.user_id.in_(input_user_ids))
                )
        result = conn.execute(stmt).all()
        existing_userids = set(row[0] for row in result)
        new_userids = set(input_user_ids) - existing_userids
        new_users_data = [
                entry for entry in data
                if entry["user_id"] in new_userids
                ]
        if new_users_data != []:
            stmt = insert(table).values(new_users_data).returning(table)
            result = conn.execute(stmt).mappings().all()
            new_users_data = [dict(row) for row in result]
        return new_users_data


def update(data: dict) -> dict:
    table = db.get_table(db.TN_ADMINISTRATORS)
    with db.get_db_connection() as conn:
        stmt = (sa_update(table).where(table.c.user_id == data["user_id"])
                .values(data).returning(table))
        try:
            result = conn.execute(stmt).mappings().one()
        except NoResultFound:
            raise DataNotFoundError(
                    f"no user with id {data['user_id']} in database")
        return dict(result)


def delete(user_id: int):
    table = db.get_table(db.TN_ADMINISTRATORS)
    with db.get_db_connection() as conn:
        stmt = (sa_delete(table).where(table.c.user_id == user_id)
                .returning(table))
        try:
            result = conn.execute(stmt).mappings().one()
        except NoResultFound:
            raise DataNotFoundError(
                    f"no user with id {user_id} in database")
        return dict(result)
