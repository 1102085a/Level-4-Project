from django.conf.urls import url
from omp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'adminpanel', views.adminpanel, name='adminpanel'),
    url(r'^dash/$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.login, name='login'),
    url(r'^dash/projects/$', views.projects, name='projectlist'),
    url(r'^dash/categories/$', views.categories, name='categorylist'),
    url(r'^(?P<user_id_slug>[\w]+)/$', views.show_user, name='show_user'),

]