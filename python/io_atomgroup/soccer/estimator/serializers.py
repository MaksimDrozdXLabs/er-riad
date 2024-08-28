import enum
import datetime
import pydantic
import pydantic_core
from typing import (Optional, Literal, List)
from rest_framework import serializers




class ML:
    class MessageType(enum.Enum):
        kickup = 'ml.juggling'

    class Kickup(pydantic.BaseModel):
        class Ball(pydantic.BaseModel):
            x : int | float
            y : int | float
            z : int | float

        class Pose(pydantic.BaseModel):
            class Joint(pydantic.BaseModel):
                x : int | float
                y : int | float
                z : int | float
                joint : Literal['Head', 'LFoot', 'RFoot']

            joints : List[Joint]

        ball : Optional[Ball] = None
        pose : Optional[Pose] = None
        count : int = 1
        ts : Optional[datetime.datetime] = None

    class KickupSerializer(serializers.Serializer):
        class Ball(serializers.Serializer):
            x = serializers.IntegerField()
            y = serializers.IntegerField()
            z = serializers.IntegerField()

        class Pose(serializers.Serializer):
            class Joint(serializers.Serializer):
                x = serializers.IntegerField()
                y = serializers.IntegerField()
                z = serializers.IntegerField()
                joint = serializers.CharField()

            joints = serializers.ListSerializer[Joint](
                child=Joint()
            )

        ball = Ball(required=False)
        pose = Pose(required=False)
        count = serializers.IntegerField(default=1)
        ts = serializers.DateTimeField()
