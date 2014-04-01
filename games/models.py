import datetime
from django.utils import timezone
from django.db import models
from profiles.models import UserProfile

class Games(models.Model):
    max_x = models.PositiveSmallIntegerField()
    max_y = models.PositiveSmallIntegerField()
    user = models.ForeignKey(UserProfile)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def was_completed_recently(self):
        return self.end_date >= timezone.now() - datetime.timedelta(days=1)

class Moves(models.Model):
    game = models.ForeignKey(Games)
    user = models.ForeignKey(UserProfile)
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    move_date = models.DateTimeField(auto_now_add=True)