# Decision-Memory-Agent

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

## Repository structure

```text
Decision-Memory-Agent/
├── README.md
├── requirements.txt
├── run_demo.py
├── docs/
│   ├── architecture.md
│   ├── decision_memory_loop.md
│   └── roadmap.md
├── examples/
│   └── factory_decision_scenario.json
├── src/
│   └── decision_memory/
│       ├── __init__.py
│       ├── decision_record.py
│       ├── memory_store.py
│       ├── decision_agent.py
│       └── evaluator.py
└── tests/
    └── test_decision_memory.py
```

## Demo scenario

The demo uses a factory robot scheduling situation.

The agent must choose between possible actions such as:

- continue current task
- pause and inspect
- switch to a safer task
- escalate to a human operator

The first decision is made with limited memory.

After the outcome is recorded, the second decision uses memory to avoid repeating a poor choice.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run demo

```bash
python run_demo.py
```

## Run tests

```bash
python -m pytest tests
```

## Current status

```text
Foundation scaffold in progress
```

Planned completion target for portfolio-grade version:

1. Deterministic source modules
2. Runnable demo
3. Unit tests
4. Captured demo output
5. Architecture docs
6. README with clear thesis and usage
7. CI workflow
8. Example decision-memory scenario

## Related directions

This repo connects to:

- memory agents
- planning agents
- reflection agents
- robotics decision systems
- agent evaluation
- inspectable AI behavior
- memory-aware product design
