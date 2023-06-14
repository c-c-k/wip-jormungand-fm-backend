"""Buisness logic related to airports.

"""

from typing import ClassVar

from pydantic import BaseModel, Field, ValidationError, validator

from jormungand.dal import (
    oa_airports_get_all, airports_del_all, airports_add_many,
    countries_get_code_to_id_map)


ACCEPTED_AIRPORT_TYPES = {"large_airport"}


class AirportModel(BaseModel):
    """Airport data pydantic model

    :airport_type: A size and usage classification of the airport.
        used to filter airports according to ACCEPTED_AIRPORT_TYPES.
        excluded from model export data.
    :iata_code: aiport IATA code.
        3 letters, will be converted to uppercase.
    :country_id: db pk for the country that hosts the airport.
    :country_code: country code of the country that hosts the airport.
        used to get country_id.
        excluded from model export data.
    :municipality: name of the municipality that hosts the airport.
        2 characters minimum.
    :name: airport name.
        2 characters minimum.
    """
    _country_code_to_id_map: None | ClassVar[dict[str, int]] = None
    airport_type: str = Field(exclude=True)
    iata_code: str = Field(to_upper=True, regex=r'^[a-zA-Z]{3}$')
    country_id: int | None = None
    country_code: str = Field(exclude=True)
    municipality: str = Field(min_length=2)
    name: str = Field(min_length=2)

    @validator("airport_type")
    def airport_type_filter(cls, v):
        if v not in ACCEPTED_AIRPORT_TYPES:
            raise ValueError("excluded airport type")

    @validator("country_code")
    def check_and_convert_country_code_to_id(cls, v, values):
        try:
            values["country_id"] = (AirportModel._country_code_to_id_map[v])
        except KeyError:
            raise ValueError(f"Unknown country code: {v}")


def _get_clean_airports_data(airports_data: list[dict]) -> list[dict]:
    cleaned_airports_data = []
    for airport_data in airports_data:
        try:
            airport_data = AirportModel(airport_data).dict()
        except ValidationError:
            continue
        cleaned_airports_data.append(airport_data)
    return cleaned_airports_data


def import_oa_airport_data():
    """Import airport data from the OurAirports.com datasets.

    Currently the data imported is:
    * country_code: Airport country ISO 3166-1 alpha-2 codes.
    * airport_type: A size and usage classification of the airport.
    * iata_code: Airport IATA codes.
    * name: Airport names.
    * municipality: Airport municipalities.

    .. note::
        Since the OurAirports airport data is relatively small, static
        and complete this function is meant to to be run once/infrequently
        and is not meant to play along with import of data from other
        data-sources (i.e. it's implementation takes a simple delete
        existing data and import fresh data approach).
    """

    airports_del_all()
    airports_data = oa_airports_get_all()
    AirportModel._country_code_to_id_map = countries_get_code_to_id_map()
    cleaned_airports_data = _get_clean_airports_data(airports_data)
    airports_add_many(cleaned_airports_data)
