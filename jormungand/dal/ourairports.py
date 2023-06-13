"""DAL: Read: OurAirports datasets: countries & airports

This module is responsible for reading country and airport data from the
datasets provided by https://ourairports.com/ .
"""

import csv
from pathlib import Path

_CSV_DIR = Path(__file__).parent.joinpath("csv")
_DATASET_COUNTRIES = _CSV_DIR.joinpath("countries")
_DATASET_AIRPORTS = _CSV_DIR.joinpath("airports")


def get_data_from_csv(
    dataset_path: Path,
    field_names: dict[str, str]
        ) -> list[dict]:
    """Get selective data from a csv dataset.

    :field_names: A dictionary used to both select the fields
        that should be imported and map their csv field names
        to application conformant field names.
    """

    data = []
    selected_fields = set(field_names.keys())

    with open(dataset_path, "r", encoding="UTF-8") as dataset_file:
        dict_reader = csv.DictReader(dataset_file)
        for entry in dict_reader:
            data.append(
                {
                    field_names[field]: value
                    for field, value in entry.items()
                    if field in selected_fields
                }
            )

    return data


def get_countries_data() -> list[dict]:
    """Get selective countries data from the OurAirports csv dataset.

    Currently the data imported is:
    * code: Country ISO 3166-1 alpha-2 codes.
    * name: Country names.
    """

    return get_data_from_csv(
        dataset_path=_DATASET_COUNTRIES,
        field_names={"code": "code", "name": "name"}
    )


def get_airports_data() -> list[dict]:
    """Get selective airport data from the OurAirports csv dataset.

    Currently the data imported is:
    * iso_country->country_code: Airport country ISO 3166-1 alpha-2 codes.
    * type: A size and usage classification of the airport.
    * iata_code: Airport IATA codes.
    * name: Airport names.
    * municipality: Airport municipalities.

    """

    return get_data_from_csv(
        dataset_path=_DATASET_AIRPORTS,
        field_names={
            "iso_country": "country_code",
            "type": "type",
            "iata_code": "iata_code",
            "name": "name",
            "municipality": "municipality",
        },
    )
