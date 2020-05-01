from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Group, Student


# Create your views here.
def index(request):
    return render(request, 'hof/index.html')


# GROUP VIEWS
class GroupsView(generic.ListView):
    model = Group
    template_name = 'hof/groups/groups.html'
    context_object_name = 'groups'


class GroupView(generic.DetailView):
    model = Group
    template_name = 'hof/groups/group.html'


# STUDENT VIEWS
def students(request):
    # Since we are grouping the students by year
    years = Group.objects.order_by('-year').values_list('year', flat=True).distinct()
    students_by_year = {}
    for year in years:
        students_by_year[year] = {
            'students': Student.objects.filter(group__year=year),
            'count': len(Student.objects.filter(group__year=year))
        }
    students_total = len(Student.objects.all())
    context = {
        'years': years,
        'students_by_year': students_by_year,
        'student_count': students_total
    }
    return render(request, 'hof/students/students.html', context)


class StudentView(generic.DetailView):
    model = Student
    template_name = 'hof/students/student.html'
