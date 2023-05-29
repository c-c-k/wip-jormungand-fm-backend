from copy import deepcopy

import pytest
from sqlalchemy import Engine, text, select

# from jormungand.core.dal.users import (
#     get_by_id, get_all, add_one, add_many, update, remove)
from jormungand.core import db
from tests.utils import setup_dataset, compare_dataset_all

DATASET_EXAMPLE_USERS = {
    'users': {
        'user_1': {
            'id': 1,
            'user_role': int(db.UserRole.CUSTOMER),
            'username': 'user_1',
            'password': 'pass',
            'email': 'user_1@email.com',
        },
        'user_2': {
            'id': 2,
            'user_role': int(db.UserRole.CUSTOMER),
            'username': 'user_2',
            'password': 'pass',
            'email': 'user_2@email.com',
        },
    }
}


@pytest.mark.current
class TestDALUsersWithDatasetExampleUsers:
    @pytest.fixture(autouse=True)
    def load_dataset_into_db(self, db_engine):
        with db_engine.begin() as conn:
            setup_dataset(conn, DATASET_EXAMPLE_USERS)


    def test_use_aufix(self, db_engine):
        with db_engine.begin() as conn:
            compare_dataset_all(conn, DATASET_EXAMPLE_USERS)
