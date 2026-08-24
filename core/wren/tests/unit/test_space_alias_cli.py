"""Compatibility tests for the --space manifest-input alias."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import typer
from typer.testing import CliRunner

import wren.cli as cli
from wren.cli import app

pytestmark = pytest.mark.unit

runner = CliRunner()


class _Table:
    def to_pandas(self):
        raise RuntimeError

    def to_pydict(self):
        return {"value": [1]}


def _engine() -> MagicMock:
    engine = MagicMock()
    engine.__enter__.return_value = engine
    engine.__exit__.return_value = False
    engine.query.return_value = _Table()
    return engine


@pytest.mark.parametrize(
    ("prefix", "expected_call"),
    [
        (["--sql", "SELECT 1", "--quiet", "--output", "json"], "query"),
        (["query", "--sql", "SELECT 1", "--quiet", "--output", "json"], "query"),
        (["dry-run", "--sql", "SELECT 1"], "dry_run"),
    ],
)
def test_main_commands_mdl_and_space_are_equivalent(
    monkeypatch, prefix, expected_call
):
    seen: list[str | None] = []
    engines: list[MagicMock] = []

    def build_engine(mdl, *_args, **_kwargs):
        seen.append(mdl)
        engine = _engine()
        engines.append(engine)
        return engine

    monkeypatch.setattr(cli, "_build_engine", build_engine)

    outputs = []
    for flag in ("--mdl", "--space"):
        result = runner.invoke(app, [*prefix, flag, "same-input"])
        assert result.exit_code == 0, result.output
        outputs.append(result.output)

    assert seen == ["same-input", "same-input"]
    assert outputs[0] == outputs[1]
    assert all(getattr(engine, expected_call).called for engine in engines)


def test_dry_plan_mdl_and_space_resolve_to_same_input(monkeypatch):
    seen: list[str | None] = []

    def stop_after_resolution(value):
        seen.append(value)
        raise typer.Exit()

    monkeypatch.setattr(cli, "_require_mdl", stop_after_resolution)
    for flag in ("--mdl", "--space"):
        result = runner.invoke(
            app, ["dry-plan", "--sql", "SELECT 1", flag, "same-input"]
        )
        assert result.exit_code == 0, result.output

    assert seen == ["same-input", "same-input"]


@pytest.mark.parametrize(
    "args",
    [
        ["--sql", "SELECT 1"],
        ["query", "--sql", "SELECT 1"],
        ["dry-plan", "--sql", "SELECT 1"],
        ["dry-run", "--sql", "SELECT 1"],
    ],
)
def test_main_commands_reject_mdl_with_space(args):
    result = runner.invoke(app, [*args, "--mdl", "one", "--space", "two"])
    assert result.exit_code == 1
    assert "--mdl and --space are mutually exclusive" in result.output


def test_main_help_recommends_space_and_marks_mdl_supported():
    result = runner.invoke(app, ["query", "--help"])
    assert result.exit_code == 0
    assert "--space" in result.output
    assert "Deprecated but supported" in result.output


@pytest.mark.parametrize(
    "args",
    [
        ["--sql", "SELECT 1"],
        ["query", "--sql", "SELECT 1"],
        ["context", "validate"],
        ["context", "build"],
    ],
)
def test_missing_project_explains_data_repo_vs_space(monkeypatch, tmp_path, args):
    import wren.context as context

    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("ONTOLOGY_PROJECT_HOME", raising=False)
    monkeypatch.setattr(context, "load_global_config", lambda: {})

    result = runner.invoke(app, args)

    assert result.exit_code == 1
    assert "data warehouse/dbt directory" in result.output
    assert "ontology context init" in result.output
    assert "`cd` to a directory containing wren_project.yml" in result.output


def _write_manifest(tmp_path: Path) -> Path:
    path = tmp_path / "manifest.json"
    path.write_text(
        json.dumps(
            {
                "catalog": "wren",
                "schema": "public",
                "models": [],
                "cubes": [
                    {
                        "name": "sales",
                        "baseObject": "orders",
                        "measures": [],
                        "dimensions": [],
                    }
                ],
            }
        )
    )
    return path


@pytest.mark.parametrize(
    "command",
    [
        ["cube", "list"],
        ["cube", "describe", "sales"],
    ],
)
def test_cube_mdl_and_space_have_equivalent_raw_json_output(tmp_path, command):
    manifest = _write_manifest(tmp_path)
    results = [
        runner.invoke(app, [*command, flag, str(manifest)])
        for flag in ("--mdl", "--space")
    ]
    assert [result.exit_code for result in results] == [0, 0]
    assert results[0].output == results[1].output


def test_cube_query_mdl_and_space_pass_equivalent_raw_json(monkeypatch, tmp_path):
    import wren_core

    manifest = _write_manifest(tmp_path)
    seen: list[str] = []

    def cube_query_to_sql(_query, mdl_json):
        seen.append(mdl_json)
        return "SELECT 1"

    monkeypatch.setattr(wren_core, "cube_query_to_sql", cube_query_to_sql)
    outputs = []
    for flag in ("--mdl", "--space"):
        result = runner.invoke(
            app,
            [
                "cube",
                "query",
                "--cube",
                "sales",
                "--measures",
                "revenue",
                "--sql-only",
                flag,
                str(manifest),
            ],
        )
        assert result.exit_code == 0, result.output
        outputs.append(result.output)

    assert seen[0] == seen[1] == manifest.read_text()
    assert outputs == ["SELECT 1\n", "SELECT 1\n"]


@pytest.mark.parametrize(
    "command",
    [
        ["cube", "list"],
        ["cube", "describe", "sales"],
        ["cube", "query", "--cube", "sales", "--measures", "revenue"],
    ],
)
def test_cube_commands_reject_mdl_with_space(command):
    result = runner.invoke(app, [*command, "--mdl", "one", "--space", "two"])
    assert result.exit_code == 1
    assert "--mdl and --space are mutually exclusive" in result.output


def test_memory_describe_mdl_and_space_have_equivalent_raw_json_output(tmp_path):
    manifest = _write_manifest(tmp_path)
    results = [
        runner.invoke(app, ["memory", "describe", flag, str(manifest)])
        for flag in ("--mdl", "--space")
    ]
    assert [result.exit_code for result in results] == [0, 0]
    assert results[0].output == results[1].output


def test_memory_index_mdl_and_space_pass_equivalent_raw_json(monkeypatch, tmp_path):
    import wren.memory.cli as memory_cli
    import wren.memory.index_backend as index_backend

    manifest = _write_manifest(tmp_path)
    seen: list[dict] = []
    store = MagicMock()
    store.index_schema.side_effect = lambda value, **_kwargs: (
        seen.append(value) or {"schema_items": 0, "seed_queries": 0}
    )
    monkeypatch.setattr(index_backend, "resolve_backend", lambda: "lancedb")
    monkeypatch.setattr(memory_cli, "_get_store", lambda _path: store)

    outputs = []
    for flag in ("--mdl", "--space"):
        result = runner.invoke(
            app,
            [
                "memory",
                "index",
                flag,
                str(manifest),
                "--no-queries",
            ],
        )
        assert result.exit_code == 0, result.output
        outputs.append(result.output)

    assert seen[0] == seen[1] == json.loads(manifest.read_text())
    assert outputs[0] == outputs[1]


@pytest.mark.parametrize(
    "command",
    [
        ["memory", "index"],
        ["memory", "describe"],
        ["memory", "fetch", "--query", "orders"],
        ["memory", "watch"],
    ],
)
def test_memory_commands_reject_mdl_with_space(command):
    result = runner.invoke(app, [*command, "--mdl", "one", "--space", "two"])
    assert result.exit_code == 1
    assert "--mdl and --space are mutually exclusive" in result.output
