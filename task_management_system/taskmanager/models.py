from datetime import datetime
from django.db import models

from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel
from ckeditor.fields import RichTextField


class TaskManager(TimeStampedModel):
    """
        Task manager model
        
        Extends:
            TimeStampedModel
        
        Create task for user
    """
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    task=models.CharField(max_length=200)
    task_description = RichTextField(null=True,blank=True)
    is_completed=models.BooleanField(default=False)
    start_date=models.DateTimeField(default=datetime.now)
    due_date=models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.user} -- {self.task}"
