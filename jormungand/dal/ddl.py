"""
TODO: ddl module docstring
"""

from pathlib import Path

from sqlalchemy import text

from jormungand.core.logging import get_logger
from jormungand.core import db

logger = get_logger(__name__)

_SQL_DIR = Path(__file__).parent.joinpath('sql')


def init_db():
    """TODO: Docstring for init_db. """

    # TODO: existing db handling
    with _SQL_DIR.joinpath('./sql/schema.sql').open() as f:
        schema = text(f.read())
    with _SQL_DIR.joinpath('./sql/stored_procedures.sql').open() as f:
        stored_procedures = text(f.read())
    with db.get_connection() as conn:
        conn.execute(schema)
        conn.execute(stored_procedures)
    
