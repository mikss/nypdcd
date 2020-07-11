import os
import time
from pathlib import Path

import click
import pandas as pd
from sodapy import Socrata

ENDPOINT_HISTORIC = "qgea-i56i"
ENDPOINT_YTD = "5uac-w243"
COMPLAINT_ID_COL = "cmplnt_num"


def fetch_complaints(*endpoints, write=False):
    """Retrieve NYPD complaints data and optionally write to disk."""
    client = Socrata("data.cityofnewyork.us", None)
    current_nanos = time.time_ns()
    df = (
        pd.concat(
            pd.DataFrame.from_records(client.get_all(endpoint))
            for endpoint in endpoints
        )
        .sort_values(COMPLAINT_ID_COL)
        .drop_duplicates(COMPLAINT_ID_COL)
        .set_index(COMPLAINT_ID_COL, drop=False)
    )
    if write:
        path = os.path.join(
            os.getenv("REPO_ROOT"), f"data/{current_nanos}/complaints.csv"
        )
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path)
        return path
    else:
        return df


def _nanos_or_zero(s):
    try:
        i = int(s)
        return i
    except ValueError:
        return 0


def get_latest_cached(filename="complaints.csv"):
    dirs = os.listdir(os.path.join(os.getenv("REPO_ROOT"), "data"))
    latest_nanos = max(_nanos_or_zero(d) for d in dirs)
    return pd.read_csv(
        os.path.join(os.getenv("REPO_ROOT", f"data/{latest_nanos}/{filename}"))
    )


@click.command()
@click.argument("endpoints", nargs=-1)
def local_copy(endpoints):
    if len(endpoints) == 0:
        endpoints = [ENDPOINT_YTD, ENDPOINT_HISTORIC]
    click.echo(f"Fetching data from {', '.join(endpoints)}.")
    fetch_complaints(*endpoints, write=True)


if __name__ == "__main__":
    local_copy()
