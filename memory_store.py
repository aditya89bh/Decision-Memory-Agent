class MemoryStore:
    def __init__(self):
        self.records = []

    def add(self, record):
        self.records.append(record)

    def all(self):
        return list(self.records)

    def find_by_context_key(self, key, value):
        matches = []
        for record in self.records:
            if record.context.get(key) == value:
                matches.append(record)
        return matches

    def find_successful_decisions(self):
        return [
            record for record in self.records
            if record.outcome == 'success'
        ]

    def find_failed_decisions(self):
        return [
            record for record in self.records
            if record.outcome == 'failure'
        ]
