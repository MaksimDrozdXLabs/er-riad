import logging
import json
from django.shortcuts import render
from django.utils import timezone
from .. import sio
from . import serializers
from .models import Sio

logger = logging.getLogger(__name__)

@sio.sio.event
async def connect(sid, environ, auth):
    await sio.sio.save_session(
        sid,
        dict(
            http=dict(
                referer=environ.get('HTTP_REFERER'),
                user_agent=environ.get('HTTP_USER_AGENT'),
            ),
            asgi=dict(
                scope=dict(
                    client=environ['asgi.scope'].get('client'),
                )
            )
        )
    )
    logger.info(json.dumps(dict(
        msg='connect ',
        sid=sid,
        session=await sio.sio.get_session(sid),
    )))

    await sio.sio.emit(
        Sio.MessageType.participant_updated.value,
        serializers.ML.KickupSerializer(
            instance=dict(
                ts=timezone.now(),
                count=1,
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
            )
        ).data,
        to=sid,
    )

@sio.sio.event
async def disconnect(sid):
    logger.info(json.dumps(dict(
        msg='disconnect ',
        sid=sid,
        session=await sio.sio.get_session(sid),
    )))

# Create your views here.
