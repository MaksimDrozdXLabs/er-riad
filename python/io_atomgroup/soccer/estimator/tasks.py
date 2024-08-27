import celery
import enum
from typing import (Optional,)
import logging


logger = logging.getLogger(__name__)


class MLMessageType(enum.Enum):
    kickup = 'ml.juggling'

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
                MLMessageType.kickup.value,
                json.dumps(dict(
                    a=1,
                    b=done_count,
                    ts=timezone.now().isoformat(),
                )),
                qos=client.QoS.at_least_once.value,
            )
            time.sleep(delay)
            done_count += 1

@celery.shared_task()
def task_process_estimator(
    max_time: Optional[float | int] = None,
) -> None:

    if max_time is None:
        max_time = 600

    from python.io_atomgroup.lib.paho import Client
    import paho.mqtt.client
    from django.utils import timezone
    import time
    import json

    client = Client(
        paho.mqtt.client.CallbackAPIVersion.VERSION2
    )

    started_at = timezone.now()

    elapsed_get = lambda : (timezone.now() - started_at).total_seconds()

    def mqtt_on_message(client, userdata, message):
        import pprint
        if message.topic == MLMessageType.kickup.value:
            pass
        else:
            raise NotImplementedError

        payload = json.loads(message.payload)

        logger.info(json.dumps(dict(
            qos=message.qos,
            topic=message.topic,
            payload=payload,
        )))

    with client:
        client.connect('mqtt')

        client.on_message = mqtt_on_message
        subscribe_res = client.subscribe(
            MLMessageType.kickup.value,
        )
        assert subscribe_res[0] == paho.mqtt.client.MQTT_ERR_SUCCESS

        while True:
            client.loop(timeout=1)
            if elapsed_get() > max_time:
                break
