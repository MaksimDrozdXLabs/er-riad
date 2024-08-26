from django.db import models

# Create your models here.

class Participant(models.Model):
    class Status(models.TextChoices):
        new = 'new'
        started = 'started'
        done = 'done'

    name = models.CharField(max_length=256)
    score = models.IntegerField()
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=Status,
        max_length=32,
        default=Status.new,
    )
