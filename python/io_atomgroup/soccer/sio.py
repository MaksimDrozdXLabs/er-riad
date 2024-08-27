import socketio

SIO_REDIS = 'redis://redis:6379/1'

mgr_pub = socketio.AsyncRedisManager(SIO_REDIS, write_only=True,)

mgr = socketio.AsyncRedisManager(SIO_REDIS)

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    client_manager=mgr,
    #logger=True,
    #engineio_logger=True,
)

sio_app = socketio.ASGIApp(
    socketio_server=sio,
    socketio_path='',
)
