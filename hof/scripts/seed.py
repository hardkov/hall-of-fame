import datetime
from django.contrib.auth.models import User
from ..models import Group, Student, TaskCollection, Task, Score

def run():
    # Clearance
    Group.objects.filter().delete()
    Student.objects.filter().delete()
    TaskCollection.objects.filter().delete()
    Task.objects.filter().delete()
    Score.objects.filter().delete()

    # Groups
    group1 = Group(year=2019, day_of_the_week='Poniedziałek', time=datetime.time(9, 35, 0), lecturer='Krzysztof Przystojniak')
    group1.save()
    group2 = Group(year=2019, day_of_the_week='Wtorek', time=datetime.time(11, 15, 0), lecturer='Mateusz Tryhard')
    group2.save()
    group3 = Group(year=2019, day_of_the_week='Środa', time=datetime.time(12, 50, 0), lecturer='Domino Komino')
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
        score = Score(task=task1, student=s, acquired_blood_cells=1, date=datetime.datetime.now())
        score.save()
        score = Score(task=task2, student=s, acquired_blood_cells=0, date=datetime.datetime.now())
        score.save()

