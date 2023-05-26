"""
TODO: tests.dal.test_ddl module docstring
"""

from sqlalchemy import text
from jormungand.dal.ddl import UserRole


def test_init_db_init_roles(db_conn):
    with db_conn as conn:
        db_user_roles = conn.execute(text("""
        SELECT * FROM user_roles;
        """)).all()
        assert len(db_user_roles) == len(UserRole)
        for role_id, role_name in db_user_roles:
            assert UserRole[role_name].value == role_id
