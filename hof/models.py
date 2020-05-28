import datetime

from django.db import models
from django.contrib.auth.models import User
from django import forms


class DayOfTheWeek(models.TextChoices):
    MON = 'Monday'
    TUE = 'Tuesday'
    WED = 'Wednesday'
    THU = 'Thursday'
    FRI = 'Friday'


class TaskCollection(models.Model):
    description = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.description[:30]}'


class Task(models.Model):
    task_collection = models.ForeignKey(TaskCollection, on_delete=models.CASCADE)
    max_blood_cells = models.FloatField(default=1)
    description = models.CharField(max_length=200)

    def clean(self):
        if self.max_blood_cells < 0:
            raise forms.ValidationError(
                'Max blood cells amount can\'t be less than zero'
            )

    def __str__(self):
        return f'{self.description[:30]}\t'


class Group(models.Model):
    year = models.IntegerField(default=int(datetime.datetime.now().year))

    day_of_the_week = models.CharField(
        max_length=12,
        choices=DayOfTheWeek.choices
    )

    time = models.TimeField(default=datetime.time(8, 0, 0))
    lecturer = models.ForeignKey(User, limit_choices_to={'groups__name': 'Lecturer'}, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.year}_{self.day_of_the_week}_hour{self.time.hour}_{self.lecturer}'


class Student(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.nickname}'


class Score(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    acquired_blood_cells = models.FloatField(default=1)
    date = models.DateTimeField('Due date')

    def clean(self):
        if self.acquired_blood_cells < 0:
            raise forms.ValidationError(
                f'Number of acquired blood cells can\'t be less than 0'
            )

        if self.acquired_blood_cells > self.task.max_blood_cells:
            raise forms.ValidationError(
                f'Extending ({self.acquired_blood_cells}) max blood '
                f'cells value ({self.task.max_blood_cells}) for this task'
            )

    def __str__(self):
        return f'{self.acquired_blood_cells}'
