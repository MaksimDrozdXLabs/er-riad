import paho.mqtt.client


class Client(paho.mqtt.client.Client):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        if not self._sock is None:
            self.disconnect()
