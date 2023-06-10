from operator import itemgetter

import pytest

pytest.skip(allow_module_level=True, reason="disabled due to dal being broken")

from jormungand.core import db
from jormungand.core.exceptions import (
        DataNotFoundError, DuplicateKeyError, InvalidDataError)
from jormungand.dal import customers
from tests.utils.data import (
        db_load_dataset, data_in_table, get_data_from_dataset)

DATASET_FIXED = {
    "users": {
        1: {
            "user_id": 1,
            "user_role_id": int(db.UserRole.CUSTOMER),
            "username": "customer_1",
            "password": "pass",
            "email": "customer_1@email.com",
            "avatar_url": "customer_1.png",
        },
        2: {
            "user_id": 2,
            "user_role_id": int(db.UserRole.CUSTOMER),
            "username": "customer_2",
            "password": "pass",
            "email": "customer_2@email.com",
            "avatar_url": "customer_2.png",
        },
    }
}
DATASET_1_CUSTOMERS = {
    "customers": {
        1: {
            "user_id": 1,
            "first_name": "first_name_1",
            "last_name": "last_name_1",
            "address": "address 1",
            "phone_number": "phone_number 1",
            "credit_card_number": "credit_card_number 1",
        },
    }
}
DATASET_2_CUSTOMERS = {
    "customers": {
        1: {
            "user_id": 1,
            "first_name": "first_name_1",
            "last_name": "last_name_1",
            "address": "address 1",
            "phone_number": "phone_number 1",
            "credit_card_number": "credit_card_number 1",
        },
        2: {
            "user_id": 2,
            "first_name": "first_name_2",
            "last_name": "last_name_2",
            "address": "address 2",
            "phone_number": "phone_number 2",
            "credit_card_number": "credit_card_number 2",
        },
    }
}


@pytest.fixture(scope="function", autouse=True)
def load_fixed_dataset(tmp_db):
    db_load_dataset(tmp_db, DATASET_FIXED, remove_apk=False)


class TestGet:
    def test_get_customer_by_id_returns_customer_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_CUSTOMERS, remove_apk=False)
        table = db.get_table(db.TN_CUSTOMERS)
        expected_data = get_data_from_dataset(dataset, table)[1]
        prog_data = customers.get_by_id(expected_data["user_id"])
        assert prog_data == expected_data

    def test_get_non_existing_customer_by_id_raises_data_not_found_error(self, tmp_db):
        with pytest.raises(
                DataNotFoundError, match=r".*id.*-9999.*"):
            customers.get_by_id(-9999)

    def test_get_all_customers_returns_all_customers_data_as_list(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_CUSTOMERS, remove_apk=False)
        table = db.get_table(db.TN_CUSTOMERS)
        expected_data = get_data_from_dataset(dataset, table).values()
        expected_data = sorted(expected_data, key=itemgetter("user_id"))
        prog_data = customers.get_all()
        prog_data = sorted(prog_data, key=itemgetter("user_id"))
        assert prog_data == expected_data

    def test_get_all_customers_when_no_customers_exist_returns_empty_list(self, tmp_db):
        prog_data = customers.get_all()
        assert prog_data == []


class TestAddOne:
    def test_add_new_customer_adds_customer(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_CUSTOMERS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table)[1]
        customers.add_one(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_add_new_customer_returns_customer_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_CUSTOMERS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table)[1]
        prog_data = customers.add_one(input_data)
        assert prog_data == input_data

    def test_add_existing_customer_raises_duplicate_key_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_CUSTOMERS, remove_apk=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table)[1]
        with pytest.raises(
                DuplicateKeyError,
                match=rf".*id.*{input_data['user_id']}.*"
                ):
            customers.add_one(input_data)

    def test_add_new_customer_with_invalid_data_raises_invalid_data_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_CUSTOMERS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table)[1]
        input_data["user_id"] = "invalid value"
        with pytest.raises(InvalidDataError):
            customers.add_one(input_data)


class TestAddMany:
    def test_add_many_customers_adds_new_customers(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_CUSTOMERS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table).values()
        customers.add_many(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_add_many_new_customers_returns_customers_data_for_all_input_customers(
        self, tmp_db
    ):
        dataset = db_load_dataset(tmp_db, DATASET_2_CUSTOMERS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_CUSTOMERS)
        test_data = get_data_from_dataset(dataset, table)
        input_data = test_data.values()
        prog_data = customers.add_many(input_data)
        assert len(prog_data) == len(input_data)
        for entry in prog_data:
            assert entry == test_data[entry["user_id"]]

    def test_add_many_customers_with_some_customers_existing_does_not_raise_exception(
        self, tmp_db
    ):
        dataset = db_load_dataset(tmp_db, DATASET_1_CUSTOMERS, remove_apk=False)
        dataset = db_load_dataset(tmp_db, DATASET_2_CUSTOMERS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table).values()
        customers.add_many(input_data)

    def test_add_many_customers_with_some_customers_existing_adds_new_customers(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_CUSTOMERS, remove_apk=False)
        dataset = db_load_dataset(tmp_db, DATASET_2_CUSTOMERS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table).values()
        customers.add_many(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_add_many_customers_with_some_customers_existing_returns_customer_data_only_for_new_customers(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_CUSTOMERS, remove_apk=False)
        dataset = db_load_dataset(tmp_db, DATASET_2_CUSTOMERS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_CUSTOMERS)
        test_data = get_data_from_dataset(dataset, table)
        input_data = test_data.values()
        prog_data = customers.add_many(input_data)
        assert len(prog_data) == 1
        assert prog_data[0] == test_data[2]

    def test_add_many_customers_with_all_customers_existing_does_not_raise_exception(
        self, tmp_db
    ):
        dataset = db_load_dataset(tmp_db, DATASET_2_CUSTOMERS, remove_apk=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table).values()
        customers.add_many(input_data)

    def test_add_many_customers_with_all_customers_existing_returns_empty_list(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_CUSTOMERS, remove_apk=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table).values()
        prog_data = customers.add_many(input_data)
        assert prog_data == []


class TestUpdate:
    def test_update_customer_updates_customer(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_CUSTOMERS, remove_apk=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table)[1]
        input_data["first_name"] = "first name changed"
        customers.update(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_update_customer_returns_updated_customer_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_CUSTOMERS, remove_apk=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table)[1]
        input_data["first_name"] = "first name changed"
        prog_data = customers.update(input_data)
        assert prog_data == input_data

    def test_update_non_existing_customer_raises_data_not_found_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_CUSTOMERS,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table)[1]
        with pytest.raises(
                DataNotFoundError,
                match=rf".*id.*{input_data['user_id']}"
                ):
            customers.update(input_data)

    def test_update_customer_with_invalid_data_raises_invalid_data_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_CUSTOMERS, remove_apk=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table)[1]
        input_data["phone_number"] = "phone_number 2"
        with pytest.raises(InvalidDataError):
            customers.update(input_data)


class TestDelete:
    def test_delete_customer_deletes_customer(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_CUSTOMERS, remove_apk=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table)[1]
        customers.delete(input_data["user_id"])
        data_in_table(tmp_db, input_data, table, reverse=True)

    def test_delete_customer_returns_deleted_customer_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_CUSTOMERS, remove_apk=False)
        table = db.get_table(db.TN_CUSTOMERS)
        input_data = get_data_from_dataset(dataset, table)[1]
        prog_data = customers.delete(input_data["user_id"])
        assert prog_data == input_data

    def test_delete_non_existing_customer_raises_data_not_found_error(self, tmp_db):
        with pytest.raises(
                DataNotFoundError, match=r".*id.*-9999.*"):
            customers.delete(-9999)
