from typing import Any, Optional

import dlt
from dlt.common.pendulum import pendulum
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources


@dlt.source(name="logfire")
def logfire_source(
    read_token: Optional[str] = dlt.secrets.value,
    sql: str = "SELECT * FROM records",
    days_back: int = 7,
) -> Any:
    """Load data from the Pydantic Logfire Query API.

    Args:
        read_token: Logfire read token. Auto-loaded from secrets.toml.
        sql: SQL query to run against Logfire's data (e.g. `records` table).
        days_back: How many days of history to include via `min_timestamp`.

    Example:
        pipeline.run(logfire_source())
        pipeline.run(
            logfire_source(sql="SELECT * FROM records LIMIT 100", days_back=1)
        )
    """
    min_timestamp = (
        pendulum.now("UTC").subtract(days=days_back).to_iso8601_string()
    )

    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://logfire-eu.pydantic.dev/",
            "auth": {
                "type": "bearer",
                "token": read_token,
            },
            "headers": {
                "Accept": "application/json",
            },
        },
        "resources": [
            {
                "name": "records",
                "endpoint": {
                    "path": "v2/query",
                    "method": "POST",
                    "json": {
                        "sql": sql,
                        "min_timestamp": min_timestamp,
                    },
                    "data_selector": "data",
                    "paginator": {"type": "single_page"},
                },
            },
        ],
    }

    yield from rest_api_resources(config)


def load_logfire() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_logfire",
        destination="duckdb",
        dataset_name="logfire_data",
        dev_mode=True,
    )

    load_info = pipeline.run(
        logfire_source().add_limit(1),
        write_disposition="replace",
    )
    print(load_info)  # noqa: T201


if __name__ == "__main__":
    load_logfire()
