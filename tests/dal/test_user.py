from copy import deepcopy

import pytest
pytest.skip(allow_module_level=True)
from sqlalchemy import Engine, text, select

from jormungand.core.dal.users import (
    get_by_id, get_all, add_one, add_many, update, remove)
from jormungand.core import db
from tests.utils import setup_dataset, compare_dataset_all

DATASET_2_TEST_USERS = {
    'users': {
        'user_1': {
            'id': 1,
            'user_role_1': int(db.UserRole.CUSTOMER),
            'username': 'user_1',
            'password': 'pass',
            'email': 'user_1@email.com',
        },
        'user_2': {
            'id': 2,
            'user_role_2': int(db.UserRole.CUSTOMER),
            'username': 'user_2',
            'password': 'pass',
            'email': 'user_2@email.com',
        },
    }
}



