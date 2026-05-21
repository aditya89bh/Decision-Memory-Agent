import json
import sys
from pathlib import Path
from uuid import uuid4

from .decision_agent import DecisionAgent
from .logging_utils import configure_logging, log_event
from .sqlite_store import SQLiteMemoryStore


class ScenarioError(ValueError):
    """Raised when a scenario file cannot be loaded or validated."""


def generate_trace_id():
    return uuid4().hex


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


def run_scenario(path, db_path="decision_memory.db", trace_id=None, logger=None):
    trace_id = trace_id or generate_trace_id()
    logger = logger or configure_logging()

    scenario = load_scenario(path)
    scenario_name = scenario.get("scenario", "unknown")
    log_event(logger, trace_id, "scenario_loaded", scenario=scenario_name, path=path)

    memory_store = SQLiteMemoryStore(db_path=db_path)
    agent = DecisionAgent(memory_store)

    log_event(logger, trace_id, "decision_started", scenario=scenario_name)
    record = agent.decide(
        context=scenario["context"],
        options=scenario["options"],
    )
    record.rationale["trace_id"] = trace_id

    log_event(logger, trace_id, "selected_option", selected_option=record.selected_option)
    log_event(logger, trace_id, "memory_record_persisted", db_path=db_path)
    log_event(logger, trace_id, "decision_completed", outcome=record.outcome)

    return record, trace_id


def print_record(record, trace_id):
    print("Trace ID:", trace_id)
    print("Context:", record.context)
    print("Selected option:", record.selected_option)
    print("Rationale:", record.rationale)
    print("Outcome:", record.outcome)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv

    if len(argv) != 1:
        print("Usage: python3 -m decision_memory.cli <scenario.json>", file=sys.stderr)
        return 2

    trace_id = generate_trace_id()
    logger = configure_logging()

    try:
        record, trace_id = run_scenario(argv[0], trace_id=trace_id, logger=logger)
    except ScenarioError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print_record(record, trace_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
