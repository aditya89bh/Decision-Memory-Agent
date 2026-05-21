import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from decision_memory import DecisionAgent, Evaluator, SQLiteMemoryStore  # noqa: E402

SCENARIOS_DIR = ROOT / "benchmarks" / "scenarios"
RESULTS_DIR = ROOT / "benchmarks" / "results"
LATEST_RESULTS_PATH = RESULTS_DIR / "latest_results.json"
BENCHMARK_DB_PATH = RESULTS_DIR / "benchmark_memory.db"


def load_scenario(path):
    with path.open("r", encoding="utf-8") as file:
        scenario = json.load(file)

    required_fields = ["scenario", "context", "options", "runs", "outcomes"]
    missing_fields = [field for field in required_fields if field not in scenario]
    if missing_fields:
        raise ValueError(f"{path} missing fields: {', '.join(missing_fields)}")

    return scenario


def load_scenarios(scenarios_dir=SCENARIOS_DIR):
    return [load_scenario(path) for path in sorted(scenarios_dir.glob("*.json"))]


def simulate_outcome(scenario, selected_option, selection_counts):
    outcomes = scenario.get("outcomes", {})
    option_outcomes = outcomes.get(selected_option, [])
    selected_count = selection_counts.get(selected_option, 0)

    if selected_count < len(option_outcomes):
        return option_outcomes[selected_count]

    return scenario.get("default_outcome", "failure")


def is_memory_influenced(record, evaluator):
    return evaluator.memory_influenced_decision(record)


def run_single_scenario(scenario, db_path):
    memory_store = SQLiteMemoryStore(db_path=str(db_path))
    agent = DecisionAgent(memory_store)
    evaluator = Evaluator()
    records = []
    selection_counts = {}

    for run_index in range(1, scenario["runs"] + 1):
        record = agent.decide(
            context=scenario["context"],
            options=scenario["options"],
        )
        outcome = simulate_outcome(scenario, record.selected_option, selection_counts)
        selection_counts[record.selected_option] = selection_counts.get(record.selected_option, 0) + 1
        agent.update_outcome(record, outcome)

        # Persist the outcome as a complete record. The original decision record
        # remains as the immutable decision event, while this captures feedback.
        memory_store.add(record)

        records.append(
            {
                "run": run_index,
                "selected_option": record.selected_option,
                "outcome": outcome,
                "memory_influenced": is_memory_influenced(record, evaluator),
                "rationale": record.rationale,
            }
        )

    return records


def compute_metrics(records):
    total_runs = len(records)
    if total_runs == 0:
        return {
            "total_runs": 0,
            "memory_influenced_decisions": 0,
            "decision_change_rate": 0.0,
            "success_rate": 0.0,
            "failure_rate": 0.0,
            "escalation_rate": 0.0,
            "improvement_after_failure": 0.0,
        }

    memory_influenced = sum(1 for record in records if record["memory_influenced"])
    decision_changes = sum(
        1
        for previous, current in zip(records, records[1:])
        if previous["selected_option"] != current["selected_option"]
    )
    successes = sum(1 for record in records if record["outcome"] == "success")
    failures = sum(1 for record in records if record["outcome"] == "failure")
    escalations = sum(1 for record in records if record["selected_option"] == "escalate_to_human")
    failure_recoveries = sum(
        1
        for previous, current in zip(records, records[1:])
        if previous["outcome"] == "failure" and current["outcome"] == "success"
    )
    failure_followups = sum(1 for previous in records[:-1] if previous["outcome"] == "failure")

    return {
        "total_runs": total_runs,
        "memory_influenced_decisions": memory_influenced,
        "decision_change_rate": round(decision_changes / max(total_runs - 1, 1), 4),
        "success_rate": round(successes / total_runs, 4),
        "failure_rate": round(failures / total_runs, 4),
        "escalation_rate": round(escalations / total_runs, 4),
        "improvement_after_failure": round(failure_recoveries / max(failure_followups, 1), 4),
    }


def aggregate_metrics(scenario_results):
    all_records = []
    for result in scenario_results:
        all_records.extend(result["records"])
    return compute_metrics(all_records)


def run_benchmarks(scenarios_dir=SCENARIOS_DIR, results_path=LATEST_RESULTS_PATH, db_path=BENCHMARK_DB_PATH):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    scenario_results = []
    for scenario in load_scenarios(scenarios_dir):
        records = run_single_scenario(scenario, db_path)
        scenario_results.append(
            {
                "scenario": scenario["scenario"],
                "description": scenario.get("description", ""),
                "metrics": compute_metrics(records),
                "records": records,
            }
        )

    results = {
        "scenarios": scenario_results,
        "aggregate_metrics": aggregate_metrics(scenario_results),
    }

    with results_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, sort_keys=True)
        file.write("\n")

    return results


def print_summary(results):
    headers = ["scenario", "runs", "mem", "change", "success", "failure", "escalation", "after_fail"]
    print(" | ".join(headers))
    print("-" * 86)

    for result in results["scenarios"]:
        metrics = result["metrics"]
        print(
            " | ".join(
                [
                    result["scenario"],
                    str(metrics["total_runs"]),
                    str(metrics["memory_influenced_decisions"]),
                    f"{metrics['decision_change_rate']:.2f}",
                    f"{metrics['success_rate']:.2f}",
                    f"{metrics['failure_rate']:.2f}",
                    f"{metrics['escalation_rate']:.2f}",
                    f"{metrics['improvement_after_failure']:.2f}",
                ]
            )
        )

    aggregate = results["aggregate_metrics"]
    print("-" * 86)
    print(
        " | ".join(
            [
                "ALL",
                str(aggregate["total_runs"]),
                str(aggregate["memory_influenced_decisions"]),
                f"{aggregate['decision_change_rate']:.2f}",
                f"{aggregate['success_rate']:.2f}",
                f"{aggregate['failure_rate']:.2f}",
                f"{aggregate['escalation_rate']:.2f}",
                f"{aggregate['improvement_after_failure']:.2f}",
            ]
        )
    )


def main():
    results = run_benchmarks()
    print_summary(results)
    print(f"\nSaved results to {LATEST_RESULTS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
