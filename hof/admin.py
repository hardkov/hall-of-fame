from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(TaskCollection)
admin.site.register(Task)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Score)
