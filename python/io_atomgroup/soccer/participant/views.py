from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers

# Create your views here.

class ParticipantViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ParticipantSerializer
    queryset = models.Participant.objects.all()
