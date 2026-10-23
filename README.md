# gx-sandbox-demo

A minimal, end-to-end [Great Expectations](https://github.com/fivetran/great_expectations) (GX Core 1.x) data-quality demo. It builds a small pandas DataFrame in memory, defines an expectation suite, and validates the data — no external database, no warehouse, no config files.

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

Because the demo is just `pip install great_expectations` + one file, it runs in any
ephemeral code sandbox. The [`sandboxes/`](sandboxes/) package gives every provider one
interface:

```bash
python sandboxes/run.py --list      # show providers + status
python sandboxes/run.py islo        # run gx_demo.py in an islo.dev microVM
python sandboxes/run.py crabbox     # run in a local Apple container (brokerless)
```

| Provider | Type | Status |
|---|---|---|
| [islo.dev](https://islo.dev) | Cloud Firecracker microVM | Verified (reference) |
| [crabbox.sh](https://crabbox.sh) (`apple-container`) | Local Apple container | Verified |
| [Daytona](https://www.daytona.io) | Cloud AI sandbox (SDK) | Implemented, not verified end to end |
| [Modal](https://modal.com) | Serverless containers | Not implemented |
| [E2B](https://e2b.dev) | Code Interpreter sandbox | Not implemented |
| [Tensorlake](https://www.tensorlake.ai) | Document/data infra (not a sandbox) | Not a runner; possible data source, not implemented |

The verified runners (islo.dev, crabbox) produce identical output. See [`sandboxes/README.md`](sandboxes/README.md) for
the provider contract, how to add one, and why Tensorlake is a data source — not a sandbox.

## Requirements

Python 3.10–3.13. Dependencies are pinned to sane lower bounds in [`requirements.txt`](requirements.txt). CI runs both scripts plus a `ruff` lint across Python 3.10, 3.11, 3.12, and 3.13 — see [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Notes

Great Expectations source: [github.com/fivetran/great_expectations](https://github.com/fivetran/great_expectations) (the old `great-expectations/great_expectations` URL redirects there).

## License

[Apache-2.0](LICENSE).
