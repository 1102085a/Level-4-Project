from django.conf.urls import url
from omp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'adminpanel', views.adminpanel, name='adminpanel'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^dashboard/(?P<username>[\w\-]+)/$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='show category'),
    url(r'^/(?P<project_name_slug>[\w\-]+)$', views.project, name='show project'),
    url(r'^add_category/$', views.add_category, name='add category'),
    url(r'^add_project/$', views.add_project, name='add project'),

]