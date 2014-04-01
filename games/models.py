import datetime
from django.utils import timezone
from django.db import models

class Game(models.Model):
    max_x = models.PositiveSmallIntegerField()
    max_y = models.PositiveSmallIntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def was_completed_recently(self):
        return self.end_date >= timezone.now() - datetime.timedelta(days=1)

class Move(models.Model):
    game = models.ForeignKey(Game)
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    move_date = models.DateTimeField(auto_now_add=True)