from django.conf.urls import url
from omp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^(?P<username>[\w\-]+)/dashboard/$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='show category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/project/(?P<project_name_slug>[\w\-]+)$',
        views.project, name='show project'),
    url(r'^create_category/$', views.add_category, name='add category'),
    url(r'^create_project/$', views.add_project, name='add project'),
    url(r'^create_student/$', views.add_student, name='add student'),
    url(r'^create_supervisor/$', views.add_supervisor, name='add supervisor'),
    url(r'^create_administrator/$', views.add_admin, name='add admin'),
    url(r'^create_preference/$', views.add_preference, name='add preference'),
    url(r'^(?P<username>[\w\-]+)/admin/supervisors/$', views.supervisor_list, name='supervisors'),
    url(r'^(?P<username>[\w\-]+)/admin/students/$', views.student_list, name='students'),
    url(r'^(?P<username>[\w\-]+)/admin/administrators/$', views.admin_list, name='administrators'),
    url(r'^(?P<username>[\w\-]+)/admin/projects/$', views.project_list, name='projects'),
    url(r'^(?P<username>[\w\-]+)/admin/categories/$', views.category_list, name='categories'),
    url(r'^(?P<username>[\w\-]+)/admin/preferences/$', views.preference_list, name='preferences'),
    url(r'^(?P<username>[\w\-]+)/admin/edit/cat/(?P<category_name_slug>[\w\-]+)/$', views.edit_category, name='edit category'),
    url(r'^(?P<username>[\w\-]+)/admin/edit/pro/(?P<project_name_slug>[\w\-]+)/$', views.edit_project, name='edit project'),
    url(r'^(?P<username>[\w\-]+)/admin/edit/stu/(?P<student_name>[\w\-]+)/$', views.edit_student, name='edit student'),
    url(r'^(?P<username>[\w\-]+)/admin/edit/sup/(?P<supervisor_name>[\w\-]+)/$', views.edit_supervisor, name='edit supervisor'),
]