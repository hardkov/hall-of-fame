from django.urls import path

from hof import views

app_name = 'hof'
urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test')
]
