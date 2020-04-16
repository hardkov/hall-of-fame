from django.db import models


# Create your models here.
class Student(models.Model):
    group = models.ForeignKey(Group)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nickname


class Task(models.Model):
    task_collection = models.ForeignKey(TaskCollection, on_delete=models.CASCADE)
    max_blood_cells = models.IntegerField(default=1)
    description = models.CharField(max_length=200)


class TaskCollection(models.Model):
    description = models.CharField(max_length=200)
