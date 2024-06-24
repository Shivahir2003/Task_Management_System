from django.urls import path

from taskmanager.views import ( 
    DashboardView,
    get_all_task_csv,
    TaskManagerView,
)

app_name='taskmanager'
urlpatterns = [
    path('', TaskManagerView.as_view(), name='task_manager'),
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('add/',TaskManagerView.as_view(),name='add_task'),
    path('edit/<int:task_pk>/',TaskManagerView.as_view(),name='edit_task'),
    path('delete/<int:task_pk>/',TaskManagerView.as_view(),name='delete_task'),
    path('complete/<int:task_pk>/',TaskManagerView.as_view(),name='complete_task'),
    path('get-all-task/',get_all_task_csv,name='get_all_tasks'),
    path('get-all-task/<int:user_pk>',get_all_task_csv,name='get_all_tasks'),
]