import json
import sys
from pathlib import Path

from .decision_agent import DecisionAgent
from .sqlite_store import SQLiteMemoryStore


class ScenarioError(ValueError):
    """Raised when a scenario file cannot be loaded or validated."""


def load_scenario(path):
    scenario_path = Path(path)
    if not scenario_path.exists():
        raise ScenarioError(f"Scenario file not found: {scenario_path}")

    try:
        with scenario_path.open("r", encoding="utf-8") as file:
            scenario = json.load(file)
    except json.JSONDecodeError as error:
        raise ScenarioError(f"Invalid JSON in scenario file: {error}") from error

    context = scenario.get("context")
    options = scenario.get("options")

    if not isinstance(context, dict):
        raise ScenarioError("Scenario must include a 'context' object.")
    if not isinstance(options, list) or not all(isinstance(option, str) for option in options):
        raise ScenarioError("Scenario must include an 'options' list of strings.")
    if not options:
        raise ScenarioError("Scenario must include at least one option.")

    return scenario


def run_scenario(path, db_path="decision_memory.db"):
    scenario = load_scenario(path)
    memory_store = SQLiteMemoryStore(db_path=db_path)
    agent = DecisionAgent(memory_store)

    record = agent.decide(
        context=scenario["context"],
        options=scenario["options"],
    )

    return record


def print_record(record):
    print("Context:", record.context)
    print("Selected option:", record.selected_option)
    print("Rationale:", record.rationale)
    print("Outcome:", record.outcome)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv

    if len(argv) != 1:
        print("Usage: python3 -m decision_memory.cli <scenario.json>", file=sys.stderr)
        return 2

    try:
        record = run_scenario(argv[0])
    except ScenarioError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print_record(record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
