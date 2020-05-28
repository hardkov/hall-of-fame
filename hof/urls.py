from django.urls import path

from hof import views

app_name = 'hof'
urlpatterns = [
    path('', views.index, name='index'),
    # GROUPS
    path('groups/', views.GroupsView.as_view(), name='groups'),
    path('groups/<int:pk>', views.GroupView.as_view(), name='group'),
    # STUDENTS
    path('students/', views.students, name='students'),
    path('student/<int:pk>', views.StudentView.as_view(), name='student'),
    # SCORE
    path('scores/', views.scores, name='scores'),

]
