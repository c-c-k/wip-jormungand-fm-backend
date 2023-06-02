from copy import deepcopy
from operator import itemgetter

import pytest
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from jormungand.core import db
from jormungand.core.exceptions import DataNotFoundError
from jormungand.dal import users
from tests.utils import db_load_dataset, data_in_table

DATASET_2_USERS = {
    "users": {
        "user_1": {
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


def get_dataset_1_user() -> dict:
    dataset = deepcopy(DATASET_2_USERS)
    dataset["users"].pop("user_2")
    return dataset


def get_dataset_2_users() -> dict:
    dataset = deepcopy(DATASET_2_USERS)
    return dataset


def get_data_1_users() -> dict:
    dataset = get_dataset_1_user()
    data = dataset["users"]["user_1"]
    return data


def get_data_2_users() -> dict:
    dataset = get_dataset_2_users()
    data = dataset["users"]
    return data


class TestGet:
    def test_get_user_by_id_returns_user_data(self, tmp_db):
        dataset = get_dataset_2_users()
        db_load_dataset(tmp_db, dataset)
        test_data = users.get_by_id(dataset["users"]["user_1"]["id"])
        assert test_data == dataset["users"]["user_1"]

    def test_get_all_users_returns_all_users_data_as_list(self, tmp_db):
        dataset = get_dataset_2_users()
        db_load_dataset(tmp_db, dataset)
        test_data = users.get_all()
        assert sorted(test_data, key=itemgetter("id")) == sorted(
            dataset["users"].values(), key=itemgetter("id")
        )

    def test_get_all_users_when_no_users_exist_returns_empty_list(self, tmp_db):
        test_data = users.get_all()
        assert test_data == []

    def test_get_non_existing_user_by_id_raises_exception(self, tmp_db):
        with pytest.raises(DataNotFoundError) as excinfo:
            users.get_by_id(-1)
            assert "-1" in str(excinfo.value)


class TestAddOne:
    def test_add_new_user_adds_user(self, tmp_db):
        data = get_data_1_users()
        table = db.get_table_by_name(db.TN_USERS)
        users.add_one(data)
        data_in_table(tmp_db, data, table)

    def test_add_new_user_returns_user_data_with_id(self, tmp_db):
        data = get_data_1_users()
        return_data = users.add_one(data)
        assert return_data.pop("id", None) is not None
        assert data == return_data

    @pytest.mark.skip(reason="should raise exception instead")
    def test_add_existing_user_returns_user_data_with_id(self, tmp_db):
        dataset = get_dataset_1_user()
        data = get_data_1_users()
        db_load_dataset(tmp_db, dataset)
        return_data = users.add_one(data)
        assert return_data.pop("id", None) is not None
        assert data == return_data

    def test_add_existing_user_raises_integrity_error(self, tmp_db):
        dataset = get_dataset_1_user()
        data = get_data_1_users()
        db_load_dataset(tmp_db, dataset)
        with pytest.raises(IntegrityError) as excinfo:
            users.add_one(data)
        assert "username" in str(excinfo.value)

    def test_add_new_user_with_invalid_data_raises_integrity_error(self, tmp_db):
        data = get_data_1_users()
        data.pop("username")
        with pytest.raises(IntegrityError) as excinfo:
            users.add_one(data)
        assert "username" in str(excinfo.value)


class TestAddMany:
    def test_add_many_users_adds_new_users(self, tmp_db):
        data = get_data_2_users()
        table = db.get_table_by_name(db.TN_USERS)
        users.add_many(data.values())
        data_in_table(tmp_db, data.values(), table)

    def test_add_many_new_users_returns_users_data_with_id_for_all_input_users(
        self, tmp_db
    ):
        data = get_data_2_users()
        return_data = users.add_many(data.values())
        assert len(return_data) == len(data)
        for entry in return_data:
            assert entry.pop("id", None) is not None
            assert entry == data[entry["username"]]

    def test_add_many_users_with_some_users_existing_adds_new_users(self, tmp_db):
        dataset = get_dataset_1_user()
        data = get_data_2_users()
        table = db.get_table_by_name(db.TN_USERS)
        db_load_dataset(tmp_db, dataset)
        users.add_many(data.values())
        data_in_table(tmp_db, data.values(), table)

    def test_add_many_users_with_some_users_existing_returns_user_data_only_for_new_users(self, tmp_db):
        dataset = get_dataset_1_user()
        data = get_data_2_users()
        db_load_dataset(tmp_db, dataset)
        return_data = users.add_many(data.values())
        data.pop("user_1")
        assert len(return_data) == len(data)
        for entry in return_data:
            assert entry.pop("id", None) is not None
            assert entry == data[entry["username"]]

    def test_add_many_users_with_some_users_existing_does_not_raise_exception(
        self, tmp_db
    ):
        dataset = get_dataset_1_user()
        data = get_data_2_users()
        db_load_dataset(tmp_db, dataset)
        users.add_many(data.values())

    def test_add_many_users_with_all_users_existing_does_not_raise_exception(
        self, tmp_db
    ):
        dataset = get_dataset_2_users()
        data_input = get_data_2_users()
        db_load_dataset(tmp_db, dataset)
        users.add_many(data_input.values())

    def test_add_many_users_with_all_users_existing_returns_empty_list(self, tmp_db):
        dataset = get_dataset_2_users()
        data_input = get_data_2_users()
        db_load_dataset(tmp_db, dataset)
        return_data = users.add_many(data_input.values())
        assert return_data == []


@pytest.mark.current
class TestUpdate:
    @pytest.mark.skip("TODO: test")
    def test_update_user_updates_user(self, tmp_db):
        dataset = get_dataset_2_user()
        data = get_data_2_users()
        # MEMO: make get data from dataset helper
        table = db.get_table_by_name(db.TN_USERS)
        db_load_dataset(tmp_db, dataset)
        data["user_1"]
        users.add_many(data.values())
        data_in_table(tmp_db, data.values(), table)
        pass

    @pytest.mark.skip("TODO: test")
    def test_update_user_returns_updated_user_data(self, tmp_db):
        pass

    @pytest.mark.skip("TODO: test")
    def test_update_non_existing_user_raises_exception(self, tmp_db):
        pass

    @pytest.mark.skip("TODO: test")
    def test_update_user_with_invalid_data_raises_exception(self, tmp_db):
        pass


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

