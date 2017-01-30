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
    url(r'^add_category/$', views.add_category, name='add category'),
    url(r'^add_project/$', views.add_project, name='add project'),
    url(r'^(?P<username>[\w\-]+)/admin/Supervisors/$', views.supervisor_list, name='supervisors'),
    url(r'^(?P<username>[\w\-]+)/admin/Students/$', views.student_list, name='students'),
    url(r'^(?P<username>[\w\-]+)/admin/Projects/$', views.project_list, name='projects'),
    url(r'^(?P<username>[\w\-]+)/admin/Categories/$', views.category_list, name='categories'),
    url(r'^(?P<username>[\w\-]+)/admin/Preferences/$', views.preference_list, name='preferences'),
]