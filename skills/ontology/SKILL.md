---
name: ontology
description: "Ontology Engine CLI for AI agents — a semantic SQL layer over 22+ databases (Postgres, MySQL, BigQuery, Snowflake, Spark, …). The actual workflow guides live inside the `ontology` CLI itself; this is just a discovery stub. Use whenever the user asks a data question (how many, show me, top N, compare, trend, breakdown, metric, revenue, customers, orders), wants to install / set up Ontology Engine, connect a new database, connect SaaS data via dlt (HubSpot, Stripe, Salesforce, GitHub, Slack), generate or regenerate an Ontology Space / MDL project from a database schema, enrich a Space with business context (enum meanings, units, cubes like ARR / DAU / churn), or turn a project's context layer into a shareable GenBI web app / dashboard and deploy it to Vercel or Cloudflare. Triggers: 'ontology space', 'generate ontology space', 'install wren', 'set up wren engine', 'connect database to wren', 'connect SaaS to wren', 'load hubspot / stripe / salesforce data', 'generate mdl', 'scaffold wren project', 'enrich wren context', 'augment my project', 'add cubes', 'build a dashboard', 'make a shareable analytics app', 'deploy my context layer as a web app', 'genbi app', 'wren onboarding', 'wren usage', 'wren generate mdl', 'wren dlt connector', 'wren enrich context', 'wren genbi'."
license: Apache-2.0
allowed-tools: Bash(ontology:*)
---

# Ontology Engine CLI

This is a discovery stub. The actual workflow guides and prompt helpers
live inside the `ontology` CLI itself, so they always match the installed
wrenai version (no skill cache, no version drift).

The project is an **Ontology Space**: structural YAML plus the separate
`knowledge/` plane. Its structural Manifest continues to use the MDL
compatibility format, `wren_project.yml`, and `target/mdl.json`.

Install: `pip install ontology-cli`.

## Workflow guides

```bash
ontology skills list                        # all available workflow guides
ontology skills get onboarding              # set up Ontology Engine end-to-end
ontology skills get usage                   # day-to-day querying
ontology skills get generate-space          # recommended: generate an Ontology Space
ontology skills get generate-mdl            # legacy name, same guide (still supported)
ontology skills get dlt-connector           # connect SaaS sources via dlt
ontology skills get enrich-context          # add business context (units, enums, cubes)
ontology skills get genbi                   # build & deploy a shareable GenBI web app
# add --full to include the skill's reference docs
# add --script <name> to fetch a bundled script (e.g. dlt-connector / introspect_dlt)
```

## Reference docs

Full reference docs live on the web: <https://github.com/Canner/WrenAI/tree/main/docs/core>

```bash
ontology docs connection-info <ds>          # required + optional connection fields for a data source
```

## Prompt enhancement (wraps a user question for an agent)

```bash
ontology ask "<question>" --guided          # for weaker LLMs (strict task flow)
ontology ask "<question>" --direct          # for stronger LLMs (minimal wrapping)
```

## Day-to-day data commands (not a sub-app — top-level)

```bash
ontology --sql '...'                        # execute SQL through the Space manifest
ontology query --sql '...'                  # same, explicit
ontology dry-plan --sql '...'               # transpile only, no DB hit
ontology context show / build / validate    # Ontology Space / Manifest lifecycle
ontology profile add / list / switch        # named connection profiles
ontology memory index / recall / store      # semantic memory (needs `[memory]` extra)
```

Run `ontology --help` for the full surface; load the matching `ontology skills get
<name>` guide before driving any multi-step workflow.
