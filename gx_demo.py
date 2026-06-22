"""Concise GX Core 1.x e2e demo: pandas, in-memory, no external DB."""
import pandas as pd
import great_expectations as gx
from great_expectations import expectations as gxe

df = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "passenger_count": [1, 2, 3, 2, 1],
    "fare_amount": [5.5, 12.0, 7.25, 99.0, 3.1],  # 99.0 trips the fare check
})

batch = (
    gx.get_context(mode="ephemeral")
    .data_sources.add_pandas("src")
    .add_dataframe_asset("trips")
    .add_batch_definition_whole_dataframe("bd")
    .get_batch(batch_parameters={"dataframe": df})
)

suite = gx.ExpectationSuite(name="trips", expectations=[
    gxe.ExpectColumnValuesToNotBeNull(column="id"),
    gxe.ExpectColumnValuesToBeBetween(column="passenger_count", min_value=1, max_value=6),
    gxe.ExpectColumnValuesToBeBetween(column="fare_amount", min_value=0, max_value=50),
])

res = batch.validate(suite)
print("overall:", "PASS" if res.success else "FAIL")
for r in res.results:
    c = r.expectation_config
    print(f"  [{'PASS' if r.success else 'FAIL'}] {c.type}({c.kwargs.get('column')})")
