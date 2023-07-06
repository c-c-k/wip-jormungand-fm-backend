"""Wrapper for Amadeus: Flight Offers Search API
"""
from copy import deepcopy
import requests

from jormungand.core.config import config
from jormungand.flights.validation.models import FlightsSearch
from .auth import get_auth_header
from . import mongodb

_ROOT_URL = config["amadeus.root_url"]
_API_URL = _ROOT_URL + "/v2/shopping/flight-offers"
_SEARCH_PARAMS_TEMPLATE = {
        "originLocationCode": None,
        "destinationLocationCode": None,
        "departureDate": None,
        "returnDate": None,
        "adults": 1,
}
_mongodb_collection = "AmadeusFlightsCache"


def _amadeus_flight_offers_search(params: dict) -> dict:
    response = requests.get(_API_URL, headers=get_auth_header(), params=params)
    return response.json()


def _format_search_params(fsp: FlightsSearch) -> dict:
    formatted_params = deepcopy(_SEARCH_PARAMS_TEMPLATE)
    formatted_params = formatted_params.update({
            "originLocationCode": fsp.origin,
            "destinationLocationCode": fsp.destination,
            "departureDate": fsp.departure_date,
            "returnDate": fsp.return_date,
    })
    return formatted_params
        
    


def _cached_flight_offers_search(params: dict) -> dict:
    return None  # TODO: implement flight search caching


def _cache_flights_search_result(params: dict,
                                 flight_search_results: dict) -> dict:
    db = mongodb.get_db()
    flight_search_results["search_params"] = params
    result = db[_mongodb_collection].insert_one({
        })



def _format_search_result(result: dict):  # -> BasicFlightsListing:
    pass


def search_flights(flights_search_params: FlightsSearch):
    formatted_params = _format_search_params(flights_search_params)

    result = _cached_flight_offers_search(formatted_params)
    if result is None:
        result = _amadeus_flight_offers_search(formatted_params)
        result = _cache_flights_search_result(formatted_params, result)

    formatted_result = _format_search_result(result)
    return formatted_result
