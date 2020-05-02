from django.contrib.auth.models import User
from django.contrib.auth.models import Group as _Group
from django.contrib.auth.models import Permission, ContentType


def wipe_lecturers():
    User.objects.filter(groups__name='Lecturer').delete()
    _Group.objects.filter(name='Lecturer').delete()


def create_lecturers_group():
    lecturer_group = _Group(name='Lecturer')
    lecturer_group.save()
    permissions = Permission.objects.filter(
        content_type__in=ContentType.objects.filter(app_label__contains='hof')
    )
    lecturer_group.permissions.add(*permissions)
    lecturer_group.save()
    return lecturer_group
