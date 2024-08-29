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
    request_body=ML.KickupSerializer,
    responses={200: None},
    operation_summary=ML.MessageType.kickup.value,
    operation_description='''
        a message published by ML
        to mqtt, when a kickup has happened

        ```python
            client.publish(
                "{M}",
                ML.Kickup(
                    ts=timezone.now(),
                ).json(),
                #qos=client.QoS.at_least_once.value,
                qos=client.QoS.at_most_once.value,
            )
        ```
    '''.replace(
        '{M}', ML.MessageType.kickup.value,
    ),
    #responses={
    #    200: drf_yasg.openapi.Response(
    #        'participant data',
    #    )
    #},
)
@rest_framework.decorators.api_view(['PUT'])
def ml_kickup(*args, **kwargs) -> None:
    raise NotImplementedError

urlpatterns = [
    path(r'ml.juggling', ml_kickup, name='ml_kickup',),
]
