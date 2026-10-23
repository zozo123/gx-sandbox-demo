# Pan-provider sandbox runners

The demo is provider-agnostic — it's just `pip install great_expectations` plus one
file — so it runs in any ephemeral code sandbox. This package exposes **one interface**
across providers:

```bash
python sandboxes/run.py --list            # show providers + status
python sandboxes/run.py islo              # run gx_demo.py in islo.dev
python sandboxes/run.py crabbox           # run in a local Apple container
python sandboxes/run.py daytona my.py     # run a different script
```

Every provider implements the same contract in [`providers.py`](providers.py):

```python
def run(script: str = "gx_demo.py") -> str:  # execute the script, return stdout
```

## Providers

| Provider | Type | Auth | Status |
|---|---|---|---|
| **islo.dev** | Cloud Firecracker microVM | `islo login` | Verified (reference) |
| **crabbox** (`apple-container`) | Local Apple container, brokerless | none | Verified |
| **Daytona** | Cloud AI sandbox (SDK) | `DAYTONA_API_KEY` | Implemented, not verified end to end |
| **Modal** | Serverless containers | `modal token` | Not implemented |
| **E2B** | Code Interpreter sandbox | `E2B_API_KEY` | Not implemented |
| **Tensorlake** | Document-ingestion / data infra | — | Not a sandbox; not implemented |

> **Why Tensorlake is not a runner:** it's document-ingestion / data infrastructure, not a
> code-execution sandbox. It would belong *upstream* of GX as a **data source** (parse documents
> → rows → GX validates them), not as a `run()` provider. That integration is not implemented.

## Adding a provider

1. Add a `run_<name>(script=...) -> str` function in `providers.py` (import any SDK **lazily**
   inside the function so the module stays importable without optional deps).
2. Register it in the `PROVIDERS` dict with a `status`.
3. Verify it produces the canonical output, then update its status here and in the top-level README.

The verified runners (islo.dev, crabbox) produce identical output (one expectation fails by design):

```
overall: FAIL
  [PASS] expect_column_values_to_not_be_null(id)
  [PASS] expect_column_values_to_be_between(passenger_count)
  [FAIL] expect_column_values_to_be_between(fare_amount)
```
