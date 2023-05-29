"""
TODO: core ducumentation
"""

from .db import load_db_engine, load_db_tables
from .logging import load_logging_configuration


# TODO: REMOVE MAYBE: core parts of the project rely on lazy 
#                     loading instead
#    """docstring for fname"""
    
# def load_core(all_=True, logging_=False, db_engine_=False, db_tables_=False):
#     """TODO: Docstring for load.

#     :load_all: TODO
#     :load_logging: TODO
#     :load_db_engine: TODO
#     :load_db_tables: TODO
#     :returns: TODO

#     """

#     # DISABLED: to be implemented if and when needed
#     # if all_ or config_:
#     #     pass

#     if all_ or logging_:
#         load_logging_configuration()

#     if all_ or db_engine_:
#         load_db_engine()

#     if all_ or db_tables_:
#         load_db_tables()

