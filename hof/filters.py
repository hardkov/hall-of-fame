from .models import Group
from django.contrib import admin


class OwnGroupStudentFilter(admin.SimpleListFilter):
    title = 'group'
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        lookups = []

        if request.user.is_superuser:
            group_set = Group.objects.all()
        else:
            group_set = request.user.group_set.all()

        for group in group_set:
            lookups.append((group.id, group.__str__()))

        return lookups

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(group=self.value())


class OwnGroupScoreFilter(admin.SimpleListFilter):
    title = 'group'

    parameter_name = 'student__group'

    def lookups(self, request, model_admin):
        lookups = []

        if request.user.is_superuser:
            group_set = Group.objects.all()
        else:
            group_set = request.user.group_set.all()

        for group in group_set:
            lookups.append((group.id, group.__str__()))

        return lookups

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(student__group=self.value())
