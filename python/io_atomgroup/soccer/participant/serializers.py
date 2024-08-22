import rest_framework.serializers
from . import models

class ParticipantSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = models.Participant
        fields = '__all__'
