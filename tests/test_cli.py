import json

from decision_memory.cli import load_scenario, main, run_scenario
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

    record = run_scenario(scenario_path, db_path=str(db_path))
    persisted_records = SQLiteMemoryStore(db_path=str(db_path)).all()

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
    assert "Context:" in output.out
    assert "Selected option: pause_and_inspect" in output.out
    assert "Rationale:" in output.out
    assert "Outcome: None" in output.out
    assert db_path.exists()


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
