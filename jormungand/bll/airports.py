"""
Business logic related to aiports.

"""

from typing import ClassVar

from pydantic import BaseModel, Field, validator, ValidationError

from .base import gen_clean_data
from jormungand.dal import (
    oa_countries_get_all, countries_get_code_to_id_map, countries_init_data,
    oa_airports_get_all, airports_init_data)


class AirportBasicQuery(BaseModel):
    """Validator for basic airport search queries.

    .. note::
        The only accepted characters are unicode alphanumeric characters
        and unicode whitespaces. This is fairly restrictive as it precludes
        someone from e.g. copy-pasting a name that contains punctuation,
        however properly addressing such a usecase would require a smart
        search algorithm that would be able to handle different spellings
        for the same name, which is out of scope for this project at the
        moment.

    :query: The query string to be validated
    """
    query: str = Field(regex=r"(?u)[\w\s]{2,64}")


class AirportShortInfo(BaseModel):
    """Brief airport information meant for basic search results.

    :country_code: country code of the country that hosts the airport.
    :iata_code: aiport IATA code.
    :country_name: country name of the country that hosts the airport.
    :municipality: name of the municipality that hosts the airport.
    :name: airport name.
    """
    country_code: str = Field(regex=r"^[A-Z]{2}$")
    iata_code: str = Field(regex=r"^[A-Z]{3}$")
    country_name: str = Field(min_length=2)
    municipality: str = Field(min_length=2)
    name: str = Field(min_length=2)
    
    class Config:
        extra = "ignore"


def find_airports(query: str) -> list[AirportShortInfo]:
    """Find and return a list of airports matching a query substring.

    The query is matched against an airport's IATA code, country code,
    country name, municipality and airport name.

    :query: The query substring to be searched for.
    :returns: A list of airports matching the query.
    """
    try:
        query = AirportBasicQuery(query=query)
    except ValidationError as err:
        x = (query, err)
    raise Exception
