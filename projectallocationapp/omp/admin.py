from django.contrib import admin
from django.contrib.auth.models import User

from omp.models import User, Student, Supervisor, Administrator, Category, Project, Preferences

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('id',)}

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('id',)}

# Update the registration to include this customised interface

admin.site.register(Student)
admin.site.register(Supervisor)
admin.site.register(Administrator)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Preferences)
