from jormungand.core import db
from jormungand.dal import get_airports_by_substring
from tests.utils import (
    db_load_dataset, table_entry_count)

DATASET_SEARCH_STRING_AA_LIMIT_5 = {
    "countries": {
        1: {
            'country_id': 1,
            'code': 'AA',
            'name': '---'
        },
        2: {
            'country_id': 2,
            'code': 'BB',
            'name': 'aaz'
        },
        3: {
            'country_id': 3,
            'code': 'ZZ',
            'name': 'zzz'
        },
    },
    "airports": {
        1: {
            'airport_id': 1,
            'iata_code': 'ZZZ',
            'country_id': 1,
            'municipality': '---',
            'name': 'should be 1st match due to country code'
        },
        2: {
            'airport_id': 2,
            'iata_code': 'AAZ',
            'country_id': 2,
            'municipality': '---',
            'name': 'should be 2nd match due to IATA code'
        },
        3: {
            'airport_id': 3,
            'iata_code': 'BBB',
            'country_id': 2,
            'municipality': '---',
            'name': 'should be 3rd match due to country name'
        },
        4: {
            'airport_id': 4,
            'iata_code': 'NNN',
            'country_id': 3,
            'municipality': 'aaz',
            'name': 'should be 4th match due to municipality'
        },
        5: {
            'airport_id': 5,
            'iata_code': 'PPP',
            'country_id': 3,
            'municipality': '---',
            'name': 'aay should be 5th match due to airport name'
        },
        6: {
            'airport_id': 6,
            'iata_code': 'TTT',
            'country_id': 3,
            'municipality': '---',
            'name': 'aaz should be excluded from matches due to limit = 5'
        },
    }
}


def test_get_airports_by_substring_returns_correct_airport_matches(tmp_db):
    db_load_dataset(tmp_db, DATASET_SEARCH_STRING_AA_LIMIT_5,
                    remove_apk=False, return_copy=False)
    prog_data = get_airports_by_substring("AA", 5)
    assert len(prog_data) == 5
    for airport, expected_id in zip(prog_data, range(1, 6)):
        assert airport["airport_id"] == expected_id
