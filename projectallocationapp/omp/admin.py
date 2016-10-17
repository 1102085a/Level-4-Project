from django.contrib import admin

from omp.models import UserProfile
from omp.models import Student
from omp.models import Supervisor
from omp.models import Administrator
from omp.models import Category
from omp.models import Project

# Add in this class to customise the Admin Interface
#class UserAdmin(admin.ModelAdmin):
    #prepopulated_fields = {'slug':('username',)}

# Update the registration to include this customised interface
admin.site.register(UserProfile)
admin.site.register(Student)
admin.site.register(Supervisor)
admin.site.register(Administrator)
admin.site.register(Category)
admin.site.register(Project)
