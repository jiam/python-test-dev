from django.urls import path
from httpapitest import views

urlpatterns = [
    path('', views.index, name='index'),
    path('project/list', views.project_list, name='project_list'),
    path('project/add', views.project_add, name='project_add'),
    path('project/edit', views.project_edit, name='project_edit'),
    path('project/delete', views.project_delete, name='project_delete'),
    path('debugtalk/edit/<int:id>', views.debugtalk_edit, name='debugtalk_edit'),
]