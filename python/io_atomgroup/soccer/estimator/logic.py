from .serializers import ML
import logging
import json


logger = logging.getLogger(__name__)


def estimator_process_kickup(kickup: ML.Kickup) -> None:
    import django.db.transaction
    from ..participant.models import Participant
    from ..participant.serializers import ParticipantSerializer
    from ..sio import mgr_pub
    from .models import Sio

    with django.db.transaction.atomic():
        q_started = Participant.objects.filter(
            status=Participant.Status.started
        ).select_for_update()

        p = q_started.first()

        if q_started.count() > 1:
            logger.error(json.dumps(dict(
                msg='too much started, quit',
            )))
            return

        if q_started.count() == 0 or p is None:
            logger.info(json.dumps(dict(
                msg='frontend did not annotate a user, quit',
            )))
            return

        assert kickup.count
        p.score += kickup.count

        p.save(update_fields=['score'])
        mgr_pub.emit(
            Sio.MessageType.participant_updated.value,
            data=dict(
                participant=ParticipantSerializer(
                    instance=p,
                ).data,
            ),
        )
