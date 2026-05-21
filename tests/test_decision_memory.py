import pytest
from pydantic import ValidationError

from decision_memory import DecisionAgent, DecisionRecord, Evaluator, MemoryStore


def test_decision_record_serializes_to_dict():
    record = DecisionRecord(
        context={'risk_level': 'high'},
        options=['continue_current_task', 'pause_and_inspect'],
        selected_option='pause_and_inspect',
        rationale={'reason': 'Safer under high risk'},
        outcome='success',
    )

    data = record.to_dict()

    assert data['context']['risk_level'] == 'high'
    assert data['selected_option'] == 'pause_and_inspect'
    assert data['outcome'] == 'success'


def test_decision_record_creates_valid_typed_model():
    record = DecisionRecord(
        context={'risk_level': 'high'},
        options=['continue_current_task', 'pause_and_inspect'],
        selected_option='pause_and_inspect',
        rationale={'reason': 'Safer under high risk'},
    )

    assert record.context == {'risk_level': 'high'}
    assert record.options == ['continue_current_task', 'pause_and_inspect']
    assert record.selected_option == 'pause_and_inspect'
    assert record.rationale == {'reason': 'Safer under high risk'}
    assert record.outcome is None


def test_decision_record_rejects_invalid_data():
    with pytest.raises(ValidationError):
        DecisionRecord(
            context=['not', 'a', 'dict'],
            options=['continue_current_task'],
            selected_option='continue_current_task',
            rationale={},
        )

    with pytest.raises(ValidationError):
        DecisionRecord(
            context={'risk_level': 'high'},
            options='continue_current_task',
            selected_option='continue_current_task',
            rationale={},
        )


def test_decision_record_json_serialization_is_compatible():
    record = DecisionRecord(
        context={'risk_level': 'high'},
        options=['continue_current_task', 'pause_and_inspect'],
        selected_option='pause_and_inspect',
        rationale={'scored_options': [('pause_and_inspect', 2)]},
        outcome='success',
    )

    assert record.to_dict()['rationale']['scored_options'] == [('pause_and_inspect', 2)]
    assert record.to_json_dict()['rationale']['scored_options'] == [['pause_and_inspect', 2]]


def test_memory_store_retrieves_by_context_key():
    memory_store = MemoryStore()
    record = DecisionRecord(
        context={'risk_level': 'high'},
        options=['continue_current_task'],
        selected_option='continue_current_task',
        rationale={},
        outcome='failure',
    )

    memory_store.add(record)

    matches = memory_store.find_by_context_key('risk_level', 'high')

    assert len(matches) == 1
    assert matches[0].selected_option == 'continue_current_task'


def test_agent_records_decision_in_memory():
    memory_store = MemoryStore()
    agent = DecisionAgent(memory_store)

    record = agent.decide(
        context={'risk_level': 'high'},
        options=['continue_current_task', 'escalate_to_human'],
    )

    assert record in memory_store.all()
    assert record.selected_option == 'escalate_to_human'


def test_memory_penalizes_failed_prior_option():
    memory_store = MemoryStore()
    agent = DecisionAgent(memory_store)

    failed_record = DecisionRecord(
        context={'risk_level': 'high'},
        options=['continue_current_task', 'escalate_to_human'],
        selected_option='escalate_to_human',
        rationale={},
        outcome='failure',
    )
    memory_store.add(failed_record)

    new_record = agent.decide(
        context={'risk_level': 'high'},
        options=['continue_current_task', 'escalate_to_human'],
    )

    assert new_record.selected_option == 'continue_current_task'


def test_evaluator_detects_memory_influence():
    memory_store = MemoryStore()
    agent = DecisionAgent(memory_store)
    evaluator = Evaluator()

    first_record = agent.decide(
        context={'risk_level': 'high'},
        options=['continue_current_task', 'escalate_to_human'],
    )
    agent.update_outcome(first_record, 'failure')

    second_record = agent.decide(
        context={'risk_level': 'high'},
        options=['continue_current_task', 'escalate_to_human'],
    )
    agent.update_outcome(second_record, 'success')

    summary = evaluator.summarize(first_record, second_record)

    assert summary['decision_changed'] is True
    assert summary['outcome_improved'] is True
    assert summary['memory_influenced_decision'] is True
