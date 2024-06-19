from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from taskmanager.models import TaskManager



from accounts.models import UserProfile

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model=UserProfile
    classes=["collapse"]


class TaskManagerInline(admin.StackedInline):
    model = TaskManager
    extra=1


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """ Customize UserProfile """

    fieldsets = [
        ("username",{"fields": ["user"]}),
        ("Profile Details",{"fields": ["mobile_number","user_image"]}),
    ]
    list_display = ["id","user", "mobile_number", "user_image"]
    list_filter = ["id","user"]
    list_display_links=["user"]


@admin.register(User)
class UserFiels(UserAdmin):
    """ adding userprofile and task to useradmin"""
    list_display=['id','username','email','first_name']
    list_display_links=["username"]

    inlines=[UserProfileInline]
    inlines=[TaskManagerInline]
