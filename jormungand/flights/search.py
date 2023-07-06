from pydantic import ValidationError

from .validation.models import FlightsSearch


def search_flights(**kwargs):
    try:
        flights_search = FlightsSearch(**kwargs)
    except ValidationError as err:
        payload = err.json(err.json())

    response = payload  # TODO: this is a placeholder for a proper response
    return response
