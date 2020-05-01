from django.contrib import admin, auth

from .models import *


admin.site.site_header = 'HOFFMAN'


class StudentInline(admin.TabularInline):
    model = Student
    extra = 5


class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'year', 'day_of_the_week', 'time', 'lecturer')
    list_editable = ('year', 'day_of_the_week', 'time', 'lecturer')
    list_filter = ('year', 'day_of_the_week', 'lecturer')
    search_fields = ['year', 'day_of_the_week']
    inlines = [StudentInline]

    def group_name(self, obj):
        return obj.__str__()


admin.site.register(TaskCollection)
admin.site.register(Task)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student)
admin.site.register(Score)
