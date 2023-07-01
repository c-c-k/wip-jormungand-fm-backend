"""Wrapper for Amadeus: Flight Offers Pricing API.
"""
import requests

from jormungand.core.config import config
from .auth import get_auth_header

_ROOT_URL = config["amadeus.root_url"]
_API_URL = _ROOT_URL + "/v1/shopping/flight-offers/pricing"


def flight_offers_pricing(data: dict):
    response = requests.post(_API_URL, headers=get_auth_header(), json=data)
    return response.json()
