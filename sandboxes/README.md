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

| Provider | Type | Auth | Status | Issue |
|---|---|---|---|---|
| **islo.dev** | Cloud Firecracker microVM | `islo login` | ✅ Verified (reference) | — |
| **crabbox** (`apple-container`) | Local Apple container, brokerless | none | ✅ Verified | — |
| **Daytona** | Cloud AI sandbox (SDK) | `DAYTONA_API_KEY` | 🟡 Implemented; verify e2e | [#8](https://github.com/zozo123/gx-sandbox-demo/issues/8) |
| **Modal** | Serverless containers | `modal token` | ⬜ Planned | [#6](https://github.com/zozo123/gx-sandbox-demo/issues/6) |
| **E2B** | Code Interpreter sandbox | `E2B_API_KEY` | ⬜ Planned | [#7](https://github.com/zozo123/gx-sandbox-demo/issues/7) |
| **Tensorlake** | Document-ingestion / data infra | — | ❌ Not a sandbox | [#9](https://github.com/zozo123/gx-sandbox-demo/issues/9) |

Tracking: [#5](https://github.com/zozo123/gx-sandbox-demo/issues/5).

> **Why Tensorlake is not a runner:** it's document-ingestion / data infrastructure, not a
> code-execution sandbox. It belongs *upstream* of GX as a **data source** (parse documents
> → rows → GX validates them), so it's tracked as a data-source integration (#9), not a `run()`
> provider.

## Adding a provider

1. Add a `run_<name>(script=...) -> str` function in `providers.py` (import any SDK **lazily**
   inside the function so the module stays importable without optional deps).
2. Register it in the `PROVIDERS` dict with a `status`.
3. Verify it produces the canonical output and close the provider's tracking issue.

All providers produce the same deterministic output (one expectation fails by design):

```
overall: FAIL
  [PASS] expect_column_values_to_not_be_null(id)
  [PASS] expect_column_values_to_be_between(passenger_count)
  [FAIL] expect_column_values_to_be_between(fare_amount)
```
