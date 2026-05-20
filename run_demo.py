from decision_memory import DecisionAgent, Evaluator, MemoryStore


memory_store = MemoryStore()
agent = DecisionAgent(memory_store)
evaluator = Evaluator()


print('\n=== Decision Memory Agent Demo ===\n')


context_1 = {
    'task': 'cnc_machine_loading',
    'risk_level': 'high',
    'robot_confidence': 'low',
}

options = [
    'continue_current_task',
    'pause_and_inspect',
    'switch_to_safe_task',
    'escalate_to_human',
]


print('--- Scenario 1 ---')
print('Context:', context_1)

record_1 = agent.decide(context_1, options)
agent.update_outcome(record_1, 'failure')

print('Selected option:', record_1.selected_option)
print('Outcome:', record_1.outcome)
print('Rationale:', record_1.rationale)


context_2 = {
    'task': 'cnc_machine_loading',
    'risk_level': 'high',
    'robot_confidence': 'low',
}


print('\n--- Scenario 2 ---')
print('Context:', context_2)

record_2 = agent.decide(context_2, options)
agent.update_outcome(record_2, 'success')

print('Selected option:', record_2.selected_option)
print('Outcome:', record_2.outcome)
print('Rationale:', record_2.rationale)


print('\n--- Memory Summary ---')
for index, record in enumerate(memory_store.all(), start=1):
    print(f'Record {index}:')
    print(record.to_dict())
    print()


print('--- Evaluation Summary ---')
summary = evaluator.summarize(record_1, record_2)
for key, value in summary.items():
    print(f'{key}: {value}')
