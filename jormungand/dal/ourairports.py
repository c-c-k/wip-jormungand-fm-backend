"""DAL: Read: OurAirports datasets: countries & airports

This module is responsible for reading country and airport data from the
datasets provided by https://ourairports.com/ .
"""

from .base import CSV_DIR, get_data_from_csv

_DATASET_COUNTRIES = CSV_DIR.joinpath("countries.csv")
_DATASET_AIRPORTS = CSV_DIR.joinpath("airports.csv")


def oa_countries_get_all() -> list[dict]:
    """Get selective countries data from the OurAirports csv dataset.

    Currently the data imported is:
    * code: Country ISO 3166-1 alpha-2 codes.
    * name: Country names.
    """

    return get_data_from_csv(
        dataset_path=_DATASET_COUNTRIES,
        field_names={"code": "code", "name": "name"}
    )


def oa_airports_get_all() -> list[dict]:
    """Get selective airport data from the OurAirports csv dataset.

    Currently the data imported is:
    * iso_country->country_code: Airport country ISO 3166-1 alpha-2 codes.
    * type->airport_type: A size and usage classification of the airport.
    * iata_code: Airport IATA codes.
    * name: Airport names.
    * municipality: Airport municipalities.

    """

    return get_data_from_csv(
        dataset_path=_DATASET_AIRPORTS,
        field_names={
            "iso_country": "country_code",
            "type": "airport_type",
            "iata_code": "iata_code",
            "name": "name",
            "municipality": "municipality",
        },
    )
