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
    ]

    class Meta:
        model = models.Participant

admin.site.register(
    models.Participant,
    ParticipantAdmin,
)
