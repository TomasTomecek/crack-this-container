from django.db import models


class Game(models.Model):
    """
    game instance
    """
    start_dt = models.DateTimeField()
    name = models.CharField(max_length=64)


class Solution(models.Model):
    """
    game solution
    """
    game = models.ForeignKey(Game, models.CASCADE)
    name = models.CharField(max_length=255)
    submitted_dt = models.DateTimeField()  # set as latest
