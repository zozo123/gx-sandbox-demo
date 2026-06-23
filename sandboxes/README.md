# Running the demo in a sandbox

The demo is intentionally provider-agnostic — it's just `pip install great_expectations`
plus a single Python file — so it runs in any ephemeral sandbox. This directory holds
thin launchers for three providers.

| Provider | Type | Broker / key | File transfer | Status |
|---|---|---|---|---|
| **islo.dev** | Cloud Firecracker microVM | `islo login` | stdin inject (no cwd sync) | ✅ Verified (Py 3.12.13) |
| **crabbox.sh** (`apple-container`) | Local Apple container | None (brokerless) | git checkout sync | ✅ Verified |
| **Daytona** | Cloud AI sandbox | `DAYTONA_API_KEY` | SDK upload | 📄 Documented (SDK; not run in CI) |

> **Note:** "AI sandbox" here means a *code-execution* runtime. Tools like **Tensorlake**
> are **not** sandboxes — they're document-ingestion / data infrastructure. Tensorlake
> would sit *upstream* of GX (parse documents → rows → GX validates them), not as a place
> to execute this script.

## islo.dev

```bash
sandboxes/run_islo.sh            # injects gx_demo.py over stdin into python:3.12-slim
```

## crabbox.sh (Apple container, brokerless)

```bash
sandboxes/run_crabbox.sh         # syncs the checkout into a local Apple container
```

## Daytona

```bash
pip install daytona
export DAYTONA_API_KEY=...        # from app.daytona.io
python sandboxes/run_daytona.py   # create → upload → exec → delete
```

All three produce the same deterministic output (one expectation fails by design):

```
overall: FAIL
  [PASS] expect_column_values_to_not_be_null(id)
  [PASS] expect_column_values_to_be_between(passenger_count)
  [FAIL] expect_column_values_to_be_between(fare_amount)
```
