import logging
import json
from django.test import TestCase

logger = logging.getLogger(__name__)

# Create your tests here.

class TestEstimator(TestCase):
    #@classmethod
    #def setUpClass(cls):
    #    import signal
    #
    #    def interrupt(*args, **kwargs):
    #        raise KeyboardInterrupt
    #
    #    signal.signal(signal.SIGINT, interrupt)

    async def test_socket(self):
        import socketio
        import pprint

        async with socketio.async_simple_client.AsyncSimpleClient() as client:
            await client.connect(
                'ws://nginx/socket.io',
            )
            sid = client.sid
            response = await client.receive(timeout=1)

            self.assertEqual(
                response[0],
                'participant.updated',
            )

            response = await client.receive(timeout=1)

    async def test_socket_eternalread(self):
        import socketio
        import pprint

        async with socketio.async_simple_client.AsyncSimpleClient(
        ) as client:
            await client.connect(
                'ws://nginx/socket.io',
                transports=['websocket'],
            )
            sid = client.sid
            logger.info(json.dumps(dict(sid=sid)))
            while True:
                response = await client.receive()
                print(response)
