"""db connection and access functions

TODO: better documentation for db module
TODO: error handling
"""
import contextlib
from enum import IntEnum, Enum
import itertools
from pathlib import Path

from sqlalchemy import (
    create_engine, Engine, MetaData, Table, text, Connection)
from sqlalchemy.engine import URL

from .config import config
from .logging import get_logger, load_logging_configuration

logger = get_logger(__name__)

_SQL_DIR = Path(__file__).parent.joinpath('sql')
# Table Names
TN_USER_ROLES = 'user_roles'
TN_USERS = 'users'
TN_CUSTOMERS = 'customers'
TN_ADMINISTRATORS = 'administrators'
TN_COUNTRIES = 'countries'
TN_AIRLINE_COMPANIES = 'airline_companies'
TN_FLIGHTS = 'flights'
TN_TICKETS = 'tickets'
TABLES_LAYERED_DEPENDANCY_ORDER = {
    TN_USER_ROLES: 11, TN_COUNTRIES: 12,
    TN_USERS: 21,
    TN_CUSTOMERS: 31, TN_ADMINISTRATORS: 32, TN_AIRLINE_COMPANIES: 33,
    TN_FLIGHTS: 41,
    TN_TICKETS: 51
}

_engine: Engine | None = None
_tables: dict[str, Table] | None = None

metadata_obj = MetaData()


# class Tables:
#     """TODO: doc"""
#     # IMPORTANT: The table names in ``table_names`` must appear in their
#     #            dependency (e.g. "user_roles" must be before "users" 
#     #            because "users" has a foreign key to "user_roles".
#     table_names = ('user_roles', 'users', 'customers', 'administrators',
#                    'countries', 'airline_companies', 'flights', 'tickets')
#     # The attributes below should be initialized by a call to load_db_tables
#     # during application startup or testing setup
#     user_roles: Table = None
#     users: Table = None
#     customers: Table = None
#     administrators: Table = None
#     countries: Table = None
#     airline_companies: Table = None
#     flights: Table = None
#     tickets: Table = None
#     t_names_sort_key: dict[str, int] = None
    

class UserRole(IntEnum):
    CUSTOMER = 1
    AIRLINE_COMPANY = 2
    ADMINISTRATOR = 3


# TODO: REMOVE: this seems to be redundant
# def config_sqlalchemy_logging():
#     """Configures sqlalchemy logging

#     Mostly this just sets the log-level for the sqlalchemy loggers.
#     for details see:
#     https://docs.sqlalchemy.org/en/20/core/engines.html#dbengine-logging
#     :returns: None
#     """
#     load_logging_configuration()
#     load_logging_configuration(config.logging.sqlalchemy)
#     for logger_name in ('engine', 'pool', 'dialects', 'orm'):
#         get_logger(f'sqlalchemy.{logger_name}').setLevel(
#                     config.logging)


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
    _tables = {
        table_name: Table(table_name, metadata_obj,
                          autoload_with=get_db_engine())
        for table_name in TABLES_LAYERED_DEPENDANCY_ORDER
    }
    # for table_name in TABLES_LAYERED_DEPENDANCY_ORDER.keys():
    #     table = Table(table_name, metadata_obj, autoload_with=get_db_engine())
    #     setattr(Tables, table_name, table)
    # table_names_sort_key = dict(zip(Tables.table_names, itertools.count()))
    # setattr(Tables, 't_names_sort_key', table_names_sort_key)


def get_table_by_name(table_name: str) -> Table:
    """TODO: Docstring for _init_tables.

    :returns: TODO
    """
    if _tables is None:
        load_db_tables()
    return _tables[table_name]


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
    if isinstance(table, str):
        table = get_table_by_name(table)
    return tuple(column.name for column in table.columns)


# TODO: REMOVE MAYBE: this might be redundant
# def get_tables(table_names: list[str] | str) -> dict[str, Table] | Table:
#     global _tables
#     if _tables is None:
#         _tables = {
#             table_name: Table(table_name, metadata_obj,
#                               autoload_with=get_db_engine())
#             for table_name in TABLE_NAMES
#         }

#     if isinstance(table_names, str):
#         tables = _tables[table_names]
#     else:
#         tables = {table_name: _tables[table_name]
#                   for table_name in table_names}
#     return tables


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


def init_db():
    """TODO: Docstring for init_db. """

    # TODO: existing db handling
    schema = text(_SQL_DIR.joinpath('./schema.sql').read_text())
    stored_procedures = text(
            _SQL_DIR.joinpath('./stored_procedures.sql').read_text())
    with get_db_connection() as conn:
        conn.execute(schema)
        conn.execute(stored_procedures)
        conn.execute(text("""
        INSERT INTO user_roles (id, role_name) VALUES (:id, :rolename);
        """), [
            {'id': int(user_role), 'rolename': user_role.name} 
            for user_role in UserRole]
        )
 
