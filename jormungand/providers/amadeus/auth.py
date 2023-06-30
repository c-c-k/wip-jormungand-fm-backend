"""Authentication and authorization for the Amadeus interface package.
"""
import time
import requests

from jormungand.core.config import config

_ROOT_URL = config["amadeus.root_url"]
_API_URL = _ROOT_URL + "/v1/security/oauth2/token"
_REQUEST_XFORM_DATA = {
        "grant_type": "client_credentials",
        "client_id": config["amadeus.key"],
        "client_secret": config["amadeus.secret"]
}
_NEXT_REFRESH_OFFSET = 5


def _token_requires_refresh():
    next_refresh = config.get("amadeus.next_refresh", None)
    requires_refresh = (next_refresh is None) or (time.time() > next_refresh)
    return requires_refresh


def _get_amadeus_auth_token():
    response = requests.post(_API_URL, data=_REQUEST_XFORM_DATA)
    return response.json()


def _refresh_token():
    auth_data = _get_amadeus_auth_token()
    if auth_data.get("state", "") == "approved":
        config["amadeus.access_token"] = auth_data["access_token"]
        config["amadeus.token_type"] = auth_data["token_type"]
        config["amadeus.next_refresh"] = (time.time() + auth_data["expires_in"]
                                          - _NEXT_REFRESH_OFFSET)
    else:
        raise Exception(str(auth_data))


def get_auth_header():
    if _token_requires_refresh():
        _refresh_token()
    auth_header = {
            "Authorization":
            " ".join((config["amadeus.token_type"],
                      config["amadeus.access_token"]))
    }
    return auth_header
