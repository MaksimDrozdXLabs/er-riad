from django.contrib import admin
from . import models

# Register your models here.

class ParticipantAdmin(admin.ModelAdmin):
    class Meta:
        model = models.Participant

admin.site.register(
    models.Participant,
    ParticipantAdmin,
)
