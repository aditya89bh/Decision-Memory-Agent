# Benchmarking

The benchmark harness measures whether deterministic decision memory changes future behavior after repeated feedback.

## Run benchmarks

```bash
python3 benchmarks/run_benchmarks.py
```

The runner loads JSON scenarios from:

```text
benchmarks/scenarios/
```

It writes the latest metrics to:

```text
benchmarks/results/latest_results.json
```

A temporary SQLite database is created at `benchmarks/results/benchmark_memory.db` for reproducible benchmark runs.

## Scenario design

Each scenario defines:

- `scenario`: stable scenario name
- `description`: human-readable purpose
- `runs`: number of repeated decisions
- `context`: decision context passed to `DecisionAgent`
- `options`: candidate options
- `outcomes`: deterministic simulated feedback by selected option
- `default_outcome`: fallback outcome if an option has no more explicit outcomes

The benchmark intentionally uses deterministic feedback. There is no ML or random sampling.

## Metrics

- `total_runs`: number of decision executions
- `memory_influenced_decisions`: decisions whose option scores differ from base scoring due to memory
- `decision_change_rate`: how often the selected option changed between consecutive runs
- `success_rate`: share of runs with `success` outcome
- `failure_rate`: share of runs with `failure` outcome
- `escalation_rate`: share of runs selecting `escalate_to_human`
- `improvement_after_failure`: share of failed runs followed by a successful run

## Architecture

The benchmark reuses the production primitives:

```text
JSON scenario → DecisionAgent → SQLiteMemoryStore → simulated outcome → metrics
```

The benchmark does not rewrite the agent. It exercises the existing deterministic decision loop repeatedly and records whether persisted outcomes influence later decisions.
