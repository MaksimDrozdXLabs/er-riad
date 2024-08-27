import paho.mqtt.client
import enum


class Client(paho.mqtt.client.Client):
    class QoS(enum.Enum):
        at_most_once = 0
        at_least_once = 1
        exactly_once = 2

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if not self._sock is None:
            self.disconnect()
