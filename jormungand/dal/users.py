"""
TODO: dal.user module docstring
"""

from sqlalchemy import select

from jormungand.core import db
from jormungand.core.exceptions import (
    DataNotFoundError)
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
 

# def add(new_users):
#     """Adds one or more new users"""
#     with get_db_connection() as conn:
#         conn.execute(text("""
#         INSERT INTO users
#             ( id, user_role, username, password, email, avatar_url )
#         VALUES
#             ( :id, :user_role, :username, :password, :email, :avatar_url )
#         """), new_users)
 

