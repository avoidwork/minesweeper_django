import datetime
from django.utils import timezone
from django.db import models

class Game(models.Model):
    max_x = models.PositiveSmallIntegerField(default=8)
    max_y = models.PositiveSmallIntegerField(default=8)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return "/games/%i/" % self.id

    def __unicode__(self):
        return str(self.id)

class Mine(models.Model):
    game = models.ForeignKey(Game)
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return str(self.id)

class Move(models.Model):
    game = models.ForeignKey(Game)
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    move_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)