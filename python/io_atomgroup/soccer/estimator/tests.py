from django.test import TestCase

# Create your tests here.

class TestEstimator(TestCase):
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
            import ipdb
            ipdb.set_trace()
