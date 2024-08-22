from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers

# Create your views here.

class LeaderboardViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LeaderboardSerializer
    queryset = models.Leaderboard.objects.all()
