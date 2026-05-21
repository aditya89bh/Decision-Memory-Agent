import json

from decision_memory.cli import generate_trace_id, load_scenario, main, run_scenario
from decision_memory.sqlite_store import SQLiteMemoryStore


def write_scenario(path):
    path.write_text(
        json.dumps(
            {
                "context": {"risk_level": "high", "task": "factory_check"},
                "options": ["continue_current_task", "pause_and_inspect"],
            }
        ),
        encoding="utf-8",
    )


def test_load_scenario_accepts_valid_json(tmp_path):
    scenario_path = tmp_path / "scenario.json"
    write_scenario(scenario_path)

    scenario = load_scenario(scenario_path)

    assert scenario["context"]["risk_level"] == "high"
    assert scenario["options"] == ["continue_current_task", "pause_and_inspect"]


def test_run_scenario_persists_decision_to_sqlite(tmp_path):
    scenario_path = tmp_path / "scenario.json"
    db_path = tmp_path / "decision_memory.db"
    write_scenario(scenario_path)

    record, trace_id = run_scenario(scenario_path, db_path=str(db_path))
    persisted_records = SQLiteMemoryStore(db_path=str(db_path)).all()

    assert trace_id
    assert record.selected_option == "pause_and_inspect"
    assert len(persisted_records) == 1
    assert persisted_records[0].context == record.context
    assert persisted_records[0].selected_option == record.selected_option


def test_main_prints_readable_output(tmp_path, capsys, monkeypatch):
    scenario_path = tmp_path / "scenario.json"
    db_path = tmp_path / "decision_memory.db"
    write_scenario(scenario_path)
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(scenario_path)])
    output = capsys.readouterr()

    assert exit_code == 0
    assert "Trace ID:" in output.out
    assert "Context:" in output.out
    assert "Selected option: pause_and_inspect" in output.out
    assert "Rationale:" in output.out
    assert "Outcome: None" in output.out
    assert "trace_id" in output.out
    assert db_path.exists()


def test_generate_trace_id_returns_unique_values():
    first_trace_id = generate_trace_id()
    second_trace_id = generate_trace_id()

    assert first_trace_id
    assert second_trace_id
    assert first_trace_id != second_trace_id


def test_main_logs_trace_events(tmp_path, capsys, monkeypatch):
    scenario_path = tmp_path / "scenario.json"
    write_scenario(scenario_path)
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(scenario_path)])
    output = capsys.readouterr()

    assert exit_code == 0
    assert "trace_id=" in output.err
    assert "event=scenario_loaded" in output.err
    assert "event=decision_started" in output.err
    assert "event=selected_option" in output.err
    assert "event=memory_record_persisted" in output.err
    assert "event=decision_completed" in output.err


def test_main_reports_missing_file(capsys):
    exit_code = main(["missing.json"])
    output = capsys.readouterr()

    assert exit_code == 1
    assert "Error: Scenario file not found" in output.err


def test_main_reports_invalid_scenario(tmp_path, capsys):
    scenario_path = tmp_path / "invalid.json"
    scenario_path.write_text(json.dumps({"context": {}, "options": "inspect"}), encoding="utf-8")

    exit_code = main([str(scenario_path)])
    output = capsys.readouterr()

    assert exit_code == 1
    assert "options" in output.err
