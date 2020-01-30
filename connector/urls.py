from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_index, name='index'),

    path('projects/', views.view_projects, name='projects'),
    path('project/create/', views.view_project_create, name='project_create'),
    path('project/<int:id_project>/', views.view_project, name='project'),

    path('project/<int:id_project>/servers', views.view_servers, name='servers'),
    path('project/<int:id_project>/server/<int:id_server>', views.view_server,
    name='server'),
]
