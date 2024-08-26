mkdir -p /app/tmp/celery/
exec celery -A python.io_atomgroup.soccer beat -s /app/tmp/celery/beat-schedule
