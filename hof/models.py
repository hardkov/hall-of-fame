import datetime
from django.db import models


class TaskCollection(models.Model):
    description = models.CharField(max_length=200)


class Task(models.Model):
    task_collection = models.ForeignKey(TaskCollection, on_delete=models.CASCADE)
    max_blood_cells = models.IntegerField(default=1)
    description = models.CharField(max_length=200)


class Group(models.Model):
    year = models.IntegerField(default=int(datetime.datetime.now().year))
    day_of_the_week = models.CharField(max_length=10)
    lecturer = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.year}_{self.day_of_the_week}_{self.lecturer}'


class Student(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nickname


class Score(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    acquired_blood_cells = models.IntegerField(default=0)
    date = models.DateTimeField('due date')

    def __str__(self):
        return self.acquired_blood_cells





