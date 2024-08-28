import drf_yasg.utils
import drf_yasg.openapi
from django.urls import path
import rest_framework.decorators
from ..serializers import ML

class Kickup(rest_framework.serializers.Serializer):
    class Meta:
        ref_name = None

    # participant = ParticipantSerializer()

@drf_yasg.utils.swagger_auto_schema(
    methods=['PUT'],
    request_body=Kickup,
    #responses={
    #    200: drf_yasg.openapi.Response(
    #        'participant data',
    #    )
    #},
)
@rest_framework.decorators.api_view(['PUT'])
def ml_kickup(*args, **kwargs):
    '''
        a message published by ML
        to mqtt, when a kickup has happened
    '''

    raise NotImplementedError

urlpatterns = [
    path(r'ml.juggling', ml_kickup, name='ml_kickup',),
]
