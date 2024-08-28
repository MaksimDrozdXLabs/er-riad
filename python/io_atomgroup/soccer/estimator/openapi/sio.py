import drf_yasg.utils
import drf_yasg.openapi
from django.urls import path
import rest_framework.decorators
from ..models import Sio
from ...participant.serializers import ParticipantSerializer

class ParticipantUpdated(rest_framework.serializers.Serializer):
    class Meta:
        ref_name = None

    participant = ParticipantSerializer()

@drf_yasg.utils.swagger_auto_schema(
    methods=['GET'],
    operation_summary=Sio.MessageType.participant_updated.value,
    operation_description='''
        being trigger when score has been updated
        for a Participant with status=started
        by an ML estimator

        ```js
            socket.on('{M}', (data) => {...});
        ```
    '''.replace(
        '{M}', Sio.MessageType.participant_updated.value,
    ),
    responses={
        200: drf_yasg.openapi.Response(
            'participant data',
            ParticipantUpdated,
        )
    },
)
@rest_framework.decorators.api_view(['GET'])
def participant_updated(*args, **kwargs):

    raise NotImplementedError

urlpatterns = [
    path(
        Sio.MessageType.participant_updated.value,
        participant_updated,
        name=Sio.MessageType.participant_updated.name,
    ),
]
