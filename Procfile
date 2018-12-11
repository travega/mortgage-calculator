web: gunicorn app:server
release: python ./release/migration.py
worker: python ./lib/consumer.py
eventstream: python ./lib/interest_rate_event_stream.py