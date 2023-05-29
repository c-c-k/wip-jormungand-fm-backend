"""
    get_by_id, get_all
test get user by id returns user info
test get all users returns all users info
test get all users when no users exist returns empty
test get non existing user by id raises exception
    add one
test add new user adds user
test add new user returns user info with id
test add existing user returns user info with id
test add existing user does not raise exception
test add new user with invalid data raises exception
    add many
test add many users adds new users
test add many users returns users info with id for all input users
test add many users with some or all users existing does not raise exception
    update
test update user updates user
test update user returns updated user info
test update non existing user raises exception
test update user with invalid data raises exception
    delete
test delete user deletes user
test delete user returns none
test delete non existing user raises exception
"""
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


# TODO: MEMO: move tempdb creator into test/utils, 
#             call on module/class scope when as needed
@pytest.mark.current
class TestDALUsersWithDatasetExampleUsers:
    def load_dataset_into_db(self, db_engine):
        with db_engine.begin() as conn:
            setup_dataset(conn, DATASET_EXAMPLE_USERS)

@pytest.mark.skip("TODO: test")
class TestGet:

    @pytest.mark.skip("TODO: test")
    def test_get_user_by_id_returns_user_info(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_get_all_users_returns_all_users_info(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_get_all_users_when_no_users_exist_returns_empty(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_get_non_existing_user_by_id_raises_exception(self):
        pass


@pytest.mark.skip("TODO: test")
class TestAddOne:

    @pytest.mark.skip("TODO: test")
    def test_add_new_user_adds_user(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_add_new_user_returns_user_info_with_id(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_add_existing_user_returns_user_info_with_id(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_add_existing_user_does_not_raise_exception(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_add_new_user_with_invalid_data_raises_exception(self):
        pass


@pytest.mark.skip("TODO: test")
class TestAddMany:

    @pytest.mark.skip("TODO: test")
    def test_add_many_users_adds_new_users(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_add_many_users_returns_users_info_with_id_for_all_input_users(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_add_many_users_with_some_or_all_users_existing_does_not_raise_exception(self):
        pass


@pytest.mark.skip("TODO: test")
class TestUpdate:

    @pytest.mark.skip("TODO: test")
    def test_update_user_updates_user(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_update_user_returns_updated_user_info(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_update_non_existing_user_raises_exception(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_update_user_with_invalid_data_raises_exception(self):
        pass


@pytest.mark.skip("TODO: test")
class TestDelete:

    @pytest.mark.skip("TODO: test")
    def test_delete_user_deletes_user(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_delete_user_returns_none(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_delete_non_existing_user_raises_exception(self):
        pass



    def test_1(self):
        # """TEST__________!"""
        assert 1==0
        # with db_engine.begin() as conn:
        #     compare_dataset_all(conn, DATASET_EXAMPLE_USERS)
