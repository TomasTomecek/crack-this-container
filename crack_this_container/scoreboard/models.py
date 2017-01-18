import datetime

from django.db import models

from django.core.exceptions import ObjectDoesNotExist


class GameQuerySet(models.QuerySet):
    pass


class GameManager(models.Manager):
    def latest_game(self):
        try:
            return self.latest("create_dt")
        except ObjectDoesNotExist:
            return Game.create()


class Game(models.Model):
    """
    game instance
    """
    codenames = [
        "Blue",
        "Brown",
        "Orange"
    ]
    message_templates = [
        "Congratulations, you have won! Your codename is %s.",
        "You scored second, well done! Your codename is %s.",
        "You have earned a third place, nicely done. Your codename is %s."
    ]
    too_late = "You did it! Unfortunately you were too late to make it to the top three."

    create_dt = models.DateTimeField(auto_now_add=True)
    start_dt = models.DateTimeField(blank=True, null=True)

    objects = GameManager.from_queryset(GameQuerySet)()

    @classmethod
    def create(cls):
        obj = cls()
        obj.save()
        return obj

    def __str__(self):
        return "%s" % self.create_dt

    @property
    def solutions_count(self):
        return self.solutions.count()

    @property
    def has_started(self):
        return self.start_dt is not None

    @property
    def timer(self):
        diff = datetime.datetime.now() - self.start_dt
        minutes = diff.total_seconds() // 60
        seconds = int(diff.total_seconds() % 60)
        return "%02d : %02d" % (minutes, seconds)

    def submit_solution(self):
        if self.solutions_count >= len(self.codenames):
            return "TOO_LATE", self.too_late
        else:
            c = self.codenames[self.solutions_count]
            return c, self.message_templates[self.solutions_count] % c

    def start_game(self):
        self.start_dt = datetime.datetime.now()
        self.save()

    @property
    def ordered_solutions(self):
        return self.solutions.order_by("submitted_dt")


class Solution(models.Model):
    """
    game solution
    """
    game = models.ForeignKey(Game, models.CASCADE, related_name="solutions")
    name = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    submitted_dt = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, game):
        codename, message = game.submit_solution()
        obj = cls(game=game, name=codename, message=message)
        obj.save()
        return obj

    @property
    def elapsed(self):
        return "%.1f s" % (self.submitted_dt - self.game.start_dt).total_seconds()

    @property
    def listing_text(self):
        return "Mr. %s in %s." % (self.name, self.elapsed)
