"""
TODO: dal.user module docstring
"""

from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from jormungand.core import db
from jormungand.core.exceptions import (
    DataNotFoundError, InvalidDataError)
from jormungand.core.logging import get_logger

logger = get_logger(__name__)

# COLUMNS_LIST = ['id', 'user'_'role', 'username', 'password', 'email',
#         'avatar'_'url']


def get_by_id(id_):
    with db.get_db_connection() as conn:
        table = db.get_table_by_name(db.TN_USERS)
        stmt = select(table).where(table.c.id == id_)
        result = conn.execute(stmt).mappings().one_or_none()
        try:
            return dict(result)
        except TypeError:
            raise DataNotFoundError(f'no user with id {id_} in database')
 

def get_all():
    with db.get_db_connection() as conn:
        table = db.get_table_by_name(db.TN_USERS)
        stmt = select(table)
        result = conn.execute(stmt).mappings().all()
        try:
            return list(dict(mapping) for mapping in result)
        except TypeError:
            raise DataNotFoundError(f'no user with id {id_} in database')
 

def add_one(data):
    """Adds one user"""
    with db.get_db_connection() as conn:
        table = db.get_table_by_name(db.TN_USERS)
        stmt = insert(table).values(data).returning(table)
        # raise Exception(str(stmt))
        try:
            result = conn.execute(stmt, data).mappings().one()
        except IntegrityError as error:
            if 'unique' in str(error):
                with db.get_db_connection() as conn:
                    stmt = (
                            select(table)
                            .where(table.c.username == data['username'])
                    )
                    result = conn.execute(stmt, data).mappings().one()
            else:
                raise InvalidDataError(str(error))
        return dict(result)
        # stmt = select(table)
        # for table_name in used_table_names:
        #     table = db.get_table_by_name(table_name)
        # conn.execute(text("""
        # INSERT INTO users
        #     ( id, user_role, username, password, email, avatar_url )
        # VALUES
        #     ( :id, :user_role, :username, :password, :email, :avatar_url )
        # """), new_users)
 

