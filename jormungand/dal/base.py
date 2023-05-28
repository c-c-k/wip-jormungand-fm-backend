"""
TODO: dal.base module docstring
"""

from enum import IntEnum
import logging
from pathlib import Path

from sqlalchemy import (
    text, MetaData, Table, insert)

from jormungand.core.db import get_db_connection, get_db_engine

logger = logging.getLogger(__name__)


def insert_(table_name, entries):
    with get_db_connection() as conn:
        conn.execute(insert(table_name), entries)
