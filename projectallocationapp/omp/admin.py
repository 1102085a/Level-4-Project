from django.contrib import admin

from omp.models import User
from omp.models import Student
from omp.models import Supervisor
from omp.models import Administrator
from omp.models import Category
from omp.models import Project

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Supervisor)
admin.site.register(Administrator)
admin.site.register(Category)
admin.site.register(Project)
