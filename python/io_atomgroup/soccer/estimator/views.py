from django.shortcuts import render
import enum
from django.utils import timezone
from .. import sio
from . import serializers

class MessageType(enum.Enum):
    connect = 'connect'
    participant_updated = 'participant.updated'
    disconnect = 'disconnect'


@sio.sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)

    await sio.sio.emit(
        MessageType.participant_updated.value,
        serializers.Estimator(
            instance=dict(
                participant=1,
                ts=timezone.now(),
                is_start=True,
                counter=1,
                is_stop=False,
                pose=dict(
                    coords=[
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
            )
        ).data,
        to=sid,
    )

@sio.sio.event
async def disconnect(sid):
    print('disconnect ', sid)

# Create your views here.
