"""
GX Core 1.x end-to-end demo: pandas, in-process, no external DB.
Run:  pip install great_expectations  &&  python run_gx_validation.py
"""
import pandas as pd
import great_expectations as gx
from great_expectations import expectations as gxe

# 1. Build a small DataFrame in-process (swap for pd.read_csv("data.csv") if you have a file)
df = pd.DataFrame(
    {
        "id": [1, 2, 3, 4, 5],
        "passenger_count": [1, 2, 3, 2, 1],
        "fare_amount": [5.50, 12.00, 7.25, 99.00, 3.10],
    }
)

# 2. Ephemeral in-memory context (deterministic: no disk, no auto-detected gx/ dir)
context = gx.get_context(mode="ephemeral")

# 3. Data Source -> Asset -> Batch Definition (whole-dataframe batch)
data_source = context.data_sources.add_pandas(name="pandas_source")
asset = data_source.add_dataframe_asset(name="trips_asset")
batch_definition = asset.add_batch_definition_whole_dataframe("trips_batch_def")

# 4. Build an Expectation Suite and add Expectations
suite = context.suites.add(gx.ExpectationSuite(name="trips_suite"))
suite.add_expectation(
    gxe.ExpectColumnValuesToNotBeNull(column="id")
)
suite.add_expectation(
    gxe.ExpectColumnValuesToBeBetween(
        column="passenger_count", min_value=1, max_value=6
    )
)
suite.add_expectation(
    gxe.ExpectColumnValuesToBeBetween(
        column="fare_amount", min_value=0, max_value=50  # 99.00 will FAIL -> demonstrates a real check
    )
)

# 5. Bind suite to the batch via a Validation Definition, then run
validation_definition = context.validation_definitions.add(
    gx.ValidationDefinition(
        name="trips_validation",
        data=batch_definition,
        suite=suite,
    )
)
result = validation_definition.run(
    batch_parameters={"dataframe": df}
)

# 6. Inspect results
print("Overall success:", result.success)
for r in result.results:
    exp = r.expectation_config.type
    col = r.expectation_config.kwargs.get("column")
    print(f"  [{ 'PASS' if r.success else 'FAIL' }] {exp} (column={col})")

# 7. (Optional) static HTML Data Docs - requires a file context, not ephemeral:
#    fctx = gx.get_context(mode="file")  # then re-add source/suite/validation on fctx
#    fctx.build_data_docs()              # writes uncommitted/data_docs/local_site/index.html
