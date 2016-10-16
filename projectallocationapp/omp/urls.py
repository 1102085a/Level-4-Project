from django.conf.urls import url
from omp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'adminpanel', views.adminpanel, name='adminpanel'),
    url(r'^dash/', views.dashboard, name='dashboard').
    url(r'^dash/projects', views.projects, name='projectlist')
]