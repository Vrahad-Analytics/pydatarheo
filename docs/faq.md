# PyDataRheo Frequently Asked Questions

**1. Is PyDataRheo a replacement for a data integration platform?**

No. PyDataRheo is a Python library. It has no orchestration, scheduling, alerting, or pipeline
monitoring, and it does not run as a service. Run it inside whatever scheduler you already use,
such as Airflow, Dagster, Prefect, or cron.

**2. What is the PyDataRheo cache? Is it a destination?**

Effectively yes. It is a built-in destination implementation backed by a SQL engine. We call it a
cache rather than a destination to keep it distinct from the destination *connectors*, which are
separate executables that PyDataRheo launches.

**3. Does PyDataRheo work with orchestration frameworks like Airflow, Dagster, and Snowpark?**

Yes. It is an ordinary Python dependency with no background services, so it runs fine inside a
task or an operator.

**4. Which connectors can PyDataRheo run?**

Any connector that implements the Airbyte protocol, which covers several hundred published
sources and destinations, plus any connector you write yourself that speaks the same protocol.

**5. Can I use PyDataRheo to develop or test a connector I am building?**

Yes. It makes connectors easy to drive from Python, which is useful both for new local connectors
and for already-published ones.

**6. Can I build a traditional ETL pipeline with it?**

Yes. Choose the cache type that matches where the data should land, such as `SnowflakeCache` for
Snowflake or `BigQueryCache` for BigQuery.

**7. Can PyDataRheo run a connector from a local directory instead of installing from PyPI?**

Yes. Any connector that exposes a CLI works, and connectors already on `PATH` are found by name.

**8. My environment is configured with `AIRBYTE_*` variables. Do I need to rename them?**

Not immediately. PyDataRheo reads `DATARHEO_`-prefixed variables, and falls back to the matching
`AIRBYTE_` name when the new one is unset. Setting the `DATARHEO_` name always wins.

**9. Does PyDataRheo phone home?**

Not unless you ask it to. Usage reporting is off by default and has no default endpoint. It sends
data only when you set `DATARHEO_TRACKING_KEY` to a Segment write key you own.
