from django.utils import timezone
import itertools, random
from django.db import models

class Game(models.Model):
    max_x = models.PositiveSmallIntegerField(default=8)
    max_y = models.PositiveSmallIntegerField(default=8)
    create_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    won = models.BooleanField(default=False)

    def complete(self, outcome):
        self.completed = True
        self.won = outcome
        self.end_date = timezone.now()
        self.save()

        return self

    def create_mines(self):
        self.start_date = timezone.now()
        self.save()

        i = 0;
        while i < 10:
            x = random.randint(0, self.max_x - 1)
            y = random.randint(0, self.max_y - 1)
            t = Mine.objects.filter(game=self, x=x, y=y).count()
            if t == 0:
                m = Mine(game=self, x=x, y=y)
                m.save()
                i = i + 1

        return self

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
    click = models.BooleanField(default=False)
    flag = models.BooleanField(default=False)
    is_mine = models.BooleanField(default=False)
    mines = models.PositiveSmallIntegerField(default=0)
    move_date = models.DateTimeField(auto_now_add=True)

    def clear(self):
        max_x   = self.game.max_x - 1
        max_y   = self.game.max_y - 1
        start_x = self.x
        start_y = self.y
        spots = list()

        for x in range(start_x - 1, start_x + 2):
            for y in range(start_y - 1, start_y + 2):
                if start_y == y and start_x == x or y < 0 or x < 0 or y > max_y or x > max_x:
                    continue

                exists = Move.objects.filter(game=self.game, x=x, y=y).count()
                if exists > 0:
                    continue

                mines = Mine.objects.filter(game=self.game, x=x, y=y).count()
                if mines > 0:
                    continue

                move = Move(game=self.game, x=x, y=y)
                move.click = True
                move.mines = move.count_mines()
                move.save()

                spots.append({"x": x, "y": y, "mines": move.mines, "click": True, "flag": False})

                if move.mines == 0:
                    cleared = move.clear()
                    spots = list(itertools.chain(spots, cleared))

        return spots

    def count_mines(self):
        max_x = self.game.max_x - 1
        max_y = self.game.max_y - 1
        start_x = self.x
        start_y = self.y
        mines = 0

        for x in range(start_x - 1, start_x + 2):
            for y in range(start_y - 1, start_y + 2):
                if start_y == y and start_x == x or y < 0 or x < 0 or y > max_y or x > max_x:
                    continue

                mines = mines + Mine.objects.filter(game=self.game, x=x, y=y).count()

        return mines

    def __unicode__(self):
        return str(self.id)
