from django.test import TestCase

# Create your tests here.
from .models import Task
from .models import TaskCollection
from .models import Student
from .models import Score
from .models import Group


class StudentTest(TestCase):

    def test_student_sth(self):
        self.assert_(1, 1)
