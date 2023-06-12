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


def get_clean_country_data(country_data: dict) -> dict | None:
    return CoutriesValidator.clean_data(
        country_id=country_data["id"],
        code=country_data["code"],
        name=country_data["name"],
    )


def get_clean_countries_data() -> list[dict]:
    cleaned_counries_data = []

    with open(_DATASET_COUNTRIES, 'r', encoding='UTF-8') as dataset_file:
        dict_reader = csv.DictReader(dataset_file)
        for country_data in dict_reader:
            cleaned_country_data = get_clean_country_data(country_data)
            if cleaned_country_data is not None:
                cleaned_counries_data.append(cleaned_country_data)

    return cleaned_counries_data


def import_country_data(debug=False):
    """One time import of selective country data from csv dataset to the DAL.

    Currently all countries are imported.

    Currently the data imported is:
    * Country OurAirports ids.
    * Country ISO 3166-1 alpha-2 codes.
    * Country names.

    .. note:: the OurAirports id fields from the csv dataset
        are directly inserted as the countries primary keys for simplicity,
        this will be changed if it causes problems.

    :debug: If set to true will call the underlying DAL executor in debug mode
        this can be useful to find a malformed and unhandled entry in the
        input dataset.
    """

    cleaned_counries_data = get_clean_countries_data()
    CountriesManager.upsert_many(
            data=cleaned_counries_data, debug=debug, mirror=True)


def get_clean_airport_data(
        airport_data: dict, airport_ids: dict[str, int]) -> dict | None:
    return AirportsValidator.clean_data(
        airport_id=airport_data["id"],
        country_id=airport_ids.get(airport_data.get["iso_country"], None),
        iata_code=airport_data["iata_code"],
        name=airport_data["name"],
        municipality=airport_data["municipality"],
        home_link=airport_data["home_link"],
        wikipedia_link=airport_data["wikipedia_link"],
    )


def get_clean_airports_data(airport_ids: dict[str, int]) -> list[dict]:
    cleaned_airports_data = []

    with open(_DATASET_AIRPORTS, 'r', encoding='UTF-8') as dataset_file:
        dict_reader = csv.DictReader(dataset_file)
        for airport_data in dict_reader:
            cleaned_airport_data = get_clean_airport_data(airport_data)
            if cleaned_airport_data is not None:
                cleaned_airports_data.append(cleaned_airport_data)

    return cleaned_airports_data


def import_airport_data(debug=False):
    """One time import of selective airport data from csv dataset to the DAL.


    Currently Only major airports with an IATA code are imported.

    Currently the data imported is:
    * Airport OurAirports ids.
    * Airport country_ids (deduced from the Airport country code).
    * Airport IATA codes.
    * Airport names.
    * Airport containing municipalities.
    * Airport homepage links.
    * Airport Wikipedia links.

    .. note:: the OurAirports id fields from the csv dataset
        are directly inserted as the airports primary keys for simplicity,
        this will be changed if it causes problems.
    """

    country_ids = CountriesManager.get_codes_to_ids_mapping()
    cleaned_airports_data = get_clean_airports_data(country_ids=country_ids)
    AirportsManager.upsert_many(
            data=cleaned_airports_data, debug=debug, mirror=True)
