from django.utils import timezone
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
    
    def clean(self):
        form_data = self.cleaned_data
        start_date = form_data['start_date']
        due_date =form_data['due_date']

        if not start_date and due_date < timezone.now():
            self.add_error('due_date','due date must be greater than start date')
        elif start_date and due_date < start_date :
            self.add_error('due_date','due date must be greater than start date')
        
        return form_data