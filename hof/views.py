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
class StudentsView(generic.ListView):
    model = Student
    template_name = 'hof/students/students.html'
    context_object_name = 'students'


class StudentView(generic.DetailView):
    model = Student
    template_name = 'hof/students/student.html'