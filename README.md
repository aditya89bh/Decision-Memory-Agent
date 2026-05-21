# Decision-Memory-Agent

[![tests](https://github.com/aditya89bh/Decision-Memory-Agent/actions/workflows/tests.yml/badge.svg)](https://github.com/aditya89bh/Decision-Memory-Agent/actions/workflows/tests.yml)

A deterministic agent system that records decisions, rationale, outcomes, and uses memory to improve future choices.

## Core thesis

Agents should not only make decisions.

They should remember:

- what decision was made
- why it was made
- what context shaped it
- what outcome followed
- whether the choice was successful
- how future decisions should change because of it

This repository explores **decision memory** as a core primitive for more reliable agents.

## What this repository demonstrates

This repo implements a small deterministic decision-memory loop:

```text
Decision Context → Candidate Options → Decision → Rationale → Memory Record → Outcome → Future Decision Bias
```

Instead of treating each decision as isolated, the agent stores past decision records and uses them to score future options.

## Why this matters

Most agents make choices without remembering the long-term consequences of earlier choices.

That creates predictable failure modes:

- repeated bad decisions
- no memory of rationale
- no learning from outcomes
- no inspectable decision trail
- no way to debug why an agent changed behavior
- no continuity between decisions across time

Decision memory gives agents a way to connect action, consequence, and future judgment.

## Architecture

```text
Scenario Input
    ↓
Decision Agent
    ↓
Option Scoring
    ↓
Decision Record
    ↓
Memory Store
    ↓
Outcome Update
    ↓
Future Decision Influence
```

| Component | Role |
|---|---|
| `DecisionRecord` | Stores one decision, rationale, context, selected option, and outcome |
| `MemoryStore` | Keeps decision records and retrieves relevant past decisions |
| `DecisionAgent` | Scores options using current context and past memory |
| `Evaluator` | Measures decision quality and memory influence |
| `run_demo.py` | Runs a deterministic factory decision-memory scenario |

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
PYTHONPATH=src python3 run_demo.py
```

## Run a scenario from JSON

```bash
PYTHONPATH=src python3 -m decision_memory.cli examples/factory_decision_scenario.json
```

The CLI loads the scenario, runs a deterministic decision, prints the context, selected option, rationale, and outcome, and persists the decision to `decision_memory.db` using `SQLiteMemoryStore`.

## Run tests

```bash
PYTHONPATH=src pytest
```

## Demo output

A sample output is included in:

```text
demo_output.txt
```

The demo shows a two-step memory loop where a failed prior decision changes the next decision under a similar high-risk context.

## Repository structure

```text
Decision-Memory-Agent/
├── README.md
├── ROADMAP.md
├── requirements.txt
├── run_demo.py
├── decision_record.py
├── memory_store.py
├── decision_agent.py
├── evaluator.py
├── test_decision_memory.py
├── factory_decision_scenario.json
├── demo_output.txt
├── docs/
│   └── architecture.md
└── .github/
    └── workflows/
        └── tests.yml
```

## Current status

```text
Runnable deterministic prototype with tests and CI
```

Implemented:

1. Decision record primitive
2. Memory store
3. Memory-aware decision scoring
4. Outcome update loop
5. Evaluator
6. Runnable demo
7. Unit tests
8. Sample scenario
9. Sample output
10. GitHub Actions CI

## Next improvements

1. Move source files into a proper package structure.
2. Add richer scenario examples.
3. Capture real local output after laptop run.
4. Add a visual decision-memory diagram.
5. Add robotics-oriented examples with task risk, operator availability, and confidence thresholds.

## Related directions

This repo connects to:

- memory agents
- planning agents
- reflection agents
- robotics decision systems
- agent evaluation
- inspectable AI behavior
- memory-aware product design
