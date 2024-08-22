from django.db import models

# Create your models here.

class Leaderboard(models.Model):
    participant = models.ForeignKey(
        'participant.Participant',
        on_delete=models.PROTECT,
        null=True,
    )
    place = models.IntegerField()
