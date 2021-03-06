from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm, UserRegisterForm, EditProfileForm
from .models import Group, Student, Score


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
    next_url = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)

        if next_url:
            return redirect(next_url)

        return redirect('/')

    context = {
        'form': form,
    }

    return render(request, "hof/accounts/login.html", context)


def register_view(request):
    next_url = request.GET.get('next')
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

        if next_url:
            return redirect(next_url)

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
    students = Student.objects.all()
    scores = Score.objects.all()
    query = {}
    for student in students:
        query[student] = 0
        for score in scores:
            if score.student == student:
                query[student] += int(score.acquired_blood_cells)

    query = sorted(query.items(), key=lambda x: x[1], reverse=True)

    context = {
        'query': query
    }
    return render(request, 'hof/score/scores.html', context)


# PROFILE VIEW

def profile(request):
    student = Student.objects.filter(user__id=request.user.id)

    context = {
        'user': request.user,
        'student': student
    }

    return render(request, 'hof/accounts/profile.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EditProfileForm(instance=request.user)
        context = {
            'form': form,
        }
        return render(request, 'hof/accounts/edit.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/')
        else:
            return redirect('/profile/password')

    else:
        form = PasswordChangeForm(user=request.user)
        context = {
            'form': form,
        }
        return render(request, 'hof/accounts/change_password.html', context)