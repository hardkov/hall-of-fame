from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic

from .forms import UserLoginForm, UserRegisterForm

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from django.shortcuts import render

from .models import Group, Student, Score, Task, TaskCollection

# Create your views here.
def index(request):
    return render(request, 'hof/index.html')


# GROUP VIEWS
class GroupsView(generic.ListView):
    model = Group
    template_name = 'hof/groups/groups.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.order_by('-year', 'day_of_the_week', 'time').all()


class GroupView(generic.DetailView):
    model = Group
    template_name = 'hof/groups/group.html'


# STUDENT VIEWS
def students(request):
    # Since we are grouping the students by year
    years = Group.objects.order_by('-year').values_list('year', flat=True).distinct()
    students_by_year = []
    for year in years:
        students_by_year.append({
            'year': year,
            'students': Student.objects.filter(group__year=year).values('id', 'nickname')
        })
    students_total = len(Student.objects.all())
    context = {
        'students_by_year': students_by_year,
        'student_count': students_total
    }
    return render(request, 'hof/students/students.html', context)


class StudentView(generic.DetailView):
    model = Student
    template_name = 'hof/students/student.html'

    
# LOGIN VIEWS
def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)

        if next:
            return redirect(next)

        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "hof/accounts/login.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        nickname = form.cleaned_data.get('nickname')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)

        student = Student.objects.get(first_name=first_name,
                                      last_name=last_name,
                                      nickname=nickname)

        student.user = new_user
        student.save()

        if next:
            return redirect(next)

        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "hof/accounts/signup.html", context)


def logout_view(request):
    logout(request)

    return redirect('/')

  
# SCORE VIEWS
def scores(request):
    # Scores needs to be grouped
    tasks = []

    context = {
        'score_for_student': tasks,
    }
    return render(request, 'hof/score/scores.html', context)
