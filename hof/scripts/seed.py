import datetime
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth.models import Group as _Group
from django.contrib.auth.models import Permission, ContentType

from hof.models import Group, Student, TaskCollection, Task, Score
from hof.models import DayOfTheWeek


def run():
    # Clearance
    User.objects.filter(groups__name='Lecturer').delete()
    _Group.objects.filter(name='Lecturer').delete()
    Group.objects.all().delete()
    Student.objects.all().delete()
    TaskCollection.objects.all().delete()
    Task.objects.all().delete()
    Score.objects.all().delete()

    # Lecturers
    lecturer_group = _Group(name='Lecturer')
    lecturer_group.save()
    permissions = Permission.objects.filter(
        content_type__in=ContentType.objects.filter(app_label__contains='hof')
    )
    lecturer_group.permissions.add(*permissions)
    lecturer_group.save()

    lecturer1 = User.objects.create_user(
        username='mateusz',
        password='expass123',
        email='mateusz@example.com',
        first_name='Mateusz',
        last_name='Example',
        is_staff=True
    )
    lecturer_group.user_set.add(lecturer1)

    lecturer2 = User.objects.create_user(
        username='krzysiu',
        password='expass123',
        email='krzysiu@example.com',
        first_name='Krzysztof',
        last_name='Przystojniak',
        is_staff=True
    )
    lecturer_group.user_set.add(lecturer2)

    # Groups
    group1 = Group(year=2019, day_of_the_week=DayOfTheWeek.MONDAY, time=datetime.time(9, 35, 0), lecturer=lecturer1)
    group1.save()
    group2 = Group(year=2019, day_of_the_week=DayOfTheWeek.TUESDAY, time=datetime.time(11, 15, 0), lecturer=lecturer2)
    group2.save()
    group3 = Group(year=2019, day_of_the_week=DayOfTheWeek.WEDNESDAY, time=datetime.time(12, 50, 0), lecturer=lecturer2)
    group3.save()

    # TaskCollections
    task_collection = TaskCollection(description='Kartkówki')
    task_collection.save()

    # Tasks
    task1 = Task(task_collection=task_collection, max_blood_cells=1, description='Pierwsza Kartkówka')
    task1.save()
    task2 = Task(task_collection=task_collection, max_blood_cells=1, description='Druga Kartkówka')
    task2.save()

    # Students
    student1 = Student(group=group1, first_name="Tytus", last_name="Szyluk", nickname='Belmondo')
    student1.save()
    student2 = Student(group=group2, first_name="Andrzej", last_name="Piaseczny", nickname='Brzydż')
    student2.save()
    student3 = Student(group=group3, first_name="Barbara", last_name="Kurdej", nickname='Szatan')
    student3.save()

    # Score
    for s in [student1, student2, student3]:
        score = Score(task=task1, student=s, acquired_blood_cells=1, date=timezone.now())
        score.save()
        score = Score(task=task2, student=s, acquired_blood_cells=0, date=timezone.now())
        score.save()

