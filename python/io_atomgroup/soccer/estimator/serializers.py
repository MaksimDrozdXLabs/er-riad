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

    coords = serializers.ListSerializer(
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
