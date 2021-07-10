from django.urls import path
from httpapitest import views

urlpatterns = [
    path('', views.index, name='index'),
    path('project/list', views.project_list, name='project_list'),
    path('project/add', views.project_add, name='project_add'),
    path('project/edit', views.project_edit, name='project_edit'),
    path('project/delete', views.project_delete, name='project_delete'),
    path('debugtalk/edit/<int:id>', views.debugtalk_edit, name='debugtalk_edit'),
    path('module/list', views.module_list, name='module_list'),
    path('module/add', views.module_add, name='module_add'),
    path('module/edit', views.module_edit, name='module_edit'),
    path('module/delete', views.module_delete, name='module_delete'),
    path('module/search/ajax', views.module_search_ajax, name='module_search_ajax'),
    path('case/add', views.case_add, name='case_add'),
    path('case/search/ajax', views.case_search_ajax, name='case_search_ajax'),
    path('case/edit/<int:id>', views.case_edit, name='case_edit'),
    path('case/list', views.case_list, name='case_list'),
    path('case/delete', views.case_delete, name='case_delete'),
    path('case/copy', views.case_copy, name='case_copy'),
    path('test/test_run', views.test_run, name='test_run'),
    path('test/test_batch_run', views.test_batch_run, name='test_batch_run'),
    path('report/list', views.report_list, name='report_list'),
    path('report/delete', views.report_delete, name='report_delete'),
    path('report/view/<int:id>', views.report_view, name='report_view'),
]