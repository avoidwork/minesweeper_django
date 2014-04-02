from django.utils import timezone
import itertools
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

    def complete(self, outcome):
        self.completed = True
        self.won = outcome
        self.end_date = timezone.now()
        self.save()

        return outcome

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
        max_x   = int(self.game.max_x)
        max_y   = int(self.game.max_y)
        start_x = int(self.x)
        start_y = int(self.y)
        spots = list()

        for x in range(start_x - 1, start_x + 2):
            for y in range(start_y - 1, start_y + 2):
                if start_y == y and start_x == x:
                    continue

                if y < 0 or x < 0 or y > max_y or x > max_x:
                    continue

                exists = Move.objects.filter(game=self.game, x=x, y=y).count()
                if exists > 0:
                    continue

                mine = Mine.objects.filter(game=self.game, x__in=[x - 1, x, x + 1], y__in=[y - 1, y, y + 1]).count()
                if mine == 0:
                    spots.append({"x":x, "y": y})
                    move = Move(game=self.game, x=x, y=y)
                    move.save()
                    cleared = move.clear()
                    spots = list(itertools.chain(spots, cleared))

        mines = Mine.objects.filter(game=self.game).count()
        moves = Move.objects.filter(game=self.game).count()

        if mines + moves >= self.game.max_x * self.game.max_y:
            self.game.complete(True)

        return spots

    def __unicode__(self):
        return str(self.id)