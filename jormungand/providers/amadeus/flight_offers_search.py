"""Wrapper for Amadeus: Flight Offers Search API
"""
import requests

from jormungand.core.config import config
from .auth import get_auth_header

_ROOT_URL = config["amadeus.root_url"]
_API_URL = _ROOT_URL + "/v2/shopping/flight-offers"


def flight_offers_search(params: dict):
    response = requests.get(_API_URL, headers=get_auth_header(), params=params)
    return response.json()
