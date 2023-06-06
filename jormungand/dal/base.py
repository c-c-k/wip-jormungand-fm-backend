"""
TODO: dal.user module docstring
"""
import re

from sqlalchemy import (
        Connection, Table, select, insert,
        update as sa_update, delete as sa_delete)
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError

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

# TODO: STOPPED AT: trying to decide if get operations should return
#       data/raise exception like they do now or return status dict
#       like I'm thinking to do with the CUD operations.

def _gen_unexpected_err_info(error: Exception, **kwargs) -> dict:
    return {
            "status": "UnexpectedError",
            "info": {
                "error_type": error.__class__,
                "error_message": error.args[0],
                **kwargs
                }
            }


def _gen_duplication_err_info(error: Exception, table: Table) -> dict:
    column_name, value = re.search(
            r"DETAIL:  Key \(([^)+])\)=\(([^)+])\) already exists."
            ).groups
    return {
            "status": "DuplicationError",
            "info": {
                "table": table.name,
                "column": column_name,
                "value": value
                }
            }


def _insert_one(
        conn: Connection, table: Table, id_c_name: str, data: dict
        ) -> dict:
    stmt = insert(table).values(data).returning(table)
    try:
        result = {
                "status": "success",
                "data": conn.execute(stmt, data).mappings().one()
                }
    except IntegrityError as e:
        if "duplicate key value violates unique" in e.args[0]:
            result = _gen_duplication_err_info(
                    err_msg=e.args[0], table_name=table.name,
                    data=data, action="insert")
        else:
            result = _gen_unexpected_err_info(
                    err_msg=e.args[0], table_name=table.name, data=data)
    except SQLAlchemyError:
        result = _gen_unexpected_err_info(
                err_msg=e.args[0], table_name=table.name, data=data)
    return result


# def _insert_one(
#         conn: Connection, table: Table, id_c_name: str, data: dict
#         ) -> dict:
#     stmt = insert(table).values(data).returning(table)
#     try:
#         result = conn.execute(stmt, data).mappings().one()
#     except (IntegrityError, DataError) as e:
#         raise e
#         if "duplicate key" in e.args[0]:
#             raise DuplicateKeyError(table_name=table.name,
#                                     column_name=id_c_name,
#                                     value=data[id_c_name])
#         else:
#             raise InvalidDataError(e.args[0])
#     return dict(result)


def add_one(table: str | Table, id_c_name: str, data: dict) -> dict:
    table = db.get_table(table)
    with db.get_db_connection() as conn:
        return _insert_one(conn, table, id_c_name, data)


# def add_one(table: str | Table, id_c_name: str, data: dict) -> dict:
#     table = db.get_table(table)
#     with db.get_db_connection() as conn:
#         stmt = insert(table).values(data).returning(table)
#         try:
#             result = conn.execute(stmt, data).mappings().one()
#         except (IntegrityError, DataError) as e:
#             if "duplicate key" in e.args[0]:
#                 raise DuplicateKeyError(table_name=table.name,
#                                         column_name=id_c_name,
#                                         value=data[id_c_name])
#             else:
#                 raise InvalidDataError(e.args[0])
#         return dict(result)


def safe_add_many(
        table: str | Table, id_c_name: str, data: list[dict]
        ) -> list[dict]:
    """"safely" adds multiple entries

    new entries with valid data are added and returned
    entries that already exist or that contain invalid data
    are silently discarded
    """
    table = db.get_table(table)
    new_data = []
    with db.get_db_connection() as conn:
        for entry in data:
            try:
                inserted_data = _insert_one(conn, table, id_c_name, entry)
            except (DuplicateKeyError, InvalidDataError):
                continue
            new_data.append(inserted_data)
    return new_data


# TODO: if/when needed
# def bulk_add_many(
#         table: str | Table, id_c_name: str, data: list[dict]
#         ) -> list[dict]:
#     input_ids = [entry[id_c_name] for entry in data]
#     table = db.get_table(table)
#     with db.get_db_connection() as conn:
#         stmt = (
#                 select(table.c[id_c_name])
#                 .where(table.c[id_c_name].in_(input_ids))
#                 )
#         result = conn.execute(stmt).all()
#         existing_ids = set(row[0] for row in result)
#         new_ids = set(input_ids) - existing_ids
#         new_data = [
#                 entry for entry in data
#                 if entry[id_c_name] in new_ids
#                 ]
#         if new_data != []:
#             stmt = insert(table).values(new_data).returning(table)
#             result = conn.execute(stmt).mappings().all()
#             new_data = [dict(row) for row in result]
#         return new_data


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
