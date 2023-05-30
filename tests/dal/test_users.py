"""
    get_by_id, get_all
test get user by id returns user data
test get all users returns all users data as list
test get all users when no users exist returns empty list
test get non existing user by id raises exception
    add one
test add new user adds user
test add new user returns user data with id
test add existing user returns user data with id
test add existing user does not raise exception
test add new user with invalid data raises exception
    add many
test add many users adds new users
test add many users returns users data with id for all input users
test add many users with some or all users existing does not raise exception
    update
test update user updates user
test update user returns updated user data
test update non existing user raises exception
test update user with invalid data raises exception
    delete
test delete user deletes user
test delete user returns none
test delete non existing user raises exception
"""
from copy import deepcopy
from operator import itemgetter

import pytest
from sqlalchemy import Engine, text, select

from jormungand.core import db
from jormungand.core.exceptions import (
    DataNotFoundError)
from jormungand.dal import users
from tests.utils import db_load_dataset, dataset_in_db

DATASET_2_USERS = {
    'users': {
        'user_1': {
            'id': 1,
            'user_role': int(db.UserRole.CUSTOMER),
            'username': 'user_1',
            'password': 'pass',
            'email': 'user_1@email.com',
            'avatar_url': 'user_1.png',
        },
        'user_2': {
            'id': 2,
            'user_role': int(db.UserRole.CUSTOMER),
            'username': 'user_2',
            'password': 'pass',
            'email': 'user_2@email.com',
            'avatar_url': 'user_2.png',
        },
    }
}


class TestGet:
    def test_get_user_by_id_returns_user_data(self, tmp_db):
        dataset = DATASET_2_USERS
        db_load_dataset(tmp_db, dataset)
        test_data = users.get_by_id(dataset['users']['user_1']['id'])
        assert test_data == dataset['users']['user_1']


    def test_get_all_users_returns_all_users_data_as_list(self, tmp_db):
        dataset = DATASET_2_USERS
        db_load_dataset(tmp_db, dataset)
        test_data = users.get_all()
        assert (
                sorted(test_data, key=itemgetter('id'))
                == sorted(dataset['users'].values(), key=itemgetter('id')))


    def test_get_all_users_when_no_users_exist_returns_empty_list(self, tmp_db):
        test_data = users.get_all()
        assert test_data == []


    def test_get_non_existing_user_by_id_raises_exception(self, tmp_db):
        with pytest.raises(DataNotFoundError) as excinfo:
            test_data = users.get_by_id(-1)
            assert '-1' in str(excinfo.value)


@pytest.mark.current
class TestAddOne:
    @pytest.mark.skip("TODO: test")
    def test_add_new_user_adds_user(self, temp_db):
        user_data = DATASET_2_USERS['users']['user_1']
        users.add_one(user_data)


    @pytest.mark.skip("TODO: test")
    def test_add_new_user_returns_user_data_with_id(self):
        pass


    @pytest.mark.skip("TODO: test")
    def test_add_existing_user_returns_user_data_with_id(self):
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
    def test_add_many_users_returns_users_data_with_id_for_all_input_users(self):
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
    def test_update_user_returns_updated_user_data(self):
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
