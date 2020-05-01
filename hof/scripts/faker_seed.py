import random
import datetime
import pytz
from faker import Faker

from django.contrib.auth.models import User
from django.contrib.auth.models import Group as _Group
from django.contrib.auth.models import Permission, ContentType

from hof.models import Group, Student, TaskCollection, Task, Score
from hof.models import DayOfTheWeek

from hof.scripts.seed import wipe, create_lecturers_group

fake = Faker(['pl-PL'])
pl = fake['pl-PL']
Faker.seed(4321)  # Will generate the same data

# Globals
no_lecturers = 5
no_groups = 8
no_students = 10
no_task_collections = 3
no_tasks_per_collection = 5
no_scores_per_student = 4


def run():
    # Clearance
    wipe()
    # Lecturers
    lecturer_group = create_lecturers_group()

    lecturers = []
    for _ in range(no_lecturers):
        lecturer = User.objects.create(
            username=pl.user_name(),
            email=pl.email(),
            first_name=pl.first_name(),
            last_name=pl.last_name(),
            is_staff=True
        )
        lecturer.set_password('expass123')
        lecturer.save()
        lecturers.append(lecturer)
        lecturer_group.user_set.add(lecturer)

    # Groups
    groups = []
    dotw = [DayOfTheWeek.MON, DayOfTheWeek.TUE, DayOfTheWeek.WED, DayOfTheWeek.THU, DayOfTheWeek.FRI]
    times = [datetime.time(8, 0, 0), datetime.time(9, 35, 0), datetime.time(11, 15, 0),
             datetime.time(12, 50, 0), datetime.time(14, 40, 0), datetime.time(16, 15, 0),
             datetime.time(17, 50, 0)]
    for _ in range(no_groups):
        group = Group.objects.create(
            year=random.randint(2012, 2020),
            day_of_the_week=dotw[random.randint(0, len(dotw) - 1)],
            time=times[random.randint(0, len(times) - 1)],
            lecturer=lecturers[random.randint(0, len(lecturers) - 1)]
        )
        groups.append(group)

    # Students
    students = []
    for _ in range(no_students):
        student = Student.objects.create(
            group=groups[random.randint(0, len(groups) - 1)],
            first_name=pl.first_name(),
            last_name=pl.last_name(),
            nickname=pl.user_name()
        )
        students.append(student)

    # Task Collections
    task_collections = []
    for _ in range(no_task_collections):
        task_collection = TaskCollection.objects.create(
            description=pl.slug()
        )
        task_collections.append(task_collection)

    # Tasks
    tasks = []
    for tc in task_collections:
        for _ in range(no_tasks_per_collection):
            task = Task.objects.create(
                task_collection=tc,
                max_blood_cells=random.randint(1, 5),
                description=pl.catch_phrase()
            )
            tasks.append(task)

    # Scores
    scores = []
    for student in students:
        for _ in range(no_scores_per_student):
            task_index = random.randint(0, len(tasks) - 1)
            random_date = pl.date_time_ad(
                tzinfo=pytz.timezone('Europe/Warsaw'),
                start_datetime=datetime.datetime(2012, 1, 1, tzinfo=pytz.timezone('Europe/Warsaw')),
                end_datetime=datetime.datetime(2020, 12, 31, tzinfo=pytz.timezone('Europe/Warsaw'))
            )
            score = Score.objects.create(
                task=tasks[task_index],
                student=student,
                acquired_blood_cells=random.randint(0, tasks[task_index].max_blood_cells),
                date=random_date
            )
            scores.append(score)
