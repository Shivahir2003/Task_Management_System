from django.urls import path

from taskmanager.views import ( 
    DashboardView,
    AddTaskView,
    EditTaskView,
    delete_task_view,
    complete_task,
    genarate_csv,
)

app_name='taskmanager'
urlpatterns = [
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('add/',AddTaskView.as_view(),name='add_task'),
    path('edit/<int:task_pk>/',EditTaskView.as_view(),name='edit_task'),
    path('delete/<int:task_pk>/',delete_task_view,name='delete_task'),
    path('complete/<int:task_pk>/',complete_task,name='complete_task'),
    path('generate-csv/tasks',genarate_csv,name='get_all_tasks'),
]