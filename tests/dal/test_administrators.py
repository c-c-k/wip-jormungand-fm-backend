from operator import itemgetter

import pytest

from jormungand.core import db
from jormungand.core.exceptions import (
        DataNotFoundError, DuplicateKeyError, InvalidDataError)
from jormungand.dal import administrators
from tests.utils.data import (
        db_load_dataset, data_in_table, get_data_from_dataset)

DATASET_2_USERS = {
    "users": {
        1: {
            "user_id": 1,
            "user_role_id": int(db.UserRole.ADMINISTRATOR),
            "username": "administrator_1",
            "password": "pass",
            "email": "administrator_1@email.com",
            "avatar_url": "administrator_1.png",
        },
        2: {
            "user_id": 2,
            "user_role_id": int(db.UserRole.ADMINISTRATOR),
            "username": "administrator_2",
            "password": "pass",
            "email": "administrator_2@email.com",
            "avatar_url": "administrator_2.png",
        },
    }
}
DATASET_1_ADMINISTRATORS = {
    "administrators": {
        1: {
            "user_id": 1,
            "first_name": "first_name_1",
            "last_name": "last_name_1",
        },
    }
}
DATASET_2_ADMINISTRATORS = {
    "administrators": {
        1: {
            "user_id": 1,
            "first_name": "first_name_1",
            "last_name": "last_name_1",
        },
        2: {
            "user_id": 2,
            "first_name": "first_name_2",
            "last_name": "last_name_2",
        },
    }
}


@pytest.fixture(scope="function", autouse=True)
def load_users_dataset(tmp_db):
    db_load_dataset(tmp_db, DATASET_2_USERS, remove_apk=False)


class TestGet:
    def test_get_administrator_by_id_returns_administrator_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_ADMINISTRATORS, remove_apk=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        expected_data = get_data_from_dataset(dataset, table)[1]
        prog_data = administrators.get_by_id(expected_data["user_id"])
        assert prog_data == expected_data

    def test_get_non_existing_administrator_by_id_raises_data_not_found_error(self, tmp_db):
        with pytest.raises(
                DataNotFoundError, match=r".*id.*-9999.*"):
            administrators.get_by_id(-9999)

    def test_get_all_administrators_returns_all_administrators_data_as_list(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_ADMINISTRATORS, remove_apk=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        expected_data = get_data_from_dataset(dataset, table).values()
        expected_data = sorted(expected_data, key=itemgetter("user_id"))
        prog_data = administrators.get_all()
        prog_data = sorted(prog_data, key=itemgetter("user_id"))
        assert prog_data == expected_data

    def test_get_all_administrators_when_no_administrators_exist_returns_empty_list(self, tmp_db):
        prog_data = administrators.get_all()
        assert prog_data == []


class TestAddOne:
    def test_add_new_administrator_adds_administrator(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table)[1]
        administrators.add_one(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_add_new_administrator_returns_administrator_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table)[1]
        prog_data = administrators.add_one(input_data)
        assert prog_data == input_data

    def test_add_existing_administrator_raises_duplicate_key_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS, remove_apk=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table)[1]
        with pytest.raises(
                DuplicateKeyError,
                match=rf".*id.*{input_data['user_id']}.*"
                ):
            administrators.add_one(input_data)

    def test_add_new_administrator_with_invalid_data_raises_invalid_data_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table)[1]
        input_data["user_id"] = "invalid value"
        with pytest.raises(InvalidDataError):
            administrators.add_one(input_data)


class TestAddMany:
    def test_add_many_administrators_adds_new_administrators(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_ADMINISTRATORS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table).values()
        administrators.add_many(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_add_many_new_administrators_returns_administrators_data_for_all_input_administrators(
        self, tmp_db
    ):
        dataset = db_load_dataset(tmp_db, DATASET_2_ADMINISTRATORS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        test_data = get_data_from_dataset(dataset, table)
        input_data = test_data.values()
        prog_data = administrators.add_many(input_data)
        assert len(prog_data) == len(input_data)
        for entry in prog_data:
            assert entry == test_data[entry["user_id"]]

    def test_add_many_administrators_with_some_administrators_existing_does_not_raise_exception(
        self, tmp_db
    ):
        dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS, remove_apk=False)
        dataset = db_load_dataset(tmp_db, DATASET_2_ADMINISTRATORS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table).values()
        administrators.add_many(input_data)

    def test_add_many_administrators_with_some_administrators_existing_adds_new_administrators(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS, remove_apk=False)
        dataset = db_load_dataset(tmp_db, DATASET_2_ADMINISTRATORS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table).values()
        administrators.add_many(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_add_many_administrators_with_some_administrators_existing_returns_administrator_data_only_for_new_administrators(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS, remove_apk=False)
        dataset = db_load_dataset(tmp_db, DATASET_2_ADMINISTRATORS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        test_data = get_data_from_dataset(dataset, table)
        input_data = test_data.values()
        prog_data = administrators.add_many(input_data)
        assert len(prog_data) == 1
        assert prog_data[0] == test_data[2]

    def test_add_many_administrators_with_all_administrators_existing_does_not_raise_exception(
        self, tmp_db
    ):
        dataset = db_load_dataset(tmp_db, DATASET_2_ADMINISTRATORS, remove_apk=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table).values()
        administrators.add_many(input_data)

    def test_add_many_administrators_with_all_administrators_existing_returns_empty_list(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_ADMINISTRATORS, remove_apk=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table).values()
        prog_data = administrators.add_many(input_data)
        assert prog_data == []


class TestUpdate:
    def test_update_administrator_updates_administrator(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS, remove_apk=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table)[1]
        input_data["first_name"] = "first name changed"
        administrators.update(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_update_administrator_returns_updated_administrator_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS, remove_apk=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table)[1]
        input_data["first_name"] = "first name changed"
        prog_data = administrators.update(input_data)
        assert prog_data == input_data

    def test_update_non_existing_administrator_raises_data_not_found_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table)[1]
        with pytest.raises(
                DataNotFoundError,
                match=rf".*id.*{input_data['user_id']}"
                ):
            administrators.update(input_data)

    # @pytest.skip(reason="administrator table doesn't have any data that can be invalid")
    # def test_update_administrator_with_invalid_data_raises_invalid_data_error(self, tmp_db):
    #     dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS, remove_apk=False)
    #     table = db.get_table(db.TN_ADMINISTRATORS)
    #     input_data = get_data_from_dataset(dataset, table)[1]
    #     input_data["???"] = ???
    #     with pytest.raises(
    #             InvalidDataError,
    #             match=rf"???"
    #             ):
    #         administrators.update(input_data)


class TestDelete:
    def test_delete_administrator_deletes_administrator(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS, remove_apk=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table)[1]
        administrators.delete(input_data["user_id"])
        data_in_table(tmp_db, input_data, table, reverse=True)

    def test_delete_administrator_returns_deleted_administrator_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_ADMINISTRATORS, remove_apk=False)
        table = db.get_table(db.TN_ADMINISTRATORS)
        input_data = get_data_from_dataset(dataset, table)[1]
        prog_data = administrators.delete(input_data["user_id"])
        assert prog_data == input_data

    def test_delete_non_existing_administrator_raises_data_not_found_error(self, tmp_db):
        with pytest.raises(
                DataNotFoundError, match=r".*id.*-9999.*"):
            administrators.delete(-9999)
