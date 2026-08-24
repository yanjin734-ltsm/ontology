# Ontology Space shell tutorial

Product demo warehouse is **DuckDB only**. Do not mix in Postgres or MySQL.

Official Wren still says MDL. We compile the same Manifest to `target/mdl.json`.
The project is an Ontology Space. `catalog: wren` in `wren_project.yml` is the
Space namespace, not a DuckDB catalog.

## Two different "jaffle" things

| Thing | What it is | Use it? |
|---|---|---|
| `dbt-labs/jaffle_shop_duckdb` | The warehouse. After `dbt build` you get `jaffle_shop.duckdb` with schema `main` and columns like `customer_id`, `first_name`. | Yes. This is the demo database. |
| `examples/jaffle-duckdb` | Our Space YAML, written for that DuckDB mart. | Yes. Copy this into a new Space directory. |
| `examples/v5-jaffle` | Inherited postgres-shaped fixture (`public`, `id`/`name`, `raw_orders`). | No. Not for this tutorial. Official Wren users who drop it on dbt DuckDB hit the same errors. |

`generate-space` (alias of `generate-mdl`) introspects a live database and
writes models. Use that for any other warehouse. For this demo, copy
`examples/jaffle-duckdb`.

## Command map

- `pip install wrenai` → `pip install ontology-cli`
- `npx skills add Canner/WrenAI` → `npx skills add yanjin734-ltsm/ontology`
- `wren` → `ontology`
- `~/.wren` → `~/.ontology`
- `generate-mdl` / `--mdl` still work; prefer `generate-space` / `--space`

## 0. Virtualenv

```bash
python3 -m venv ~/.venvs/ontology
source ~/.venvs/ontology/bin/activate
```

## 1. Seed the DuckDB warehouse

```bash
git clone https://github.com/dbt-labs/jaffle_shop_duckdb.git
cd jaffle_shop_duckdb
pip install dbt-core dbt-duckdb
dbt build
ls jaffle_shop.duckdb
pwd
```

Remember that directory. The profile `url` is the **directory**, not the `.duckdb` file.

If you already have the file elsewhere (`find ~ -name jaffle_shop.duckdb`), use that directory.

## 2. Install Ontology Engine 0.13.4+

Tsinghua / tuna does not carry `ontology-cli`. Always use official PyPI.
0.13.3 is the identity-only wheel: no `--space`, no `generate-space`.

```bash
python -m pip install --upgrade --no-cache-dir \
  --index-url https://pypi.org/simple \
  "ontology-cli[memory,main]==0.13.4"
ontology --version
ontology skills list | grep generate-space
ontology dry-plan --help | grep -- --space
```

Must print `ontology-cli 0.13.4`. Do not `pip install wrenai`.

## 3. Skill stub (optional, for an agent)

```bash
npx skills add yanjin734-ltsm/ontology --agent pi -g
```

The CLI skills live in the wheel (`ontology skills get generate-space`).
The npx stub is only for the agent.

## 4. DuckDB profile (do not use `--ui` for this demo)

`--ui` is easy to save as a half-filled MySQL profile. Use a file.

```bash
# set URL to YOUR jaffle_shop_duckdb directory
cat > /tmp/jaffle-duckdb.yml << 'YML'
datasource: duckdb
url: /Users/YOU/jaffle_shop_duckdb
format: duckdb
YML

ontology profile add jaffle-duckdb --from-file /tmp/jaffle-duckdb.yml --activate
ontology profile debug
```

`profile debug` must show `datasource: duckdb` and the directory path.
If it shows `mysql` and only `ssl_mode`, delete that profile and add again.

Do not reuse a leftover profile named `jaffle-shop` unless you have confirmed it is duckdb.

## 5. Init a Space in a new directory

The dbt clone is the warehouse. The Space is a different directory.

```bash
mkdir -p ~/jaffle-ontology && cd ~/jaffle-ontology
ontology context init --empty
```

If `wren_project.yml` already exists, skip init. Do not run init from inside
`jaffle_shop_duckdb`.

```bash
ontology context set-profile jaffle-duckdb
```

You should see `data_source: … -> duckdb`. Then rebuild later.

Keep `catalog: wren` and `schema: public` in `wren_project.yml`. That is the
Space namespace. DuckDB physical tables stay `jaffle_shop.main.*`.

## 6. Fill the Space from our DuckDB example

```bash
cd /tmp
rm -rf ontology-ex
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/yanjin734-ltsm/ontology.git ontology-ex
cd ontology-ex && git sparse-checkout set examples/jaffle-duckdb

cd ~/jaffle-ontology
rsync -a /tmp/ontology-ex/examples/jaffle-duckdb/ ./
ontology context set-profile jaffle-duckdb
ontology context validate
ontology context build
```

Expect 2 models, 1 view. If build says MDL was built for postgres, build again
after `set-profile`.

Other databases: skip the rsync and run `ontology skills get generate-space`,
then have the agent introspect. Do not copy `examples/v5-jaffle`.

## 7. Query model names, not `wren.public…`

The rewriter adds CTEs and leaves your SQL as written. DuckDB treats `wren` as
a physical catalog, so `FROM wren.public.customers` fails with
`Catalog "wren" does not exist`.

```bash
cd ~/jaffle-ontology
ontology dry-plan --sql "SELECT first_name, last_name FROM customers LIMIT 5" \
  --datasource duckdb --space target/mdl.json
ontology --sql "SELECT first_name, last_name, number_of_orders FROM customers LIMIT 5"
```

dry-plan should mention `jaffle_shop` and `main`, not `"public".customers`.
Columns are `first_name` / `last_name` / `number_of_orders`, not `name`.

```bash
ontology --sql "SELECT first_name, last_name, order_id, amount FROM customer_orders LIMIT 5"
```

## Do not

- Point the tutorial at Canner/WrenAI. Use `yanjin734-ltsm/ontology`.
- `pip install` 0.13.3 or a Tsinghua index.
- `ontology profile add … --ui` unless you pick duckdb and the directory path.
- `context init` / `validate` / `build` / `--sql` inside the dbt clone.
- Copy `examples/v5-jaffle` onto this DuckDB file.
- Query `wren.public.customers` or column `name`.
- Bind a MySQL/Postgres profile to this Space.

## If you already have a broken `~/jaffle-ontology`

You do not need to start over. Fix the profile, replace models with
`examples/jaffle-duckdb`, `set-profile jaffle-duckdb`, `context build`, then
query `FROM customers`.
