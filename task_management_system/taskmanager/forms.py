from django import forms

from taskmanager.models import TaskManager

class TaskForm(forms.ModelForm):
    """
        Add or Edit Task Form
    """
    task=forms.CharField(max_length=200,required=True)
    task_description=forms.CharField(max_length=500,required=False,widget=forms.Textarea())
    start_date=forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
            },
        )
    )
    due_date=forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local'
            }
        )
    )


    class Meta:
        model=TaskManager
        exclude=['is_completed','user']
