from django.db import models

class Game(models.Model):
    max_x = models.PositiveSmallIntegerField(default=8)
    max_y = models.PositiveSmallIntegerField(default=8)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    won = models.BooleanField(default=False)

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

    def clear(self):
        start_x = self.x
        start_y = self.y
        spots = []

        for x in range(start_x - 1, start_x + 2):
            for y in range(start_y - 1, start_y + 2):
                if start_y == y and start_x == x:
                    continue

                if y < 0 or x < 0:
                    continue

                try:
                    mine = Mine(game=self.game, x=x, y=y)
                except Mine.DoesNotExist:
                    continue

                spots.append({"x":x, "y": y})

        return spots

    def __unicode__(self):
        return str(self.id)