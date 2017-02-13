import random
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectallocationapp.settings')

import django
django.setup()
from omp.models import User, Project, Student, PrefListEntry


'''
General algorithm outline:

    Select students randomly
    Assign project to first in list
    If taken, give second, third, etc
        - Any students without five preferences thrown out

'''


def greedy_assignment():
    students_list = Student.objects.all()

    # O(N) Random selection
    size = len(students_list)
    while size:
        index = random.randrange(size)
        student = students_list[index]
        students_list[index] = students_list[size - 1]
        size -= 1
        process(student)


def process(student):
    studentprefs = PrefListEntry.objects.filter(Student)
    if len(studentprefs) < 5:
        return;
    pref = studentprefs[0]
    student.project = pref.project
    student.save()
    print(student.user.username + " assigned project: " + pref.project.name)

