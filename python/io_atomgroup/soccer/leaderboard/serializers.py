import rest_framework.serializers
from . import models

class LeaderboardSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = models.Leaderboard
        fields = '__all__'
