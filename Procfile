web: gunicorn app:server
release: python ./release/migration.py
worker: python ./lib/consumer.py
worker: python ./lib/interest_rate_event_stream.py