import celery
from typing import (Optional,)
import logging


logger = logging.getLogger(__name__)


@celery.shared_task()
def task_simulate_estimator(
    max_count: Optional[int] = None,
) -> None:

    if max_count is None:
        max_count = 16

    import paho.mqtt.client
    from django.utils import timezone
    import time
    import json

    client = paho.mqtt.client.Client(
        paho.mqtt.client.CallbackAPIVersion.VERSION2
    )
    client.connect('mqtt')

    done_count = 0

    logger.info('started')

    while True:
        if done_count >= max_count:
            break

        client.publish(
            'estimator',
            json.dumps(dict(
                a=1,
                ts=timezone.now().isoformat(),
            ))
        )
        time.sleep(1)
        done_count += 1
