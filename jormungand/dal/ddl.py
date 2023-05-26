"""
TODO: dal.ddl module docstring
"""

from enum import Enum
from pathlib import Path

from sqlalchemy import text

from jormungand.core.logging import get_logger
from jormungand.core import db

logger = get_logger(__name__)

_SQL_DIR = Path(__file__).parent.joinpath('sql')


class UserRole(Enum):
    CUSTOMER = 1
    AIRLINE_COMPANY = 2
    ADMINISTRATOR = 3


def init_db():
    """TODO: Docstring for init_db. """

    # TODO: existing db handling
    schema = text(_SQL_DIR.joinpath('./schema.sql').read_text())
    stored_procedures = text(
            _SQL_DIR.joinpath('./stored_procedures.sql').read_text())
    with db.get_connection() as conn:
        conn.execute(schema)
        conn.execute(stored_procedures)
        conn.execute(text("""
        INSERT INTO user_roles (id, role_name) VALUES (:id, :rolename);
        """), [
            {'id': user_role.value, 'rolename': user_role.name} 
            for user_role in UserRole]
        )
    
