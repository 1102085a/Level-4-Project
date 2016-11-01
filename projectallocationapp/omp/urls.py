from django.conf.urls import url
from omp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'adminpanel', views.adminpanel, name='adminpanel'),
    url(r'^dash_student/$', views.studentdash, name='studentdashboard'),
    url(r'^dash_supervisor/$', views.supervisordash, name='supervisordashboard'),
    url(r'^dash_admin/$', views.admindash, name='admindashboard'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^dash/projects/$', views.projects, name='projectlist'),
    url(r'^dash/categories/$', views.categories, name='categorylist'),
    url(r'^dash/add_category/$', views.add_category, name='add category'),

]