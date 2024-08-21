from django.shortcuts import render
from .. import sio

@sio.sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.sio.event
def disconnect(sid):
    print('disconnect ', sid)

# Create your views here.
