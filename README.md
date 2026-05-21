# Decision-Memory-Agent

[![tests](https://github.com/aditya89bh/Decision-Memory-Agent/actions/workflows/tests.yml/badge.svg)](https://github.com/aditya89bh/Decision-Memory-Agent/actions/workflows/tests.yml)

**A production-oriented decision-memory system for agents that need to remember what they decided, why they decided it, what happened next, and how that history should change future behavior.**

Most agent systems can produce actions. Fewer can explain how past decisions changed later choices. This repository implements a deterministic, inspectable memory loop for outcome-aware decision making.

```text
Context -> Options -> Decision -> Rationale -> Memory -> Outcome -> Future Decision Bias
```

## What is implemented

| Capability | Status |
|---|---:|
| Typed decision records with Pydantic validation | Implemented |
| SQLite-backed persistent memory store | Implemented |
| Installable CLI command | Implemented |
| Structured logs with trace IDs | Implemented |
| Benchmark and evaluation harness | Implemented |
| Scenario-driven JSON execution | Implemented |
| Unit and integration tests | 21 passing |
| Production readiness roadmap | Documented |

## Quick start

```bash
git clone https://github.com/aditya89bh/Decision-Memory-Agent.git
cd Decision-Memory-Agent
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Run a scenario:

```bash
decision-memory examples/factory_decision_scenario.json
```

Run tests:

```bash
pytest
```

Run benchmarks:

```bash
python3 benchmarks/run_benchmarks.py
```

## CLI example

```text
Trace ID: <trace-id>
Context: {'task': 'cnc_machine_loading', 'risk_level': 'high', 'robot_confidence': 'low'}
Selected option: escalate_to_human
Rationale: {'selected_option': 'escalate_to_human', 'selected_score': 3, ...}
Outcome: None
```

Each CLI run persists the decision to SQLite and emits structured trace logs.

## Benchmark snapshot

Latest benchmark run across repeated decision-memory scenarios:

| Metric | Value |
|---|---:|
| Total runs | 23 |
| Memory-influenced decisions | 18 |
| Success rate | 0.91 |
| Failure rate | 0.09 |
| Escalation rate | 0.70 |
| Improvement after failure | 1.00 |

The benchmark harness tests repeated failures, repeated successes, unsafe high-risk contexts, confidence recovery, and escalation-heavy scenarios.

## Why this matters

Agents that do not remember consequences tend to repeat mistakes.

A decision-memory system makes the decision trail explicit:

- the situation that produced the decision
- the options the agent considered
- the selected action
- the rationale for that action
- the outcome that followed
- the way that outcome influenced future scoring

This makes agent behavior easier to debug, evaluate, and improve. It also creates a bridge between planning agents, reflection agents, memory systems, and embodied robotics agents where decisions have operational consequences.

## Architecture

```text
JSON Scenario
    |
    v
DecisionAgent
    |
    v
Option Scoring + Memory Adjustment
    |
    v
DecisionRecord
    |
    v
SQLiteMemoryStore
    |
    v
Outcome + Evaluation Metrics
    |
    v
Future Decision Bias
```

| Component | Role |
|---|---|
| `DecisionRecord` | Pydantic model for context, options, selected option, rationale, and outcome |
| `MemoryStore` | In-memory store for deterministic prototype flows |
| `SQLiteMemoryStore` | Durable memory store backed by SQLite |
| `DecisionAgent` | Scores options using current context and prior memory |
| `Evaluator` | Measures decision changes, memory influence, and outcome improvement |
| `decision-memory` | Installable CLI for running JSON scenarios |
| `benchmarks/` | Repeatable evaluation suite for memory-influenced decisions |

## Memory loop diagram

```text
[Current Context]
        |
        v
[Candidate Options]
        |
        v
[Score Options]
        |
        v
[Retrieve Similar Memories]
        |
        v
[Apply Success/Failure Adjustments]
        |
        v
[Select Decision]
        |
        v
[Persist Decision Record]
        |
        v
[Attach Outcome]
        |
        v
[Influence Future Decisions]
```

## Demo and media

Planned visual assets:

| Asset | Status |
|---|---:|
| Terminal GIF demo | Planned |
| Benchmark screenshot | Planned |
| Architecture diagram | Markdown version included |
| Memory loop diagram | Markdown version included |

## Repository structure

```text
Decision-Memory-Agent/
├── src/decision_memory/
│   ├── decision_agent.py
│   ├── decision_record.py
│   ├── evaluator.py
│   ├── logging_utils.py
│   ├── memory_store.py
│   ├── sqlite_store.py
│   └── cli.py
├── tests/
├── examples/
├── benchmarks/
│   ├── scenarios/
│   ├── results/
│   └── run_benchmarks.py
├── docs/
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Production roadmap

Implemented production-oriented layers:

1. Package structure under `src/`
2. Pydantic typed records
3. SQLite persistence
4. Installable CLI
5. Structured trace logging
6. Benchmark harness
7. CI and test suite

Next production layers:

1. richer memory retrieval beyond exact context-key matching
2. configurable scoring policies
3. schema migration support for persistent records
4. richer benchmark reporting
5. optional API layer
6. Dockerized execution environment

## Related directions

This repo connects to:

- memory agents
- planning agents
- reflection agents
- robotics decision systems
- agent evaluation
- inspectable AI behavior
- memory-aware product design
