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
        '''
            Returns up to 16 participants,
            in a decreasing order of score value;
        '''

        queryset = self.queryset.order_by('-score')[:16]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return rest_framework.response.Response(serializer.data)
