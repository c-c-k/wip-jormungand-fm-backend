"""
TODO: tests.dal.test_ddl module docstring
"""

from jormungand.dal.ddl import UserRole


def test_init_db_init_roles(db_conn):
    with db_conn as conn:
        db_user_roles = conn.execute("""
        SELECT * FROM user_roles;
        """).mappings()
        assert len(db_user_roles) == len(UserRole)
        for db_user_role in db_user_roles:
            assert (db_user_role['id']
                    == UserRole[db_user_role['role_name']].value)
