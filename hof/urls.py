from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
)
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

    # LOGIN
    path('login/', views.login_view),
    path('signup/', views.register_view),
    path('logout/', views.logout_view),

    # SCORE
    path('scores/', views.scores, name='scores'),

    # PROFILE
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit, name='edit'),

    # PASSWORD
    path('profile/password/', views.change_password, name='change_password'),
    ##
    # path('profile/reset-password/', PasswordResetView.as_view(), name='password_reset'),
    # path('profile/reset-password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path(r'^profile/reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    #     PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    ##
]
