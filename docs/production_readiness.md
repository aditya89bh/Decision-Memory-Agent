# Production Readiness Plan

This repository is currently a portfolio-grade deterministic prototype.

The next goal is to evolve it into a production-oriented decision-memory system.

## Current state

Implemented:

- deterministic decision records
- in-memory memory store
- memory-aware option scoring
- outcome updates
- evaluator summary
- runnable demo
- unit tests
- CI workflow
- package-style source layout

## Not production-ready yet

Missing production concerns:

- persistent storage
- typed data validation
- configurable scoring policies
- structured logging
- explicit error handling
- CLI or API interface
- migration strategy for memory records
- richer test coverage
- benchmark scenarios
- deployment documentation

## Productionization phases

### Phase 1: Typed models

Replace loose Python objects with typed models.

Target:

- `DecisionRecord` as a validated model
- explicit outcome enum
- typed context and rationale fields
- serialization and deserialization tests

### Phase 2: Persistent memory

Replace in-memory-only storage with durable persistence.

Target:

- SQLite-backed memory store
- save decision records
- load historical records
- query records by context fields
- update outcomes after decision execution

### Phase 3: Configurable policy layer

Separate scoring policy from the agent.

Target:

- base score config
- memory adjustment config
- failure penalty config
- success reward config
- policy tests

### Phase 4: Observability

Add production-style visibility.

Target:

- structured logs
- decision trace IDs
- memory lookup logs
- evaluation summaries
- failure diagnostics

### Phase 5: Interface layer

Expose the system for practical use.

Target:

- CLI entrypoint
- JSON scenario input
- JSON decision output
- optional lightweight API later

### Phase 6: Evaluation depth

Move beyond toy tests.

Target:

- multiple scenarios
- repeated decision loops
- benchmark fixtures
- regression tests
- memory influence metrics

## Near-term laptop checklist

When running locally:

```bash
git pull
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python run_demo.py
PYTHONPATH=src pytest
```

Then replace `results/demo_output.txt` with real captured output.

## Target production-readiness milestones

| Milestone | Expected production readiness |
|---|---:|
| Current prototype | 25% |
| Typed models + pyproject | 35% |
| SQLite persistence | 50% |
| CLI + logging + richer tests | 65% |
| policy layer + benchmarks | 75% |
| API + deployment docs | 85% |
