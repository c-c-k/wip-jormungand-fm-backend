"""db connection and access functions

TODO: better documentation for db module
TODO: error handling
"""
import contextlib
from enum import IntEnum
from pathlib import Path

from sqlalchemy import (
    create_engine, Engine, Connection, MetaData, Table, text, insert)
from sqlalchemy.engine import URL

from .config import config
from .exceptions import MiscError
from .logging import get_logger

logger = get_logger(__name__)
sa_loggers = tuple(
    get_logger(sa_logger_name)
    for sa_logger_name in (
        "sqlalchemy.engine",
        "sqlalchemy.pool",
        "sqlalchemy.dialects",
        "sqlalchemy.orm",
    )
)

_SQL_DIR = Path(__file__).parent.joinpath('sql')
_INIT_SCHEMA = _SQL_DIR.joinpath('schema.v0.2.0.sql')

# Table Names
TN_META = 'meta'
TN_USER_ROLES = 'user_roles'
TN_USERS = 'users'
TN_CUSTOMERS = 'customers'
TN_ADMINISTRATORS = 'administrators'
TN_COUNTRIES = 'countries'
TN_AIRPORTS = 'airports'
TABLES_LAYERED_DEPENDANCY_ORDER = {
    TN_USER_ROLES: 11, TN_COUNTRIES: 12, TN_META: 13,
    TN_USERS: 21, TN_AIRPORTS: 22,
    TN_CUSTOMERS: 31, TN_ADMINISTRATORS: 32,
}

_engine: Engine | None = None
_tables: dict[str, Table] | None = None

metadata_obj = MetaData()


class UserRole(IntEnum):
    ADMINISTRATOR = 1
    CUSTOMER = 2


def set_level_sqlalchemy_loggers(level: str):
    """Set the log-level for the sqlalchemy loggers.

    for details see:
    https://docs.sqlalchemy.org/en/20/core/engines.html#dbengine-logging
    """
    for sa_logger in sa_loggers:
        sa_logger.setLevel(level)


def load_db_engine(testing_engine: Engine = None):
    """TODO: Docstring

    :returns: TODO
    """
    global _engine
    if testing_engine is None:
        _engine = create_engine(URL.create(**config.database),
                                echo=False, echo_pool=False)
    else:
        _engine = testing_engine


def get_db_engine() -> Engine:
    """TODO: Docstring for get_engine.

    :returns: TODO
    """
    if _engine is None:
        load_db_engine()
    return _engine


def load_db_tables():
    """TODO: Docstring

    :returns: TODO
    """
    global _tables
    set_level_sqlalchemy_loggers("WARN")
    _tables = {
        table_name: Table(table_name, metadata_obj,
                          autoload_with=get_db_engine())
        for table_name in TABLES_LAYERED_DEPENDANCY_ORDER
    }
    set_level_sqlalchemy_loggers("DEBUG")


def get_table(table: str | Table) -> Table:
    """TODO: Docstring for _init_tables.

    :returns: TODO
    """
    if _tables is None:
        load_db_tables()
    if isinstance(table, str):
        _table = _tables[table]
    else:
        _table = table
    return _table


def table_name_sort_key(table_name):
    """TODO: Docstring for table_name_sort_key.

    :table_name: TODO
    :returns: TODO

    """
    return TABLES_LAYERED_DEPENDANCY_ORDER[table_name]


def get_colum_names(table: str | Table) -> list[str]:
    """TODO: Docstring for _init_tables.

    :returns: TODO
    """
    table = get_table(table)
    return tuple(column.name for column in table.columns)


@contextlib.contextmanager
def get_db_connection(begin_once: bool = True) -> Connection | object:
    """Get an sqlalchemy database connection

    transaction context:
        - begin once: implicitly commit at end of context
        - normal: commit only on explicit calls to commit()
    :begin_mode: True (default) for begin once transaction context,
                 False for normal transaction context.
    :returns: A database connection that should usually be used
              in a transaction context
              (i.e. ``with get_engine as conn:...``)
              .. note:: the exact returned object might not be an actual
                        Connection but a wrapper around the Connection,
                        however, as long as it's used in a with context the 
                        behavior should be the same a Connection object.
    """
    try:
        if begin_once:
            connection = get_db_engine().begin
        else:
            connection = get_db_engine().connect
        with connection() as conn:
            yield conn
    except Exception:
        raise
    finally:
        pass


def init_db(confirm_init_db=False):
    """.. IMPORTANT::
            for the moment this is only meant for unittests,
            development (and production) databases should be adjusted
            manually or via migration scripts (which are also written manually
            for the moment)
            """

    if not confirm_init_db:
        raise MiscError("""
        `init_db()` can be a destructive and hard to reverse action if called
        accidentally when the database already contains data, if you are sure
        of what you are doing invoke this function with:
        `init_db(confirm_init_db=True)`
                """)

    schema = text(_INIT_SCHEMA.read_text())
    # TODO: Adjust stored procedures
    # stored_procedures = text(
    #         _SQL_DIR.joinpath('./stored_procedures.sql').read_text())
    with get_db_connection(begin_once=False) as conn:
        conn.execute(schema)
        # TODO: Adjust stored procedures to per table id names
        # conn.execute(stored_procedures)
        conn.commit()
        table = get_table(TN_USER_ROLES)
        data = [
            {'user_role_id': int(user_role), 'role_name': user_role.name}
            for user_role in UserRole
            ]
        conn.execute(insert(table), data)
        conn.commit()
 
