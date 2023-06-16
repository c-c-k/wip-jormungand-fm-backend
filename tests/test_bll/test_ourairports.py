from jormungand.core import db
from jormungand.dal import ourairports
from jormungand.bll import (
    import_oa_country_data, import_oa_airport_data)
from tests.utils import (
    Assets, db_load_dataset, dataset_in_db, table_entry_count)

DATASET_FIXED = {
    "countries": {
        1: {'code': 'AA', 'name': 'valid country a'},
        2: {'code': 'BB', 'name': 'valid country b'}
    },
    "airports": {
        1: {
            'iata_code': 'AAA',
            'country_id': 1,
            'municipality': 'valid municipality a',
            'name': 'valid airport a'
        },
        2: {
            'iata_code': 'BBB',
            'country_id': 2,
            'municipality': 'valid municipality b',
            'name': 'valid airport b'
        }
    }
}


def test_ourairports_data_import(monkeypatch, tmp_db):
    # NOTE: Currently this test is somewhat of a placeholder
    #       that tests the entire process of importing data from
    #       the OurAirports csv datasets (i.e. it tests both the BLL
    #       and the DAL related functionalities of the process).
    #       It will be split into more specific tests if/when there
    #       is the time and need to do so.

    dataset = db_load_dataset(tmp_db, DATASET_FIXED,
                              remove_apk=False, load_to_db=False)
    monkeypatch.setattr(ourairports, "_DATASET_COUNTRIES",
                        Assets.ouraiports_countries_sample)
    monkeypatch.setattr(ourairports, "_DATASET_AIRPORTS",
                        Assets.ouraiports_airports_sample)
    import_oa_country_data()
    import_oa_airport_data()
    dataset_in_db(tmp_db, dataset)
    assert table_entry_count(tmp_db, db.TN_COUNTRIES) == 2
    assert table_entry_count(tmp_db, db.TN_AIRPORTS) == 2
