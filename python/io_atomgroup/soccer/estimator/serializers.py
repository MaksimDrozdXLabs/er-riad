import enum
import datetime
import pydantic
import pydantic_core
from typing import (Optional, Literal, List)
from rest_framework import serializers

class Ball(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()
    z = serializers.IntegerField()

class Pose(serializers.Serializer):
    class Coord(serializers.Serializer):
        x = serializers.IntegerField()
        y = serializers.IntegerField()
        z = serializers.IntegerField()
        joint = serializers.CharField()

    coords = serializers.ListSerializer[Coord](
        child=Coord()
    )

class Estimator(serializers.Serializer):
    participant = serializers.IntegerField(required=True,)
    is_start = serializers.BooleanField(required=False)
    is_stop = serializers.BooleanField(required=False)
    counter = serializers.IntegerField(required=False)
    pose = Pose(required=False)
    ball = Ball(required=False)
    ts = serializers.DateTimeField()

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
        count : int = 0
        ts : Optional[datetime.datetime] = None
