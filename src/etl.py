import json
import os
import time
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Iterable, List, Union

import click
import pandas as pd
import requests
from sodapy import Socrata

ENDPOINT_HISTORIC = "qgea-i56i"
ENDPOINT_YTD = "5uac-w243"
COMPLAINT_ID_COL = "CMPLNT_NUM"


def fetch_complaints(
    *endpoints: Iterable[str], how: str = "url", write: bool = False
) -> List[Union[pd.DataFrame, str]]:
    """Retrieve NYPD complaints data and optionally write to disk."""
    latest_path = os.path.join(os.getenv("REPO_ROOT"), "data", str(time.time_ns()))

    complaints = []
    for endpoint in endpoints:
        if how == "api":

            def _reader(data):
                return pd.DataFrame.from_records(data)

            def _writer(data, out_path):
                with open(out_path, "w") as f:
                    json.dump(list(data), f)

            ext = "json"
            client = Socrata("data.cityofnewyork.us", None)
            data = client.get_all(endpoint)

        elif how == "url":

            def _reader(data):
                return pd.read_csv(BytesIO(data.content))

            def _writer(data, out_path):
                with open(out_path, "wb") as f:
                    f.write(data.content)

            ext = "csv"
            data = requests.get(
                f"https://data.cityofnewyork.us/api/views/{endpoint}/rows.csv"
            )

        else:
            raise NotImplementedError(
                "The keyword argument `how` must be one of 'api' or 'url'."
            )

        if write:
            Path(latest_path).mkdir(parents=True, exist_ok=True)
            out_path = os.path.join(latest_path, f"{endpoint}.{ext}")
            _writer(data, out_path)
            complaints.append(out_path)

        else:
            complaints.append(_reader(data))

    return complaints


def _nanos_or_neg(s: str) -> int:
    try:
        i = int(s)
        return i
    except ValueError:
        return -1


def get_latest_concatenated(
    endpoints: Iterable[str] = (ENDPOINT_HISTORIC, ENDPOINT_YTD)
) -> pd.DataFrame:
    data_path = os.path.join(os.getenv("REPO_ROOT"), "data")
    data_walk = os.walk(data_path)
    subdirectories = next(data_walk)[1]
    latest_caches = {}

    @dataclass
    class Cache:
        endpoint: str
        nanos: int
        extension: str
        data_path: str

        def __post_init__(self):
            self.path = os.path.join(
                self.data_path, str(self.nanos), self.endpoint + self.extension
            )

        def __call__(self):
            if self.extension not in (".csv", ".json"):
                raise NotImplementedError(f"Invalid extension `{self.extension}`.")
            _reader = pd.read_csv if (self.extension == ".csv") else pd.read_json
            return _reader(self.path)

    for i in range(len(subdirectories)):
        data_step = next(data_walk)
        nanos = _nanos_or_neg(subdirectories[i])
        if nanos > 0:
            for filename in data_step[2]:
                endpoint, extension = os.path.splitext(filename)
                if endpoint in endpoints:
                    if (endpoint not in latest_caches) or (
                        nanos > latest_caches[endpoint].nanos
                    ):
                        latest_caches[endpoint] = Cache(
                            endpoint, nanos, extension, data_path
                        )

    return (
        pd.concat(cache() for cache in latest_caches.values())
        .sort_values(COMPLAINT_ID_COL)
        .drop_duplicates(COMPLAINT_ID_COL)
        .set_index(COMPLAINT_ID_COL, drop=False)
    )


@click.command()
@click.argument("endpoints", nargs=-1)
def local_copy(endpoints: Iterable[str]):
    if len(endpoints) == 0:
        endpoints = [ENDPOINT_YTD, ENDPOINT_HISTORIC]
    click.echo(f"Fetching data from {', '.join(endpoints)}.")
    fetch_complaints(*endpoints, write=True)


if __name__ == "__main__":
    local_copy()
