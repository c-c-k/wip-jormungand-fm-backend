from copy import deepcopy
from operator import itemgetter

import pytest
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from jormungand.core import db
from jormungand.core.exceptions import DataNotFoundError
from jormungand.dal import users
from tests.utils.data import (
        db_load_dataset, data_in_table, get_data_from_dataset)

DATASET_1_USERS = {
    "users": {
        "user_1": {
            "id": 1,
            "user_role": int(db.UserRole.CUSTOMER),
            "username": "user_1",
            "password": "pass",
            "email": "user_1@email.com",
            "avatar_url": "user_1.png",
        },
    }
}
DATASET_2_USERS = {
    "users": {
        "user_1": {
            "id": 2,
            "user_role": int(db.UserRole.CUSTOMER),
            "username": "user_1",
            "password": "pass",
            "email": "user_1@email.com",
            "avatar_url": "user_1.png",
        },
        "user_2": {
            "user_role": int(db.UserRole.CUSTOMER),
            "username": "user_2",
            "password": "pass",
            "email": "user_2@email.com",
            "avatar_url": "user_2.png",
        },
    }
}
# dataset = DATASET_2_USERS


# def get_dataset_1_user() -> dict:
#     dataset = deepcopy(DATASET_2_USERS)
#     dataset["users"].pop("user_2")
#     return dataset


# def get_dataset_2_users() -> dict:
#     dataset = deepcopy(DATASET_2_USERS)
#     return dataset


# def get_data_1_users() -> dict:
#     dataset = get_dataset_1_user()
#     data = dataset["users"]["user_1"]
#     return data


# def get_data_2_users() -> dict:
#     dataset = get_dataset_2_users()
#     data = dataset["users"]
#     return data


class TestGet:
    def test_get_user_by_id_returns_user_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_USERS, remove_ids=False)
        table = db.get_table(db.TN_USERS)
        expected_data = get_data_from_dataset(dataset, table)["user_1"]
        prog_data = users.get_by_id(expected_data["id"])
        assert prog_data == expected_data

    def test_get_non_existing_user_by_id_raises_exception(self, tmp_db):
        with pytest.raises(DataNotFoundError) as excinfo:
            users.get_by_id(-1)
            assert "-1" in str(excinfo.value)

    def test_get_all_users_returns_all_users_data_as_list(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_USERS, remove_ids=False)
        table = db.get_table(db.TN_USERS)
        expected_data = get_data_from_dataset(dataset, table).values()
        expected_data = sorted(expected_data, key=itemgetter("id"))
        prog_data = users.get_all()
        prog_data = sorted(prog_data, key=itemgetter("id"))
        assert prog_data == expected_data

    def test_get_all_users_when_no_users_exist_returns_empty_list(self, tmp_db):
        prog_data = users.get_all()
        assert prog_data == []


class TestAddOne:
    def test_add_new_user_adds_user(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_USERS, load_to_db=False)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table)["user_1"]
        users.add_one(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_add_new_user_returns_user_data_with_id(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_USERS, load_to_db=False)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table)["user_1"]
        prog_data = users.add_one(input_data)
        assert prog_data.pop("id", None) is not None
        assert prog_data == input_data

    def test_add_existing_user_raises_integrity_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_USERS)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table)["user_1"]
        with pytest.raises(IntegrityError) as excinfo:
            users.add_one(input_data)
        assert "username" in str(excinfo.value)

    def test_add_new_user_with_invalid_data_raises_integrity_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_USERS, load_to_db=False)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table)["user_1"]
        input_data.pop("username")
        with pytest.raises(IntegrityError) as excinfo:
            users.add_one(input_data)
        assert "username" in str(excinfo.value)


class TestAddMany:
    def test_add_many_users_adds_new_users(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_USERS, load_to_db=False)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table).values()
        users.add_many(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_add_many_new_users_returns_users_data_with_id_for_all_input_users(
        self, tmp_db
    ):
        dataset = db_load_dataset(
                tmp_db, DATASET_2_USERS, load_to_db=False)
        table = db.get_table(db.TN_USERS)
        test_data = get_data_from_dataset(dataset, table)
        input_data = test_data.values()
        prog_data = users.add_many(input_data)
        assert len(prog_data) == len(input_data)
        for entry in prog_data:
            assert entry.pop("id", None) is not None
            assert entry == test_data[entry["username"]]

    def test_add_many_users_with_some_users_existing_does_not_raise_exception(
        self, tmp_db
    ):
        db_load_dataset(tmp_db, DATASET_1_USERS, return_copy=False)
        dataset = db_load_dataset(
                tmp_db, DATASET_2_USERS, load_to_db=False)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table).values()
        users.add_many(input_data)

    def test_add_many_users_with_some_users_existing_adds_new_users(self, tmp_db):
        db_load_dataset(tmp_db, DATASET_1_USERS, return_copy=False)
        dataset = db_load_dataset(
                tmp_db, DATASET_2_USERS, load_to_db=False)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table).values()
        users.add_many(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_add_many_users_with_some_users_existing_returns_user_data_only_for_new_users(self, tmp_db):
        db_load_dataset(tmp_db, DATASET_1_USERS, return_copy=False)
        dataset = db_load_dataset(
                tmp_db, DATASET_2_USERS, load_to_db=False)
        table = db.get_table(db.TN_USERS)
        test_data = get_data_from_dataset(dataset, table)
        input_data = test_data.values()
        prog_data = users.add_many(input_data)
        assert len(prog_data) == 1
        assert prog_data[0].pop("id", None) is not None
        assert prog_data[0] == test_data["user_2"]

    def test_add_many_users_with_all_users_existing_does_not_raise_exception(
        self, tmp_db
    ):
        dataset = db_load_dataset(tmp_db, DATASET_2_USERS)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table).values()
        users.add_many(input_data)

    def test_add_many_users_with_all_users_existing_returns_empty_list(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_USERS)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table).values()
        prog_data = users.add_many(input_data)
        assert prog_data == []


@pytest.mark.current
class TestUpdate:
    def test_update_user_updates_user(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_USERS, remove_ids=False)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table)["user_1"]
        input_data["email"] = "email-changed@email.com"
        users.update(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_update_user_returns_updated_user_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_USERS, remove_ids=False)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table)["user_1"]
        input_data["email"] = "email-changed@email.com"
        prog_data = users.update(input_data)
        assert prog_data == input_data

    def test_update_non_existing_user_raises_exception(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_USERS, remove_ids=False,
                                  load_to_db=False)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table)["user_1"]
        with pytest.raises(
                DataNotFoundError, match=rf".*id.*{input_data['id']}"):
            users.update(input_data)

    def test_update_user_with_invalid_data_raises_exception(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_USERS, remove_ids=False)
        table = db.get_table(db.TN_USERS)
        input_data = get_data_from_dataset(dataset, table)["user_1"]
        input_data["username"] = None
        with pytest.raises(IntegrityError) as excinfo:
            users.update(input_data)
        assert "username" in str(excinfo.value)


@pytest.mark.skip("TODO: test")
class TestDelete:
    @pytest.mark.skip("TODO: test")
    def test_delete_user_deletes_user(self, tmp_db):
        pass

    @pytest.mark.skip("TODO: test")
    def test_delete_user_returns_none(self, tmp_db):
        pass

    @pytest.mark.skip("TODO: test")
    def test_delete_non_existing_user_raises_exception(self, tmp_db):
        pass

