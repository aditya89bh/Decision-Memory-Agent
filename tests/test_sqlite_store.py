from decision_memory import DecisionRecord, SQLiteMemoryStore


def make_record(context=None, options=None, selected_option='inspect', rationale=None, outcome='success'):
    return DecisionRecord(
        context=context or {'risk_level': 'high', 'site': 'factory-a'},
        options=options or ['continue', 'inspect'],
        selected_option=selected_option,
        rationale=rationale or {'reason': 'Reduce operational risk'},
        outcome=outcome,
    )


def test_sqlite_store_persists_records_across_instances(tmp_path):
    db_path = tmp_path / 'memory.db'
    store = SQLiteMemoryStore(db_path=str(db_path))
    record = make_record()

    store.add(record)
    reloaded_store = SQLiteMemoryStore(db_path=str(db_path))

    records = reloaded_store.all()
    assert len(records) == 1
    assert isinstance(records[0], DecisionRecord)
    assert records[0].context == record.context
    assert records[0].options == record.options
    assert records[0].selected_option == record.selected_option
    assert records[0].rationale == record.rationale
    assert records[0].outcome == record.outcome


def test_sqlite_store_finds_records_by_context_key(tmp_path):
    store = SQLiteMemoryStore(db_path=str(tmp_path / 'memory.db'))
    matching_record = make_record(context={'risk_level': 'high', 'site': 'factory-a'})
    other_record = make_record(context={'risk_level': 'low', 'site': 'factory-b'})

    store.add(matching_record)
    store.add(other_record)

    matches = store.find_by_context_key('risk_level', 'high')
    assert len(matches) == 1
    assert isinstance(matches[0], DecisionRecord)
    assert matches[0].context['site'] == 'factory-a'


def test_sqlite_store_finds_successful_and_failed_decisions(tmp_path):
    store = SQLiteMemoryStore(db_path=str(tmp_path / 'memory.db'))
    successful_record = make_record(selected_option='inspect', outcome='success')
    failed_record = make_record(selected_option='continue', outcome='failure')
    unknown_record = make_record(selected_option='defer', outcome=None)

    store.add(successful_record)
    store.add(failed_record)
    store.add(unknown_record)

    successful = store.find_successful_decisions()
    failed = store.find_failed_decisions()

    assert [record.selected_option for record in successful] == ['inspect']
    assert [record.selected_option for record in failed] == ['continue']
    assert all(isinstance(record, DecisionRecord) for record in successful + failed)
