"""
ASGI config for soccer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

import fastapi
from fastapi.middleware.cors import CORSMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python.io_atomgroup.soccer.settings')

from django.core.asgi import get_asgi_application
from . import sio

fastapi_app = fastapi.FastAPI()

django_app = get_asgi_application()

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_app.mount(
    '/socket.io',
    sio.sio_app
)

fastapi_app.mount(
    '/api',
    django_app
)

import python.io_atomgroup.soccer.estimator.views

from . import celery

application = fastapi_app
