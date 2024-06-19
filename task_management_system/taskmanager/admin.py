from django.contrib import admin

from taskmanager.models import TaskManager


@admin.register(TaskManager)
class TaskManagerAdmin(admin.ModelAdmin):
    """ Customize Taskmanger """
    fieldsets=[
        ("Task manager",{
            "fields": ['task','task_description','is_completed','start_date','due_date']
            }),
        ]
    list_display=['id','user','task','start_date','due_date','is_completed']
    list_display_links=['task']
    search_fields = ["task",'user__username']
    list_filter=['user','start_date','due_date','is_completed']
