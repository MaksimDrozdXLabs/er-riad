import celery
import time
from typing import (Optional, Literal, List)
import pydantic_core
import logging
from ...lib.celery import Service
from .serializers import ML


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
                ML.MessageType.kickup.value,
                ML.Kickup(
                    pose=ML.Kickup.Pose(
                        joints=[
                            ML.Kickup.Pose.Joint(
                                x=0,
                                y=0,
                                z=0,
                                joint='Head',
                            ),
                            ML.Kickup.Pose.Joint(
                                x=0,
                                y=0,
                                z=0,
                                joint='LFoot',
                            ),
                            ML.Kickup.Pose.Joint(
                                x=0,
                                y=0,
                                z=0,
                                joint='RFoot',
                            ),
                        ],
                    ),
                    ball=ML.Kickup.Ball(
                        x=0,
                        y=0,
                        z=0,
                    ),
                    count=4,
                    ts=timezone.now(),
                ).json(),
                #qos=client.QoS.at_least_once.value,
                qos=client.QoS.at_most_once.value,
            )
            time.sleep(delay)
            done_count += 1

def task_process_estimator_raw(
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
        from . import logic
        payload = pydantic_core.from_json(message.payload)

        print('blah')
        if message.topic == ML.MessageType.kickup.value:
            kickup = ML.Kickup.model_validate(
                payload,
            )
            logic.estimator_process_kickup(kickup)
        else:
            raise NotImplementedError


        logger.info(json.dumps(dict(
            qos=message.qos,
            topic=message.topic,
            payload=payload,
        )))

    with client:
        client.connect('mqtt')

        client.on_message = mqtt_on_message
        subscribe_res = client.subscribe(
            ML.MessageType.kickup.value,
        )
        assert subscribe_res[0] == paho.mqtt.client.MQTT_ERR_SUCCESS

        while True:
            client.loop(timeout=1)
            if elapsed_get() > max_time:
                break

@celery.shared_task(track_start=True,)
def task_process_estimator(*args, **kwargs):
    try:
        return task_process_estimator_raw(*args, **kwargs)
    except:
        celery.current_app.current_task.apply_async(
            args=args,
            kwargs=kwargs,
            countdown=4,
        )
        raise
