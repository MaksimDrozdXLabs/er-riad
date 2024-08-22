from django.contrib import admin
from . import models

# Register your models here.

class LeaderboardAdmin(admin.ModelAdmin):
    class Meta:
        model = models.Leaderboard

admin.site.register(
    models.Leaderboard,
    LeaderboardAdmin,
)
