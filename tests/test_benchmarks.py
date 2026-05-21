import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from benchmarks.run_benchmarks import compute_metrics, load_scenarios, run_benchmarks


def test_load_scenarios_finds_benchmark_cases():
    scenarios = load_scenarios()
    names = {scenario["scenario"] for scenario in scenarios}

    assert len(scenarios) >= 5
    assert "repeated_failure" in names
    assert "repeated_success" in names
    assert "unsafe_high_risk" in names
    assert "confidence_recovery" in names
    assert "escalation_heavy" in names


def test_compute_metrics_reports_memory_and_outcomes():
    records = [
        {"selected_option": "escalate_to_human", "outcome": "failure", "memory_influenced": False},
        {"selected_option": "pause_and_inspect", "outcome": "success", "memory_influenced": True},
        {"selected_option": "pause_and_inspect", "outcome": "success", "memory_influenced": True},
    ]

    metrics = compute_metrics(records)

    assert metrics["total_runs"] == 3
    assert metrics["memory_influenced_decisions"] == 2
    assert metrics["decision_change_rate"] == 0.5
    assert metrics["success_rate"] == 0.6667
    assert metrics["failure_rate"] == 0.3333
    assert metrics["escalation_rate"] == 0.3333
    assert metrics["improvement_after_failure"] == 1.0


def test_run_benchmarks_writes_results(tmp_path):
    results_path = tmp_path / "latest_results.json"
    db_path = tmp_path / "benchmark_memory.db"

    results = run_benchmarks(results_path=results_path, db_path=db_path)

    assert results_path.exists()
    assert db_path.exists()
    assert results["aggregate_metrics"]["total_runs"] > 0
    assert results["aggregate_metrics"]["memory_influenced_decisions"] > 0

    persisted = json.loads(results_path.read_text(encoding="utf-8"))
    assert persisted["aggregate_metrics"] == results["aggregate_metrics"]
    assert len(persisted["scenarios"]) >= 5
