"""Import of OurAirports datasets.

This module is responsible for importing country and airport data from the
datasets provided by https://ourairports.com/ .
"""

import csv
from pathlib import Path

from jormungand.dal import AirportsManager, CountriesManager
from jormungand.validation import AirportsValidator, CoutriesValidator

_CSV_DIR = Path(__file__).parent.joinpath('csv')
_DATASET_COUNTRIES = _CSV_DIR.joinpath('countries')
_DATASET_AIRPORTS = _CSV_DIR.joinpath('airports')


def _get_clean_country_data(country_data: dict) -> dict | None:
    return CoutriesValidator.clean_data(
        with_id=False,
        country_id=country_data["id"],
        code=country_data["code"],
        name=country_data["name"],
    )


def _get_clean_countries_data() -> list[dict]:
    cleaned_counries_data = []

    with open(_DATASET_COUNTRIES, 'r', encoding='UTF-8') as dataset_file:
        dict_reader = csv.DictReader(dataset_file)
        for country_data in dict_reader:
            cleaned_country_data = _get_clean_country_data(country_data)
            if cleaned_country_data is not None:
                cleaned_counries_data.append(cleaned_country_data)

    return cleaned_counries_data


def import_country_data():
    """One time import of selective country data from csv dataset to the DAL.

    Currently the data imported is:
    * Country ISO 3166-1 alpha-2 codes.
    * Country names.
    """

    cleaned_counries_data = _get_clean_countries_data()
    CountriesManager.upsert_many(data=cleaned_counries_data, mirror=True)


def _get_clean_airport_data(
        airport_data: dict, country_ids: dict[str, int]) -> dict | None:
    if airport_data["type"] != "large_airport":
        cleaned_airport_data = None
    else:
        cleaned_airport_data = AirportsValidator.clean_data(
            with_id=False,
            airport_id=airport_data["id"],
            country_id=country_ids.get(airport_data.get["iso_country"], None),
            iata_code=airport_data["iata_code"],
            name=airport_data["name"],
            municipality=airport_data["municipality"],
        )
    return cleaned_airport_data


def _get_clean_airports_data(country_ids: dict[str, int]) -> list[dict]:
    cleaned_airports_data = []

    with open(_DATASET_AIRPORTS, 'r', encoding='UTF-8') as dataset_file:
        dict_reader = csv.DictReader(dataset_file)
        for airport_data in dict_reader:
            cleaned_airport_data = _get_clean_airport_data(airport_data,
                                                           country_ids)
            if cleaned_airport_data is not None:
                cleaned_airports_data.append(cleaned_airport_data)

    return cleaned_airports_data


def import_airport_data():
    """One time import of selective airport data from csv dataset to the DAL.

    Currently the data imported is:
    * Airport country_ids (deduced from the Airport country code).
    * Airport IATA codes.
    * Airport names.
    * Airport containing municipalities.

    .. note::
        Currently Only major airports are imported.
        Also airports without name/municipality/IATA code
        are pruned during validation.
    """

    country_ids = CountriesManager.get_codes_to_ids_mapping()
    cleaned_airports_data = _get_clean_airports_data(country_ids=country_ids)
    AirportsManager.upsert_many(data=cleaned_airports_data, mirror=True)
