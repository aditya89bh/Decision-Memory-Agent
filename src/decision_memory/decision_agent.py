from .decision_record import DecisionRecord


class DecisionAgent:
    def __init__(self, memory_store):
        self.memory_store = memory_store

    def decide(self, context, options):
        scored_options = []

        for option in options:
            score = self._base_score(option)
            score += self._memory_adjustment(context, option)
            scored_options.append((option, score))

        scored_options.sort(key=lambda item: item[1], reverse=True)
        selected_option, selected_score = scored_options[0]

        rationale = self._build_rationale(selected_option, selected_score, scored_options)

        record = DecisionRecord(
            context=context,
            options=options,
            selected_option=selected_option,
            rationale=rationale,
        )

        self.memory_store.add(record)
        return record

    def update_outcome(self, record, outcome):
        record.outcome = outcome
        return record

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

    def _memory_adjustment(self, context, option):
        adjustment = 0
        similar_records = self.memory_store.find_by_context_key(
            'risk_level',
            context.get('risk_level'),
        )

        for record in similar_records:
            if record.selected_option != option:
                continue

            if record.outcome == 'success':
                adjustment += 2
            elif record.outcome == 'failure':
                adjustment -= 3

        return adjustment

    def _build_rationale(self, selected_option, selected_score, scored_options):
        return {
            'selected_option': selected_option,
            'selected_score': selected_score,
            'scored_options': scored_options,
            'reason': 'Selected the highest-scoring option after applying memory-based adjustments.',
        }
