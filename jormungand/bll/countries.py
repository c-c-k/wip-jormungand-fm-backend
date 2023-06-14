"""Buisness logic related to countries.

"""

from pydantic import BaseModel, Field

from .base import gen_clean_data
from jormungand.dal import (
    oa_countries_get_all, countries_del_all, countries_add_many)


class CountryModel(BaseModel):
    """Country data pydantic model

    :code: Country ISO 3166-1 alpha-2 code.
        2 letters, will be converted to uppercase.
    :name: country name.
        2 characters minimum.
    """
    code: str = Field(to_upper=True, regex=r'^[a-zA-Z]{2}$')
    name: str = Field(min_length=2)


def import_oa_country_data():
    """Import country data from the OurAirports.com datasets.

    Currently the data imported is:
    * Country ISO 3166-1 alpha-2 codes.
    * Country names.

    .. note::
        Since the OurAirports country data is relatively small, static
        and complete this function is meant to to be run once/infrequently
        and is not meant to play along with import of data from other
        data-sources (i.e. it's implementation takes a simple delete
        existing data and import fresh data approach).
    """

    countries_del_all()
    countries_data = oa_countries_get_all()
    cleaned_countries_data = gen_clean_data(countries_data, CountryModel)
    countries_add_many(cleaned_countries_data)
