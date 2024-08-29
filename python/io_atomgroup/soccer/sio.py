import socketio
from django.conf import settings

mgr_pub = socketio.AsyncRedisManager(settings.SIO_REDIS, write_only=True,)
mgr_pub_sync = socketio.RedisManager(settings.SIO_REDIS, write_only=True,)

mgr = socketio.AsyncRedisManager(settings.SIO_REDIS)

mgr_sync = socketio.RedisManager(settings.SIO_REDIS)

sio = socketio.AsyncServer(
    async_mode='asgi',
    #cors_allowed_origins=['*'],
    cors_allowed_origins=[],
    #cors_credentials=False,
    client_manager=mgr,
    ping_timeout=5,
    ping_interval=5,
    transports=["websocket"],
    #logger=True,
    #engineio_logger=True,
)

sio_app = socketio.ASGIApp(
    socketio_server=sio,
    socketio_path='',
)
