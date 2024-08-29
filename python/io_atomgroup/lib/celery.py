import celery
from typing import Any

class Task(celery.Task):
    pass

class Service(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if self.retry:
            self.retry(
                # max_retries=9999999,
                countdown=0,
            )

    def on_retry(self, *args, **kwargs):
        print('blah')
        super().on_retry(*args, **kwargs)
