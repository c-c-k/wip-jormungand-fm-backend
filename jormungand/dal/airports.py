"""Data access functionality related to airports.

"""

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
