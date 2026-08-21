# Ontology Engine v0 identity execution log

Date: 2026-08-21 (Asia/Shanghai)

## Who did the work

Codex (gpt-5.6-sol, high reasoning) **started twice but did not edit any product files**.

- Session 1: missing `/home/box/.local/bin/codex-code-mode-host` — tools fail closed.
- Session 2: `--disable code_mode --disable code_mode_host` — still `code-mode host is disabled`.

**Fallback: the executor subagent implemented v0 identity isolation** using the same section 9 rules.

## Scope

v0 identity only on branch `ontology/identity-v0`. No push. No v0.1 jaffle SQL. No v0.2 public repo. No PyPI. No Cursor skill. No Aos desktop. No Canner/WrenAI push URL restore. No Rosella GitHub.

Plan section 9 was appended to `ONTOLOGY-ENGINE-FORK-PLAN.md` and copied to `/workspace/ONTOLOGY-ENGINE-FORK-PLAN.md`.

## Acceptance (9.4)

| Check | Result |
| --- | --- |
| `pip install -e ./core/wren` then `.venv/bin/ontology --help` | PASS — Usage: ontology; help = Ontology Engine CLI |
| no package-provided `wren` console script | PASS after uninstalling leftover `wrenai` (same venv must not keep official package) |
| `ONTOLOGY_HOME=/tmp/ontology-smoke ontology profile list` | PASS — did not create `~/.wren` or `/tmp/ontology-smoke/.wren` |
| `--version` | PASS — `ontology-cli 0.13.3` |
| skills list has 6 guides | PASS — onboarding, usage, generate-mdl, enrich-context, dlt-connector, genbi |
| `skills get usage` has no product-name Wren | PASS (`rg -i \bwren\b` empty) |
| pyproject extras do not mention `wrenai[` | PASS |
| `pytest tests/unit` | 1226 passed, 60 skipped, 4 failed (all `TestLocalFirstEmbeddings`, missing `sentence_transformers` / memory extra — not identity) |

Old `.venv/bin/wren` disappeared after `pip uninstall wrenai`. Editable `ontology-cli` is the only CLI package.

## Remaining Wren-facing leaks (intentional or deferred)

- Python import remains `import wren`; hatch `packages = ["src/wren"]`
- Engine wheel `wren-core-py`; GenBI CDN `@wrenai/wren-core-wasm` (deferred)
- Project file `wren_project.yml`; MDL `catalog: wren`; OSI vendor `WREN`; HTTP header `x-wren-db-statement_timeout`
- Skills reference filename `wren-sql`
- `docs/**` not rewritten (CC BY; v0 hard skip)
- SDK extras still mention upstream `wrenai[...]` (deferred)
- Internal class names `WrenEngine` / `WrenError` / `WrenConfig`

## Git

- Branch: `ontology/identity-v0`
- Local commit allowed; **no push**
- origin fetch: `https://github.com/Canner/WrenAI.git`
- origin push: `DISABLED-DO-NOT-PUSH-CANNER` (unchanged)

## Codex sessions

- 01a0234d-4b90-7ea1-9620-2e68fd946b71 (code-mode-host missing)
- 01a0234d-f1df-7801-a419-68199a388da8 (code_mode disabled, still fail closed)
