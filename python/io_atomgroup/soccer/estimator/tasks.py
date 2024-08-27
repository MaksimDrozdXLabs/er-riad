import celery
import pydantic
import pydantic_core
import enum
from typing import (Optional, Literal, List)
import logging


logger = logging.getLogger(__name__)


class ML:
    class MessageType(enum.Enum):
        kickup = 'ml.juggling'

    class Kickup(pydantic.BaseModel):
        class Ball(pydantic.BaseModel):
            x : int | float
            y : int | float
            z : int | float

        class Pose(pydantic.BaseModel):
            class Joint(pydantic.BaseModel):
                x : int | float
                y : int | float
                z : int | float
                _type : Literal['Head', 'LFoot', 'RFoot']

            joints : List[Joint]

        ball : Optional[Ball] = None
        pose : Optional[Pose] = None

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
                json.dumps(dict(
                    pose=dict(
                        joints=[
                            dict(
                                x=0,
                                y=0,
                                z=0,
                                joint='Head',
                            ),
                            dict(
                                x=0,
                                y=0,
                                z=0,
                                joint='LFoot',
                            ),
                            dict(
                                x=0,
                                y=0,
                                z=0,
                                joint='RFoot',
                            ),
                        ],
                    ),
                    ball=dict(
                        x=0,
                        y=0,
                        z=0,
                    ),
                    count=4,
                    ts=timezone.now().isoformat(),
                )),
                qos=client.QoS.at_least_once.value,
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
        import pprint
        payload = pydantic_core.from_json(message.payload)

        if message.topic == ML.MessageType.kickup.value:
            kickup = ML.Kickup.model_validate(
                payload,
            )
            import ipdb
            ipdb.set_trace()
            pass
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

@celery.shared_task()
def task_process_estimator(*args, **kwargs):
    return task_process_estimator_raw(*args, **kwargs)
