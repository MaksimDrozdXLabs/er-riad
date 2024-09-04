import rest_framework
import django.db.transaction
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

        queryset = self.queryset.order_by('-score', 'name')[:16]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return rest_framework.response.Response(serializer.data)

    # @django.db.transaction.atomic()
    def update(self, request, *args, **kwargs):
        if (
            kwargs.get('partial') is True and
            isinstance(request.data, dict) and
            'pk' in request.data and
            'status' in request.data
        ):
            self.queryset.filter(
                status=models.Participant.Status.started.value
            #).select_for_update().update(
            ).update(
                status=models.Participant.Status.done.value
            )

            # self.queryset.filter(id=int(request.data['pk'])).select_for_update().get()

        return super().update(request, *args, **kwargs)
