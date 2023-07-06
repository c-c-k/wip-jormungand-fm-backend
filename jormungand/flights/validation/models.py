from datetime import date
from typing import Annotated

from pydantic import BaseModel, validator, Field

from jormungand.common.annotated_fields import IATACodeField
from jormungand.common.validators import normalize_char_code


class FlightsSearch(BaseModel):
    origin: IATACodeField
    destination: IATACodeField
    departure_date: date
    return_date: date | None = None

    _normalize_origin_and_destination = validator(
            "origin", "destination", allow_reuse=True,
            pre=True)(normalize_char_code)

    @validator("destination")
    def origin_different_from_destination(cls, destination, values, **kwargs):
        if ("origin" in values) and (values["origin"] == destination):
            raise ValueError(
                    "Origin and destination airports can't be the same")
        return destination

    @validator("return_date")
    def no_departure_before_return(cls, return_date, values, **kwargs):
        if ("departure_date" in values) and (values["departure_date"]
                                             > return_date):
            raise ValueError("Return date can't precede departure date")
        return return_date

    class Config:
        extra = "ignore"


# class BasicFlightInfo(BaseModel):
#     # id: Annotated[int, Field(
#     pass


# class BasicFlightsListing(BaseModel):
#     original_search_id: "id"
#     flights: list[BasicFlightInfo]
