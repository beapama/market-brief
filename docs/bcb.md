# Banco Central SGS collector

Module: [`src/market_brief/bcb.py`](../src/market_brief/bcb.py)

Collects macroeconomic indicators from the **SGS** (*Sistema Gerenciador de Séries Temporais*),
the Banco Central do Brasil's public time-series API. No authentication is required.

## The API

Each indicator is an independent series identified by a numeric code:

```
GET https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados/ultimos/{n}?formato=json
```

Response (oldest point first; dates in `dd/mm/yyyy`; values as **strings**):

```json
[{"data": "04/11/2026", "valor": "5.4778"}, {"data": "05/11/2026", "valor": "5.4621"}]
```

An unknown series code returns **HTTP 404** with a plain-text body (`A serie nao existe!`), not JSON.

## Series collected

| Key            | Code  | Indicator                                 | Frequency | Notes |
|----------------|-------|-------------------------------------------|-----------|-------|
| `selic_target` | 432   | Selic target rate (% p.a.), set by Copom  | Daily     | Published with **future dates**: the value in force is repeated for upcoming days. |
| `ipca_12m`     | 13522 | IPCA, 12-month accumulated inflation (%)  | Monthly   | Released with a lag of roughly one month; the date is the 1st day of the reference month. |
| `ptax_sell`    | 1     | USD/BRL PTAX exchange rate, sell (R$)     | Business days | Not published on weekends and holidays. |

## Functions

### `fetch_sgs_series(code, last=1, timeout=10.0) -> list[dict]`

Low-level function: fetches the last `last` points of **one** series and returns them with proper
types, hiding the API's quirks (Portuguese keys, Brazilian date format, values as strings).

```python
[{"date": date(2026, 11, 5), "value": 5.4621}]
```

It raises `BCBFetchError` on any expected failure. It does not decide what to do with the error.

### `collect_bcb_indicators(series=SGS_SERIES_CODES) -> dict`

High-level function: calls `fetch_sgs_series` once per series and keeps the most recent point.
The output is JSON-serializable (dates as ISO strings), ready to be saved in the daily snapshot.

```json
{
  "data": {
    "selic_target": {"date": "2026-12-09", "value": 13.75},
    "ptax_sell":    {"date": "2026-11-05", "value": 5.4621}
  },
  "errors": {
    "ipca_12m": "Request failed for series 13522: 503 Server Error: ..."
  }
}
```

## Error handling strategy

The goal is that **one failing series never stops the whole run**. If the IPCA request times out,
the daily briefing should still be produced with the Selic and the dollar.

1. **Every request has a timeout.** `requests` has no default timeout. Without one, a stalled
   server would hang the GitHub Actions job until it is killed.
2. **All expected failures become a single exception type.** `fetch_sgs_series` translates them
   into `BCBFetchError`, chained with `raise ... from e` so the original cause stays in the traceback:

   | Failure                        | Original exception                           |
   |--------------------------------|----------------------------------------------|
   | Network down, DNS, timeout     | `requests.ConnectionError`, `requests.Timeout` |
   | HTTP 4xx/5xx                   | `requests.HTTPError` (via `raise_for_status()`) |
   | Body is not JSON               | `requests.JSONDecodeError`                    |
   | Empty response                 | explicit check                               |
   | Missing key or malformed value | `KeyError`, `ValueError`                      |

   The first three all inherit from `requests.RequestException`, so one `except` covers them.
3. **Failures are isolated per series.** `collect_bcb_indicators` catches only `BCBFetchError`
   inside the loop, logs a warning and records the message in `errors`. Unexpected exceptions
   (real bugs) are deliberately **not** caught, so they surface instead of being hidden.

## Running

```powershell
python src/market_brief/bcb.py
```

## Open questions

- **Selic date:** series 432 returns future dates, so the "latest" point may be dated weeks ahead.
  Decide how the briefing and charts should present it (e.g. use the collection date instead).
