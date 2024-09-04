from django.contrib import admin
from . import models

# Register your models here.

class ParticipantAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'score',
        'updated',
        'contact',
        'email',
        'status',
    ]

    @admin.action()
    def task_simulator_estimator(*args, **kwargs):
        from .. import celery
        from ..estimator.tasks import task_simulate_estimator

        task_simulate_estimator.apply_async(
            queue=celery.Queue.admin.value,
            soft_time=120,
        )

    actions = [
        task_simulator_estimator,
    ]

    class Meta:
        model = models.Participant

admin.site.register(
    models.Participant,
    ParticipantAdmin,
)
