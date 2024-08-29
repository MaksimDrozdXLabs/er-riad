mkdir -p /app/tmp/celery/
exec celery -A python.io_atomgroup.soccer beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
