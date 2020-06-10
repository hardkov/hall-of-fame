from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import *
from .forms import AddMultipleScoreForm
from .filters import OwnGroupScoreFilter, OwnGroupStudentFilter

admin.site.site_header = 'Hall of Fame'


# inlines
class StudentInline(admin.TabularInline):
    model = Student
    extra = 5
    show_change_link = True
    readonly_fields = ('user',)


class TaskInline(admin.TabularInline):
    model = Task
    extra = 5
    show_change_link = True


class ScoreInline(admin.TabularInline):
    model = Score
    extra = 5
    show_change_link = True


# admins
class GroupAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'year', 'day_of_the_week', 'time', 'lecturer_link')
    list_editable = ('year', 'day_of_the_week', 'time')
    list_filter = ('year', 'day_of_the_week', 'lecturer')
    search_fields = ['year', 'day_of_the_week', 'lecturer__first_name', 'lecturer__last_name']

    inlines = [StudentInline]
    show_full_result_count = True

    def lecturer_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.lecturer.id])
        return format_html("<a href='{}'>{}</a>", url, obj.lecturer.__str__())

    def get_queryset(self, request):
        qs = super(GroupAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(lecturer=request.user)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return super(GroupAdmin, self).get_list_display(request)

        return '__str__', 'year', 'day_of_the_week', 'time', 'lecturer'

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return super(GroupAdmin, self).get_list_filter(request)

        return 'year', 'day_of_the_week'

    def get_search_fields(self, request):
        if request.user.is_superuser:
            return super(GroupAdmin, self).get_search_fields(request)

        return 'year', 'day_of_the_week'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'lecturer' and not request.user.is_superuser:
            kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
            kwargs['initial'] = request.user

        return super(GroupAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'first_name', 'last_name', 'group_link', 'total_score')
    list_editable = ('first_name', 'last_name')
    list_filter = (OwnGroupStudentFilter, 'group__year', 'group__day_of_the_week', 'group__lecturer')
    search_fields = (
        'nickname',
        'first_name',
        'last_name',
        'group__year',
        'group__day_of_the_week',
        'group__lecturer__first_name',
        'group__lecturer__last_name'
    )
    readonly_fields = ('user',)
    actions = ('add_multiple_score',)

    inlines = [ScoreInline]
    show_full_result_count = True

    def add_multiple_score(self, request, queryset):
        form = None

        if 'apply' in request.POST:
            form = AddMultipleScoreForm(request.POST)

            if form.is_valid():
                for student in queryset:
                    task = form.cleaned_data['task']
                    acquired_blood_cells = form.cleaned_data['acquired_blood_cells']

                    new_score = Score.objects.create(
                        task=task,
                        student=student,
                        acquired_blood_cells=acquired_blood_cells,
                        date=timezone.now()
                    )

                self.message_user(request,
                                  f'Added scores to {queryset.count()} students')

                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = AddMultipleScoreForm(initial={
                '_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        return render(request,
                      'admin/add_multiple_score.html',
                      {'form': form})

    def total_score(self, obj):
        total_score = 0

        for score in obj.score_set.all():
            total_score += score.acquired_blood_cells

        return total_score

    def group_link(self, obj):
        url = reverse('admin:hof_group_change', args=[obj.group.id])
        return format_html("<a href='{}'>{}</a>", url, obj.group.__str__())

    def get_queryset(self, request):
        queryset = super(StudentAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(group__lecturer=request.user)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return super(StudentAdmin, self).get_list_filter(request)

        return 'group__year', 'group__day_of_the_week', OwnGroupStudentFilter

    def get_search_fields(self, request):
        if request.user.is_superuser:
            return super(StudentAdmin, self).get_search_fields(request)

        return 'nickname', 'first_name', 'last_name', 'group__year', 'group__day_of_the_week'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'group' and not request.user.is_superuser:
            kwargs['queryset'] = Group.objects.filter(lecturer=request.user)

        return super(StudentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('score_details', 'task_link', 'student_link', 'acquired_blood_cells', 'date')
    list_editable = ['acquired_blood_cells']
    list_filter = [OwnGroupScoreFilter]
    search_fields = (
        'student__nickname',
        'student__first_name',
        'student__last_name',
        'task__description',
        'acquired_blood_cells',
        'date'
    )
    show_full_result_count = True

    def score_details(self, obj):
        return 'details'

    def student_link(self, obj):
        url = reverse('admin:hof_student_change', args=[obj.student.id])
        return format_html("<a href='{}'>{}</a>", url, obj.student.__str__())

    def task_link(self, obj):
        url = reverse('admin:hof_task_change', args=[obj.task.id])
        return format_html("<a href='{}'>{}</a>", url, obj.task.__str__())

    def get_queryset(self, request):
        qs = super(ScoreAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(student__group__lecturer=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student' and not request.user.is_superuser:
            kwargs['queryset'] = Student.objects.filter(group__lecturer=request.user)
            pass

        return super(ScoreAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class TaskCollectionAdmin(admin.ModelAdmin):
    search_fields = ['description']
    inlines = [TaskInline]
    show_full_result_count = True


class TaskAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'task_collection_link', 'max_blood_cells')
    list_editable = ['max_blood_cells']
    search_fields = ('task_collection__description', 'description', 'max_blood_cells')

    show_full_result_count = True

    def task_collection_link(self, obj):
        url = reverse('admin:hof_taskcollection_change', args=[obj.task_collection.id])
        return format_html("<a href='{}'>{}</a>", url, obj.task_collection.__str__())


admin.site.register(TaskCollection, TaskCollectionAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Score, ScoreAdmin)
