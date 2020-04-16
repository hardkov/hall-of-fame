from django.db import models
import datetime as d


class Group(models.Model):
    year = models.IntegerField(default=int(d.datetime.now().year))
    day_of_the_week = models.CharField(max_length=10)
    lecturer = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.year}_{self.day_of_the_week}_{self.lecturer}'
