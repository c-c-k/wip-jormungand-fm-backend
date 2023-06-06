from operator import itemgetter

import pytest

from jormungand.core import db
from jormungand.core.exceptions import (
        DataNotFoundError, DuplicateKeyError, InvalidDataError)
from jormungand.dal import airline_companies
from tests.utils.data import (
        db_load_dataset, data_in_table, get_data_from_dataset)

DATASET_FIXED = {
    "users": {
        1: {
            "user_id": 1,
            "user_role_id": int(db.UserRole.AIRLINE_COMPANY),
            "username": "airline_company_1",
            "password": "pass",
            "email": "airline_company_1@email.com",
            "avatar_url": "airline_company_1.png",
        },
        2: {
            "user_id": 2,
            "user_role_id": int(db.UserRole.AIRLINE_COMPANY),
            "username": "airline_company_2",
            "password": "pass",
            "email": "airline_company_2@email.com",
            "avatar_url": "airline_company_2.png",
        },
    },
    "countries": {
        1: {
            "country_id": 1,
            "name": "country_1",
            "flag_url": "country_1.png",
        },
        2: {
            "country_id": 2,
            "name": "country_2",
            "flag_url": "country_2.png",
        },
    }
}
DATASET_1_AIRLINE_COMPANIES = {
    "airline_companies": {
        1: {
            "user_id": 1,
            "country_id": 1,
            "name": "airline_company_1",
        },
    }
}
DATASET_2_AIRLINE_COMPANIES = {
    "airline_companies": {
        1: {
            "user_id": 1,
            "country_id": 1,
            "name": "airline_company_1",
        },
        2: {
            "user_id": 2,
            "country_id": 2,
            "name": "airline_company_2",
        },
    }
}


@pytest.fixture(scope="function", autouse=True)
def load_fixed_dataset(tmp_db):
    db_load_dataset(tmp_db, DATASET_FIXED, remove_apk=False)


class TestGet:
    def test_get_airline_company_by_id_returns_airline_company_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_AIRLINE_COMPANIES, remove_apk=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        expected_data = get_data_from_dataset(dataset, table)[1]
        prog_data = airline_companies.get_by_id(expected_data["user_id"])
        assert prog_data == expected_data

    def test_get_non_existing_airline_company_by_id_raises_data_not_found_error(self, tmp_db):
        with pytest.raises(
                DataNotFoundError, match=r".*id.*-9999.*"):
            airline_companies.get_by_id(-9999)

    def test_get_all_airline_companies_returns_all_airline_companies_data_as_list(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_AIRLINE_COMPANIES, remove_apk=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        expected_data = get_data_from_dataset(dataset, table).values()
        expected_data = sorted(expected_data, key=itemgetter("user_id"))
        prog_data = airline_companies.get_all()
        prog_data = sorted(prog_data, key=itemgetter("user_id"))
        assert prog_data == expected_data

    def test_get_all_airline_companies_when_no_airline_companies_exist_returns_empty_list(self, tmp_db):
        prog_data = airline_companies.get_all()
        assert prog_data == []


class TestAddOne:
    def test_add_new_airline_company_adds_airline_company(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_AIRLINE_COMPANIES,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table)[1]
        airline_companies.add_one(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_add_new_airline_company_returns_airline_company_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_AIRLINE_COMPANIES,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table)[1]
        prog_data = airline_companies.add_one(input_data)
        assert prog_data == input_data

    def test_add_existing_airline_company_raises_duplicate_key_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_AIRLINE_COMPANIES, remove_apk=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table)[1]
        with pytest.raises(
                DuplicateKeyError,
                match=rf".*id.*{input_data['user_id']}.*"
                ):
            airline_companies.add_one(input_data)

    def test_add_new_airline_company_with_invalid_data_raises_invalid_data_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_AIRLINE_COMPANIES,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table)[1]
        input_data["user_id"] = "invalid value"
        with pytest.raises(InvalidDataError):
            airline_companies.add_one(input_data)


class TestAddMany:
    def test_add_many_airline_companies_adds_new_airline_companies(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_AIRLINE_COMPANIES,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table).values()
        airline_companies.add_many(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_add_many_new_airline_companies_returns_airline_companies_data_for_all_input_airline_companies(
        self, tmp_db
    ):
        dataset = db_load_dataset(tmp_db, DATASET_2_AIRLINE_COMPANIES,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        test_data = get_data_from_dataset(dataset, table)
        input_data = test_data.values()
        prog_data = airline_companies.add_many(input_data)
        assert len(prog_data) == len(input_data)
        for entry in prog_data:
            assert entry == test_data[entry["user_id"]]

    def test_add_many_airline_companies_with_some_airline_companies_existing_does_not_raise_exception(
        self, tmp_db
    ):
        dataset = db_load_dataset(tmp_db, DATASET_1_AIRLINE_COMPANIES, remove_apk=False)
        dataset = db_load_dataset(tmp_db, DATASET_2_AIRLINE_COMPANIES,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table).values()
        airline_companies.add_many(input_data)

    def test_add_many_airline_companies_with_some_airline_companies_existing_adds_new_airline_companies(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_AIRLINE_COMPANIES, remove_apk=False)
        dataset = db_load_dataset(tmp_db, DATASET_2_AIRLINE_COMPANIES,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table).values()
        airline_companies.add_many(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_add_many_airline_companies_with_some_airline_companies_existing_returns_airline_company_data_only_for_new_airline_companies(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_AIRLINE_COMPANIES, remove_apk=False)
        dataset = db_load_dataset(tmp_db, DATASET_2_AIRLINE_COMPANIES,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        test_data = get_data_from_dataset(dataset, table)
        input_data = test_data.values()
        prog_data = airline_companies.add_many(input_data)
        assert len(prog_data) == 1
        assert prog_data[0] == test_data[2]

    def test_add_many_airline_companies_with_all_airline_companies_existing_does_not_raise_exception(
        self, tmp_db
    ):
        dataset = db_load_dataset(tmp_db, DATASET_2_AIRLINE_COMPANIES, remove_apk=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table).values()
        airline_companies.add_many(input_data)

    def test_add_many_airline_companies_with_all_airline_companies_existing_returns_empty_list(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_AIRLINE_COMPANIES, remove_apk=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table).values()
        prog_data = airline_companies.add_many(input_data)
        assert prog_data == []


class TestUpdate:
    def test_update_airline_company_updates_airline_company(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_AIRLINE_COMPANIES, remove_apk=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table)[1]
        input_data["name"] = "airline co. name changed"
        airline_companies.update(input_data)
        data_in_table(tmp_db, input_data, table)

    def test_update_airline_company_returns_updated_airline_company_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_AIRLINE_COMPANIES, remove_apk=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table)[1]
        input_data["name"] = "airline co. name changed"
        prog_data = airline_companies.update(input_data)
        assert prog_data == input_data

    def test_update_non_existing_airline_company_raises_data_not_found_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_AIRLINE_COMPANIES,
                                  remove_apk=False, load_to_db=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table)[1]
        with pytest.raises(
                DataNotFoundError,
                match=rf".*id.*{input_data['user_id']}"
                ):
            airline_companies.update(input_data)

    def test_update_airline_company_with_invalid_data_raises_invalid_data_error(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_2_AIRLINE_COMPANIES, remove_apk=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table)[1]
        input_data["name"] = None
        with pytest.raises(InvalidDataError):
            airline_companies.update(input_data)


class TestDelete:
    def test_delete_airline_company_deletes_airline_company(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_AIRLINE_COMPANIES, remove_apk=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table)[1]
        airline_companies.delete(input_data["user_id"])
        data_in_table(tmp_db, input_data, table, reverse=True)

    def test_delete_airline_company_returns_deleted_airline_company_data(self, tmp_db):
        dataset = db_load_dataset(tmp_db, DATASET_1_AIRLINE_COMPANIES, remove_apk=False)
        table = db.get_table(db.TN_AIRLINE_COMPANIES)
        input_data = get_data_from_dataset(dataset, table)[1]
        prog_data = airline_companies.delete(input_data["user_id"])
        assert prog_data == input_data

    def test_delete_non_existing_airline_company_raises_data_not_found_error(self, tmp_db):
        with pytest.raises(
                DataNotFoundError, match=r".*id.*-9999.*"):
            airline_companies.delete(-9999)
