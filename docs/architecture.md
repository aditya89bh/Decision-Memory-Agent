# Architecture

This repository implements a deterministic decision-memory loop.

The system has four parts:

1. A decision record that stores context, options, selected action, rationale, and outcome.
2. A memory store that keeps previous decisions.
3. A decision agent that scores current options using past outcomes.
4. An evaluator that checks whether memory changed future choices.

The goal is to make agent decisions inspectable and reusable across time.
