import json
import sqlite3

from .decision_record import DecisionRecord


class SQLiteMemoryStore:
    def __init__(self, db_path="decision_memory.db"):
        self.db_path = db_path
        self._create_table()

    def add(self, record):
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO decision_records (
                    context,
                    options,
                    selected_option,
                    rationale,
                    outcome
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self._to_json(record.context),
                    self._to_json(record.options),
                    record.selected_option,
                    self._to_json(record.rationale),
                    record.outcome,
                ),
            )

    def all(self):
        return self._query("SELECT context, options, selected_option, rationale, outcome FROM decision_records ORDER BY id")

    def find_by_context_key(self, key, value):
        return [
            record for record in self.all()
            if record.context.get(key) == value
        ]

    def find_successful_decisions(self):
        return self._query(
            """
            SELECT context, options, selected_option, rationale, outcome
            FROM decision_records
            WHERE outcome = ?
            ORDER BY id
            """,
            ("success",),
        )

    def find_failed_decisions(self):
        return self._query(
            """
            SELECT context, options, selected_option, rationale, outcome
            FROM decision_records
            WHERE outcome = ?
            ORDER BY id
            """,
            ("failure",),
        )

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS decision_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    context TEXT NOT NULL,
                    options TEXT NOT NULL,
                    selected_option TEXT NOT NULL,
                    rationale TEXT NOT NULL,
                    outcome TEXT
                )
                """
            )

    def _query(self, query, parameters=()):
        with self._connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [self._row_to_record(row) for row in rows]

    @staticmethod
    def _to_json(value):
        return json.dumps(value, sort_keys=True)

    @staticmethod
    def _from_json(value):
        return json.loads(value)

    @classmethod
    def _row_to_record(cls, row):
        context, options, selected_option, rationale, outcome = row
        return DecisionRecord(
            context=cls._from_json(context),
            options=cls._from_json(options),
            selected_option=selected_option,
            rationale=cls._from_json(rationale),
            outcome=outcome,
        )
