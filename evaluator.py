class Evaluator:
    def decision_changed(self, first_record, second_record):
        return first_record.selected_option != second_record.selected_option

    def outcome_improved(self, first_record, second_record):
        return first_record.outcome == 'failure' and second_record.outcome == 'success'

    def memory_influenced_decision(self, second_record):
        scored_options = second_record.rationale.get('scored_options', [])
        return any(score != self._base_score(option) for option, score in scored_options)

    def summarize(self, first_record, second_record):
        return {
            'decision_changed': self.decision_changed(first_record, second_record),
            'outcome_improved': self.outcome_improved(first_record, second_record),
            'memory_influenced_decision': self.memory_influenced_decision(second_record),
        }

    def _base_score(self, option):
        if option == 'escalate_to_human':
            return 3
        if option == 'pause_and_inspect':
            return 2
        if option == 'switch_to_safe_task':
            return 2
        if option == 'continue_current_task':
            return 1
        return 0
