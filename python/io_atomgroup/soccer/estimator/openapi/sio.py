import drf_yasg.utils
import drf_yasg.openapi
from django.urls import path
import rest_framework.decorators
from ...participant.serializers import ParticipantSerializer

class ParticipantUpdated(rest_framework.serializers.Serializer):
    class Meta:
        ref_name = None

    participant = ParticipantSerializer()

@drf_yasg.utils.swagger_auto_schema(
    methods=['GET'],
    responses={
        200: drf_yasg.openapi.Response(
            'participant data',
            ParticipantUpdated,
        )
    },
)
@rest_framework.decorators.api_view(['GET'])
def participant_updated(*args, **kwargs):
    '''
        being trigger when score has been updated
        for a Participant with status=started
        by an ML estimator
    '''

    raise NotImplementedError

urlpatterns = [
    path(r'participant.updated', participant_updated, name='participant_updated',),
]
