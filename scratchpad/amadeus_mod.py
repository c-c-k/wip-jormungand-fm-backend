import datetime as dt
import importlib
import json
from pathlib import Path
from pprint import pprint
import time

from jormungand.core.config import config

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


def main():
    pass
