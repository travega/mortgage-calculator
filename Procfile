web: gunicorn app:server
release: python ./release/migration.py
eventstreams: python ./lib/interest_rate_event_stream.py
enquiryconsumer: python ./lib/consumer.py