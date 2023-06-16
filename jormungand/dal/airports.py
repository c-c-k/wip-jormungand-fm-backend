"""Data access functionality related to airports.

"""

import sqlalchemy as sa

from . import base
from jormungand.core import db
from jormungand.core.logging import get_logger

logger = get_logger(__name__)

_TABLE_NAME = db.TN_AIRPORTS
_ID_C_NAME = "airport_id"


def airports_init_data(data: list[dict]):
    """Remove all existing airports data from the db and add new data instead.

    :data: The new airports data that is to be inserted into the database.
    :returns: None
    """
    base.init_table_data(_TABLE_NAME, data)


def get_airports_by_substring(substring: str, limit: int = 5) -> list[dict]:
    """Get a small selection of airports matching a substring.

    The substring is matched against:

    1. Airport IATA code
    2. Airport country code
    3. Airport country name
    4. Airport principality
    5. Airport airport name

    :substring: The substring to match against the above fields.
    :limit: The number of results to return.
    :returns: A short list of airport matches.
    """
    with db.get_db_connection() as conn:
        result = conn.execute(sa.text(
            """
            SELECT * FROM GET_AIRPORTS_BY_SUBSTRING(:substring, :limit)
            """), {"substring": substring, "limit": limit}
            ).mappings().all()
        return [dict(entry) for entry in result]
