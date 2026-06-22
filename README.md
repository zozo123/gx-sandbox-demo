# gx-sandbox-demo

A minimal, end-to-end [Great Expectations](https://github.com/great-expectations/great_expectations) (GX Core 1.x) data-quality demo. It builds a small pandas DataFrame in memory, defines an expectation suite, and validates the data — no external database, no warehouse, no config files.

One expectation **fails by design** so you can see that validation is actually running and not silently passing everything.

## What it checks

`gx_demo.py` validates a 5-row trips table against three expectations:

| Expectation | Column | Rule | Result |
|---|---|---|---|
| `ExpectColumnValuesToNotBeNull` | `id` | no nulls | PASS |
| `ExpectColumnValuesToBeBetween` | `passenger_count` | between 1 and 6 | PASS |
| `ExpectColumnValuesToBeBetween` | `fare_amount` | between 0 and 50 | FAIL (by design) |

The `fare_amount` column contains a `99.0` value, which is outside the `[0, 50]` range — so that expectation fails. The script reports the per-expectation results and exits 0 (it only prints results; it does not raise on failure).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python gx_demo.py
```

Expected output:

```
overall: FAIL
  [PASS] expect_column_values_to_not_be_null(id)
  [PASS] expect_column_values_to_be_between(passenger_count)
  [FAIL] expect_column_values_to_be_between(fare_amount)
```

There is also `run_gx_validation.py`, a more verbose variant that uses a GX `ValidationDefinition`. Both scripts produce the same outcome and exit 0.

## Run it in a sandbox

The demo has been run end-to-end on two ephemeral sandbox providers (both `python:3.12-slim`, identical output):

**[islo.dev](https://islo.dev)** — cloud Firecracker microVM. islo does not sync your working directory, so inject the script over stdin:

```bash
B64=$(base64 < gx_demo.py | tr -d '\n')
islo use gx-demo -i python:3.12-slim -- bash -lc \
  "pip install great_expectations && echo $B64 | base64 -d | python3 -"
```

**[crabbox.sh](https://crabbox.sh)** — local Apple `container` provider, brokerless. crabbox syncs your checkout, so run the file directly (requires a git repo):

```bash
crabbox run --provider apple-container --apple-container-image python:3.12-slim \
  -- bash -lc 'pip install -r requirements.txt && python gx_demo.py'
```

## Requirements

Python 3.10–3.13. Dependencies are pinned to sane lower bounds in [`requirements.txt`](requirements.txt). CI runs both scripts plus a `ruff` lint across Python 3.10, 3.11, 3.12, and 3.13 — see [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Notes

The canonical Great Expectations repository is [github.com/great-expectations/great_expectations](https://github.com/great-expectations/great_expectations) (`great_expectations` 1.x, Python 3.10–3.13). The `fivetran/great_expectations` URL redirects to the same repo.

## License

[Apache-2.0](LICENSE).
