class DecisionRecord:
    def __init__(self, context, options, selected_option, rationale, outcome=None):
        self.context = context
        self.options = options
        self.selected_option = selected_option
        self.rationale = rationale
        self.outcome = outcome

    def to_dict(self):
        return {
            'context': self.context,
            'options': self.options,
            'selected_option': self.selected_option,
            'rationale': self.rationale,
            'outcome': self.outcome,
        }
