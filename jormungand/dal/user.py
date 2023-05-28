"""
TODO: dal.user module docstring
"""
import logging

from sqlalchemy import text

from jormungand.core.db import get_db_connection

logger = logging.getLogger(__name__)

COLUMNS_LIST = ['id', 'user'_'role', 'username', 'password', 'email',
        'avatar'_'url']


def add(new_users):
    """Adds one or more new users"""
    with get_db_connection() as conn:
        conn.execute(text("""
        INSERT INTO users
            ( id, user_role, username, password, email, avatar_url )
        VALUES
            ( :id, :user_role, :username, :password, :email, :avatar_url )
        """), new_users)
 

