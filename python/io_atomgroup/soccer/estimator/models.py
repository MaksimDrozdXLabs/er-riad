from django.db import models
import enum

# Create your models here.

class Sio:
    class MessageType(enum.Enum):
        connect = 'connect'
        participant_updated = 'participant.updated'
        disconnect = 'disconnect'
