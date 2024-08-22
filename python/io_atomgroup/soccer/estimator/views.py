from django.shortcuts import render
from .. import sio

@sio.sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)

    await sio.sio.emit(
        'ml_to_front',
        dict(
            a=1,
        )
    )

@sio.sio.event
async def disconnect(sid):
    print('disconnect ', sid)

# Create your views here.
