"""Collect indicators from the Banco Central do Brasil SGS API (time series system)."""

import json
import logging
from datetime import datetime

import requests

logger = logging.getLogger(__name__)

SGS_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados/ultimos/{last}"

SGS_SERIES: dict[str, int] = {
    "selic_target": 432,
    "ipca_12m": 13522,
    "ptax_sell": 1,
}


class BCBFetchError(Exception):
    """Failed to fetch or parse an SGS series."""


def fetch_sgs_series(code: int, last: int = 1, timeout: float = 10.0) -> list[dict]:
    """Fetch the latest `last` data points of an SGS series.

    Returns: [{"date": date(2026, 11, 4), "value": 15.0}, ...]
    Raises: BCBFetchError on any failure (network, timeout, HTTP, format).
    """

    sgs_url = SGS_URL.format(code=code, last=last)

    try:
        response = requests.get(sgs_url, params={"formato": "json"}, timeout=timeout)
        response.raise_for_status()
        points = response.json()
    except requests.RequestException as e:
        raise BCBFetchError(f"Request failed for series {code}: {e}") from e

    if not points:
        raise BCBFetchError(f"BCB returned no data for series {code}")

    sgs_series = []

    for item in points:
        try:
            sgs_series.append(
                {
                    "date": datetime.strptime(item["data"], "%d/%m/%Y").date(),
                    "value": float(item["valor"]),
                }
            )
        except (KeyError, ValueError) as e:
            raise BCBFetchError("Failed to parse") from e

    return sgs_series


def collect_bcb_indicators(series: dict[str, int] = SGS_SERIES) -> dict:
    """Collect the most recent point of each series, isolating failures.

    Returns: {"data": {name: {"date": "YYYY-MM-DD", "value": float}},
              "errors": {name: "message"}}
    """
    # For each (name, code): try fetch_sgs_series; on success, store the
    # latest point in "data" (date as ISO string); on BCBFetchError, record
    # it in "errors" and log a warning. Move on to the next series either way.
    raise NotImplementedError


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    result = collect_bcb_indicators()
    print(json.dumps(result, indent=2, ensure_ascii=False))
