from django.contrib import admin, auth
from django.urls import reverse
from django.utils.html import format_html

from .models import *


admin.site.site_header = 'HOFFMAN'


class StudentInline(admin.TabularInline):
    model = Student
    extra = 5
    show_change_link = True

class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'year', 'day_of_the_week', 'time', 'lecturer')
    list_editable = ('year', 'day_of_the_week', 'time', 'lecturer')
    list_filter = ('year', 'day_of_the_week', 'lecturer')
    search_fields = ['year', 'day_of_the_week']
    inlines = [StudentInline]

    def group_name(self, obj):
        return obj.__str__()


class ScoreInline(admin.TabularInline):
    model = Score
    extra = 5
    show_change_link = True


class StudentAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'first_name', 'last_name', 'group_link')
    list_editable = ('first_name', 'last_name')
    list_filter = ['group']
    search_fields = ('nickname', 'first_name', 'last_name')
    inlines = [ScoreInline]

    def task_collection_link(self, obj):
        url = reverse('admin:hof_taskcollection_change', args=[obj.task_collection.id])
        return format_html("<a href='{}'>{}</a>", url, obj.task_collection.__str__())

    def group_link(self, obj):
        url = reverse('admin:hof_group_change', args=[obj.group.id])
        return format_html("<a href='{}'>{}</a>", url, obj.group.__str__())


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('score', 'task_link', 'student_link', 'acquired_blood_cells', 'date')
    list_editable = ['acquired_blood_cells']
    search_fields = (
        'student__nickname',
        'student__first_name',
        'student__last_name',
        'task__description',
        'acquired_blood_cells',
        'date'
    )

    def score(self, obj):
        return 'details'

    def student_link(self, obj):
        url = reverse('admin:hof_student_change', args=[obj.student.id])
        return format_html("<a href='{}'>{}</a>", url, obj.student.__str__())

    def task_link(self, obj):
        url = reverse('admin:hof_task_change', args=[obj.task.id])
        return format_html("<a href='{}'>{}</a>", url, obj.task.__str__())


class TaskInline(admin.TabularInline):
    model = Task
    extra = 5
    show_change_link = True

class TaskCollectionAdmin(admin.ModelAdmin):
    search_fields = ['description']
    inlines = [TaskInline]


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'task_collection_link', 'max_blood_cells')
    list_editable = ['max_blood_cells']
    search_fields = ('task_collection__description', 'description', 'max_blood_cells')

    def task_collection_link(self, obj):
        url = reverse('admin:hof_taskcollection_change', args=[obj.task_collection.id])
        return format_html("<a href='{}'>{}</a>", url, obj.task_collection.__str__())

    def task_name(self, obj):
        return obj.__str__()


admin.site.register(TaskCollection, TaskCollectionAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Score, ScoreAdmin)
