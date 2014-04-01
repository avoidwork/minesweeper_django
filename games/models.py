from django.db import models

class Games(models.Model):
    max_x = models.PositiveSmallIntegerField()
    max_y = models.PositiveSmallIntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

class Moves(models.Model):
    game = models.ForeignKey(Games)
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    move_date = models.DateTimeField(auto_now_add=True)