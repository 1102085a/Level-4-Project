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

processlist = {}

def greedyAssignment():
    students_list = Student.objects.all()

    # O(N) Random selection
    size = len(students_list)
    while size:
        index = random.randrange(size)
        student = students_list[index]
        students_list[index] = students_list[size - 1]
        size -= 1
        process(student)
    return processlist


def process(student):
    studentprefs = PrefListEntry.objects.filter(Student)
    if len(studentprefs) < 5:
        student.project = None
    for pref in studentprefs:
        project = pref.project
        supervisor = project.supervisor
        if project.assigned:
            student.project = None
        elif supervisor.capacity == supervisor.assigned:
            student.project = None
        else:
            student.project = project
            supervisor.assigned += 1
            student.save()
            supervisor.save()
    processlist[student.user.username] = student.project.name


