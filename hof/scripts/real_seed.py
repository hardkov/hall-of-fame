import datetime
from django.utils import timezone
import csv
from django.contrib.auth.models import User

from hof.models import Group, Student, TaskCollection, Task, Score
from hof.models import DayOfTheWeek
from .lecturer_group import wipe_lecturers, create_lecturers_group
from hof.scripts.seed import wipe
from faker import Faker

fake = Faker(['pl-PL'])
pl = fake['pl-PL']
Faker.seed(1236)  # Will generate the same data

csv_filename = 'aside/example-data/hof2019.csv'

def run():
    # Clearance
    wipe()
    wipe_lecturers()

    # Lecturers
    lecturer_group = create_lecturers_group()

    lecturer1 = User.objects.create_user(
        username='SPolak',
        password='admin',
        email='spolak@example.com',
        first_name='Stanislaw',
        last_name='Polak',
        is_staff=True
    )
    lecturer_group.user_set.add(lecturer1)

    lecturer2 = User.objects.create_user(
        username='MMajcher',
        password='admin',
        email='MMajcher@example.com',
        first_name='Mateusz',
        last_name='Majcher',
        is_staff=True
    )
    lecturer_group.user_set.add(lecturer2)

    lecturer3 = User.objects.create_user(
        username='Apohllo',
        password='admin',
        email='pohl@example.com',
        first_name='Aleksander',
        last_name='Pohl-Smywinski',
        is_staff=True
    )
    lecturer_group.user_set.add(lecturer3)

    lecturer4 = User.objects.create_user(
        username='ZKaleta',
        password='admin',
        email='zkaleta@example.com',
        first_name='Zbigniew',
        last_name='Kaleta',
        is_staff=True
    )
    lecturer_group.user_set.add(lecturer4)

    # Groups
    groups = []

    group1 = Group(year=2019, day_of_the_week=DayOfTheWeek.MON, time=datetime.time(9, 35, 0), lecturer=lecturer1)
    groups.append(group1)
    group1.save()

    group2 = Group(year=2019, day_of_the_week=DayOfTheWeek.MON, time=datetime.time(12, 50, 0), lecturer=lecturer1)
    groups.append(group2)
    group2.save()

    group3 = Group(year=2019, day_of_the_week=DayOfTheWeek.MON, time=datetime.time(17, 50, 0), lecturer=lecturer2)
    groups.append(group3)
    group3.save()

    group4 = Group(year=2019, day_of_the_week=DayOfTheWeek.TUE, time=datetime.time(14, 40, 0), lecturer=lecturer3)
    groups.append(group4)
    group4.save()

    group5 = Group(year=2019, day_of_the_week=DayOfTheWeek.TUE, time=datetime.time(16, 15, 0), lecturer=lecturer4)
    groups.append(group5)
    group5.save()

    group6 = Group(year=2019, day_of_the_week=DayOfTheWeek.TUE, time=datetime.time(17, 50, 0), lecturer=lecturer4)
    groups.append(group6)
    group6.save()

    group7 = Group(year=2019, day_of_the_week=DayOfTheWeek.WED, time=datetime.time(9, 35, 0), lecturer=lecturer3)
    groups.append(group7)
    group7.save()

    group8 = Group(year=2019, day_of_the_week=DayOfTheWeek.WED, time=datetime.time(11, 15, 0), lecturer=lecturer3)
    groups.append(group8)
    group8.save()

    group9 = Group(year=2019, day_of_the_week=DayOfTheWeek.WED, time=datetime.time(17, 50, 0), lecturer=lecturer3)
    groups.append(group9)
    group9.save()

    group10 = Group(year=2019, day_of_the_week=DayOfTheWeek.WED, time=datetime.time(17, 50, 0), lecturer=lecturer2)
    groups.append(group10)
    group10.save()

    group11 = Group(year=2019, day_of_the_week=DayOfTheWeek.THU, time=datetime.time(11, 15, 0), lecturer=lecturer3)
    groups.append(group11)
    group11.save()

    group12 = Group(year=2019, day_of_the_week=DayOfTheWeek.THU, time=datetime.time(12, 50, 0), lecturer=lecturer3)
    groups.append(group12)
    group12.save()

    group13 = Group(year=2019, day_of_the_week=DayOfTheWeek.THU, time=datetime.time(16, 15, 0), lecturer=lecturer4)
    groups.append(group13)
    group13.save()

    group14 = Group(year=2019, day_of_the_week=DayOfTheWeek.THU, time=datetime.time(17, 50, 0), lecturer=lecturer4)
    groups.append(group14)
    group14.save()

    # TaskCollections
    task_collection1 = TaskCollection(description='Kartkówki')
    task_collection1.save()

    task_collection2 = TaskCollection(description='Zadania Laboratoryjne')
    task_collection2.save()

    task_collection3 = TaskCollection(description='Projekty')
    task_collection3.save()

    quizzes = []
    for i in range(2, 8):
        task = Task(task_collection=task_collection1, max_blood_cells=1, description=f'{i} Kartkowka')
        task.save()
        quizzes.append(task)

    labs = []
    for i in range(2, 9):
        lab = Task(task_collection=task_collection2, max_blood_cells=1, description=f'{i} Zadanie Laboratoryjne')
        lab.save()
        labs.append(lab)

    project1 = Task(task_collection=task_collection3, max_blood_cells=8, description=f'Pierwszy projekt')
    project1.save()

    project2 = Task(task_collection=task_collection3, max_blood_cells=4, description=f'Drugi projekt')
    project2.save()

    project3 = Task(task_collection=task_collection3, max_blood_cells=2, description=f'Wybieranie tematu')
    project3.save()

    with open(csv_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_line = True                               # to be refactored
        group_itr = 0
        for row in csv_reader:
            if first_line:
                first_line = False
                continue

            student = Student(group=groups[group_itr], first_name=pl.first_name(),
                              last_name=pl.last_name(), nickname=row[1])
            student.save()

            for i in range(1, 7):
                if row[2*i] != '':
                    score = Score.objects.create(
                        task=quizzes[i-1],
                        student=student,
                        acquired_blood_cells=int(row[2*i]),
                        date=timezone.now()     # change?
                    )
                    score.save()

                if row[2*i+1] != '':
                    score = Score.objects.create(
                        task=labs[i-1],
                        student=student,
                        acquired_blood_cells=int(row[2*i+1]),
                        date=timezone.now()     # change?
                    )
                    score.save()

            if row[14] != '':
                score = Score.objects.create(
                    task=project3,
                    student=student,
                    acquired_blood_cells=int(row[14]),
                    date=timezone.now()  # change?
                )
                score.save()

            if row[15] != '':
                score = Score.objects.create(
                    task=labs[6],
                    student=student,
                    acquired_blood_cells=int(float(row[15])),
                    date=timezone.now()  # change?
                )
                score.save()

            if row[16] != '':
                score = Score.objects.create(
                    task=project1,
                    student=student,
                    acquired_blood_cells=int(float(row[16])),
                    date=timezone.now()  # change?
                )
                score.save()

            if row[17] != '':
                score = Score.objects.create(
                    task=project2,
                    student=student,
                    acquired_blood_cells=int(float(row[17])),
                    date=timezone.now()  # change?
                )
                score.save()

            group_itr += 1
            group_itr %= 14
