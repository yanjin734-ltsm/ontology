# jaffle-duckdb

Ontology Space for the dbt-labs `jaffle_shop_duckdb` warehouse.

This is the product demo. Use DuckDB only.

Do not use `examples/v5-jaffle` with this warehouse.
That fixture is a simplified postgres-shaped Space (`public`, `id`/`name`).
dbt DuckDB tables live in catalog `jaffle_shop` (attach alias from
`jaffle_shop.duckdb`), schema `main`, columns `customer_id` / `first_name`.

Query model names (`FROM customers`), not `wren.public.customers`.
`catalog: wren` in `wren_project.yml` is the Space namespace, not a DuckDB catalog.
