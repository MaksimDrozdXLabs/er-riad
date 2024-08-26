import celery
from typing import (Optional,)
import logging


logger = logging.getLogger(__name__)


@celery.shared_task()
def task_simulate_estimator(
    max_count: Optional[int] = None,
    delay: Optional[float | int] = None,
) -> None:

    if delay is None:
        delay = 1

    if max_count is None:
        max_count = 16

    from python.io_atomgroup.lib.paho import Client
    import paho.mqtt.client
    from django.utils import timezone
    import time
    import json

    client = Client(
        paho.mqtt.client.CallbackAPIVersion.VERSION2
    )

    with client:
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
            time.sleep(delay)
            done_count += 1
