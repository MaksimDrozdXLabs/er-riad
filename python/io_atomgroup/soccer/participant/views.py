import rest_framework
import drf_yasg.utils
from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers

# Create your views here.

class ParticipantViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ParticipantSerializer
    queryset = models.Participant.objects.all()

    @rest_framework.decorators.action(
        detail=False,
        methods=['get'],
    )
    def leaderboard(self, request):
        raise NotImplementedError
