web: gunicorn app:server
release: python ./release/migration.py
worker: python ./lib/consumer.py