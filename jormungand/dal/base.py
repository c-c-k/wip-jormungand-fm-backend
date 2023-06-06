"""
TODO: dal.user module docstring
"""

from sqlalchemy import (
        Table, select, insert, update as sa_update, delete as sa_delete)
from sqlalchemy.exc import NoResultFound, IntegrityError, DataError

from jormungand.core import db
from jormungand.core.exceptions import (
        DataNotFoundError, DuplicateKeyError, InvalidDataError)
from jormungand.core.logging import get_logger

logger = get_logger(__name__)


def get_by_id(table: str | Table, id_c_name: str, id_: int) -> dict:
    table = db.get_table(table)
    with db.get_db_connection() as conn:
        stmt = select(table).where(table.c[id_c_name] == id_)
        result = conn.execute(stmt).mappings().one_or_none()
        if result is not None:
            return dict(result)
        else:
            raise DataNotFoundError(table_name=table.name,
                                    column_name=id_c_name, value=id_)


def get_all(table: str) -> list[dict]:
    table = db.get_table(table)
    with db.get_db_connection() as conn:
        stmt = select(table)
        result = conn.execute(stmt).mappings().all()
        return list(dict(mapping) for mapping in result)


def add_one(table: str | Table, id_c_name: str, data: dict) -> dict:
    table = db.get_table(table)
    with db.get_db_connection() as conn:
        stmt = insert(table).values(data).returning(table)
        try:
            result = conn.execute(stmt, data).mappings().one()
        except (IntegrityError, DataError) as e:
            if "duplicate key" in e.args[0]:
                raise DuplicateKeyError(table_name=table.name,
                                        column_name=id_c_name,
                                        value=data[id_c_name])
            else:
                raise InvalidDataError(e.args[0])
        return dict(result)


def add_many(
        table: str | Table, id_c_name: str, data: list[dict]
        ) -> list[dict]:
    input_ids = [entry[id_c_name] for entry in data]
    table = db.get_table(table)
    with db.get_db_connection() as conn:
        stmt = (
                select(table.c[id_c_name])
                .where(table.c[id_c_name].in_(input_ids))
                )
        result = conn.execute(stmt).all()
        existing_ids = set(row[0] for row in result)
        new_ids = set(input_ids) - existing_ids
        new_data = [
                entry for entry in data
                if entry[id_c_name] in new_ids
                ]
        if new_data != []:
            stmt = insert(table).values(new_data).returning(table)
            result = conn.execute(stmt).mappings().all()
            new_data = [dict(row) for row in result]
        return new_data


def update(table: str | Table, id_c_name: str, data: dict) -> dict:
    table = db.get_table(table)
    with db.get_db_connection() as conn:
        stmt = (sa_update(table).where(table.c[id_c_name] == data[id_c_name])
                .values(data).returning(table))
        try:
            result = conn.execute(stmt).mappings().one()
        except NoResultFound:
            raise DataNotFoundError(table_name=table.name,
                                    column_name=id_c_name,
                                    value=data[id_c_name])
        except IntegrityError as e:
            raise InvalidDataError(e.args[0])
        return dict(result)


def delete(table: str | Table, id_c_name: str, id_: int) -> dict:
    table = db.get_table(table)
    with db.get_db_connection() as conn:
        stmt = (sa_delete(table).where(table.c[id_c_name] == id_)
                .returning(table))
        try:
            result = conn.execute(stmt).mappings().one()
        except NoResultFound:
            raise DataNotFoundError(table_name=table.name,
                                    column_name=id_c_name, value=id_)
        return dict(result)
