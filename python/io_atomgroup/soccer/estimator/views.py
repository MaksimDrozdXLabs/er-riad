from django.shortcuts import render
from django.utils import timezone
from .. import sio
from . import serializers

@sio.sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)

    await sio.sio.emit(
        'soccer.estimator',
        serializers.Estimator(
            instance=dict(
                participant=1,
                ts=timezone.now(),
            )
        ).data
    )

@sio.sio.event
async def disconnect(sid):
    print('disconnect ', sid)

# Create your views here.
