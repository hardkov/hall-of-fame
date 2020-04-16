import datetime
from django.db import models
from django.utils import datezone


# Create your models here.

class Score(models.Model):
    task = models.ForeignKey(Task)
    student = models.ForeignKey(Student)
    acquired_blood_cells = models.IntegerField(default=0)
    date = models.DateTimeField('due date')

    def __str__(self):
        return self.acquired_blood_cells
