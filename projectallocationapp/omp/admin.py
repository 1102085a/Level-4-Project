from django.contrib import admin
from omp.models import User, Student, Supervisor, Administrator, Category, Project, PrefListEntry, SiteConfiguration


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('id',)}

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('id',)}

class StudentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'id':('user',)}

class SupervisorAdmin(admin.ModelAdmin):
    class StudentAdmin(admin.ModelAdmin):
        prepopulated_fields = {'id': ('user',)}

# Update the registration to include this customised interface

admin.site.register(Supervisor, SupervisorAdmin)
admin.site.register(Administrator)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(PrefListEntry)
admin.site.register(SiteConfiguration)




