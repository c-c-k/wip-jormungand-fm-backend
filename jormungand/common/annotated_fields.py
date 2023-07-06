from typing import Annotated

from pydantic import Field

CountryCodeField = Annotated[
        str,
        Field(regex=r'^[A-Z]{2}$',
              description="Country 2 letter ISO 3166-1 alpha-2 code.")]

IATACodeField = Annotated[
        str,
        Field(regex=r'^[A-Z]{3}$',
              description="Airport 3 letter IATA code.")]
