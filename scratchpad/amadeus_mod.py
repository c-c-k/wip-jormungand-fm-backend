import datetime as dt
import importlib
import json
from pathlib import Path
from pprint import pprint
import time

from jormungand.core.config import config
from jormungand.providers.amadeus import auth
from jormungand.providers.amadeus import flight_offers_search

DUMP_ROOT = Path(__file__).parent.resolve().joinpath("data_dumps")


def dump_data(data: dict,
              base_name: str,
              print_before: bool = False,
              print_after: bool = False,
              add_timestamp: bool = False):
    if print_before:
        pprint(data)
    if add_timestamp:
        base_name += dt.datetime.now().strftime("_%Y%m%dT%H%M%S")
    file_path = (DUMP_ROOT.joinpath(base_name + ".json"))
    with open(file_path, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)
    if print_after:
        with open(file_path, "r", encoding="UTF-8") as f:
            pprint(json.load(f))


def load_data(fname: str):
    file_path = (DUMP_ROOT.joinpath("".join((fname, ".json"))))
    with open(file_path, "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


def spad_get_auth_data_full():
    importlib.reload(auth)
    time.sleep(1)
    data = auth._get_amadeus_auth_token()
    data['access_token'] = '[a-zA-Z0-9]{28}'
    data['application_name'] = 'AppName'
    data['client_id'] = '[a-zA-Z0-9]{32}'
    data['username'] = 'user@email.com'
    dump_data(data, "auth_token", print_after=True)


def spad_get_auth_header():
    importlib.reload(auth)
    time.sleep(1)
    # config["amadeus.next_refresh"] = None
    token = auth.get_auth_header()
    print("token from get_token: ", token)
    print("expires: ", time.ctime(config["amadeus.next_refresh"]))
    print("now:     ", time.ctime(time.time()))


def spad_flights_offers_search_one_way():
    importlib.reload(flight_offers_search)
    depart_date = dt.date.today() + dt.timedelta(days=2)
    params = {
            "originLocationCode": "TLV",
            "destinationLocationCode": "LAS",
            "departureDate": depart_date.strftime("%Y-%m-%d"),
            "adults": 1,
    }
    data = flight_offers_search.flight_offers_search(params)
    dump_data(data, "flights_search_one_way")


def spad_flights_offers_search_two_way():
    importlib.reload(flight_offers_search)
    depart_date = dt.date.today() + dt.timedelta(days=2)
    return_date = depart_date + dt.timedelta(days=7)
    params = {
            "originLocationCode": "TLV",
            "destinationLocationCode": "LAS",
            "departureDate": depart_date.strftime("%Y-%m-%d"),
            "returnDate": return_date.strftime("%Y-%m-%d"),
            "adults": 1,
    }
    data = flight_offers_search.flight_offers_search(params)
    dump_data(data, "flights_search_two_way")


def main():
    # spad_get_auth_data_full()
    # spad_get_auth_header()
    # spad_flights_offers_search_one_way()
    # spad_flights_offers_search_two_way()
    pass
