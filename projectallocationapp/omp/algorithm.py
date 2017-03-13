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
    students_list = list(Student.objects.all())

    # O(N) Random selection
    size = len(students_list)
    while size:
        index = random.randrange(size)
        student = students_list[index]
        students_list[index] = students_list[size - 1]
        size -= 1
        print("Processing " + student.user.username)
        process(student)
    return processlist


def process(student):
    studentprefs = PrefListEntry.objects.filter(student=student)
    if len(studentprefs) < 5:
        student.project = None
        print("Less than five projects.")
    else:
        for pref in studentprefs:
            project = pref.project
            supervisor = project.supervisor
            if project.assigned:
                student.project = None
                print("Project Already Assigned.")
            elif supervisor.capacity == supervisor.assigned:
                student.project = None
                print("Supervisor at Capacity")
            else:
                student.project = project
                supervisor.assigned += 1
                student.save()
                supervisor.save()
                print("Project Assigned: " + project.name)
                break

    print("DONE.")
    if student.project is None:
        processlist[student.user.username] = None
    else:
        processlist[student.user.username] = student.project.name


