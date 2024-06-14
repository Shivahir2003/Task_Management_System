import datetime
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic.base import View,TemplateView

from taskmanager.models import TaskManager
from taskmanager.forms import TaskForm

# Create your views here.


class DashboardView(LoginRequiredMixin,TemplateView):
    """
        show All Task of logged in user
        
        Return:
           in Get: render dashboard.html with all task_list
    """
    template_name='taskmanager/dashboard.html'

    def get_context_data(self,**kwargs):
        """
            get all task of user and return to template
            
            Arguments:
            request (HttpRequest)
            
            Returns:
                context data of all tasks 
            
        """
        context = super(DashboardView, self).get_context_data(**kwargs)
        user=User.objects.get(username=self.request.user.username)
        context['task_list']=user.taskmanager_set.all()
        return context


class AddTaskView(LoginRequiredMixin,View):
    """
        Add Task View
    """
    def get(self,request):
        """
            Add Task get method
            
            Arguments:
                request (HttpRequest)
            
            Returns:
                render add_edit_task.html with empty form
        """
        addtaskform=TaskForm()
        return render(request,"taskmanager/add_edit_task.html",{'taskform':addtaskform})

    def post(self,request):
        """
            Add Task post method
            
            Arguments:
                request (HttpRequest)
            
            Required Parameters:
                task,due_date
                
            Optional Parameters:
                task_description,star_date
            
            Returns:
                HttpResponseRedirect: dashboard.html if successful
                re-render page with validatoin error
        """
        try:
            user=User.objects.get(pk=request.user.pk)
            addtaskform=TaskForm(request.POST)
            if addtaskform.is_valid():
                task_data=addtaskform.cleaned_data
                task=task_data['task']
                task_description=task_data['task_description']
                start_date=task_data['start_date']
                due_date=task_data['due_date']
                if start_date is None:
                    start_date=datetime.datetime.now()
                TaskManager.objects.create(
                    user=user,
                    task=task,
                    task_description=task_description,
                    start_date=start_date,
                    due_date=due_date   
                )
                
                return redirect('taskmanager:dashboard')
            return render(request,"taskmanager/add_edit_task.html",{'taskform':addtaskform})
        except User.DoesNotExist:
            return render(request,"error_404.html")


class EditTaskView(LoginRequiredMixin,View):
    """
        Edit Task View
    """
    def get(self,request,task_pk):
        """
            Edit Task get method
            
            Arguments:
                request (HttpRequest)
                task_pk
            
            Returns:
                render add_edit_task.html with empty form
        """
        try:
            task= TaskManager.objects.get(pk=task_pk)
            edittaskform=TaskForm(instance=task)
            return render(request,"taskmanager/add_edit_task.html",{'taskform':edittaskform})
        except TaskManager.DoesNotExist:
            return render(request,'error_404.html')

    def post(self,request,task_pk):
        """
            Edit Task post method
            
            Arguments:
                request (HttpRequest)
                task_pk
            
            Required Parameters:
                task,due_date
                
            Optional Parameters:
                task_description,star_date

            Returns:
                HttpResponseRedirect: dashboard.html with edited form if successful
                re-render page with validatoin error
        """
        try:
            task_obj= TaskManager.objects.get(pk=task_pk)
            edittaskform=TaskForm(request.POST)
            if edittaskform.is_valid():
                task_data=edittaskform.cleaned_data
                task=task_data['task']
                task_description=task_data['task_description']
                start_date=task_data['start_date']
                due_date=task_data['due_date']

                task_obj.task=task
                task_obj.task_description=task_description
                task_obj.start_date=start_date
                task_obj.due_date=due_date
                task_obj.save()
                return redirect('taskmanager:dashboard')
            return render(request,"taskmanager/add_edit_task.html",{'taskform':edittaskform})
        except TaskManager.DoesNotExist:
            return render(request,'error_404.html')


@login_required()
def deletetaskview(request,task_pk):
    """
        Delete task form database
        
        Arguments:
            request (HttpRequest),
            task_pk
        
        delete task of given primary key
    """
    try:
        TaskManager.objects.get(pk=task_pk).delete()
        return redirect('taskmanager:dashboard')
    except TaskManager.DoesNotExist:
        return render(request,'error_404.html')

@login_required()
def completetask(request,task_pk):
    """
        toggle is_completed field
        
        Arguments:
            request (HttpRequest),
            task_pk
        
        check if is_completed field and set toggle
            set True if Task is not completed else False for reset task
    """
    try:
        task=TaskManager.objects.get(pk=task_pk)
        if task.is_completed:
            task.is_completed=False
        else:
            task.is_completed=True
        task.save()
        return redirect('taskmanager:dashboard')
    except TaskManager.DoesNotExist:
        return render(request,'error_404.html')


def genarate_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="alltasks.csv"'},
    )
    tasks=TaskManager.objects.all()
    writer = csv.writer(response)
    writer.writerow(['task', 'task_description', 'start_date', 'due_date', 'created'])
    for task in tasks:
        print(task)
        writer.writerow([task.task, task.task_description, task.start_date.strftime("%Y-%m-%d, %H:%M:%S"), task.due_date.strftime("%Y-%m-%d, %H:%M:%S"), task.created.strftime("%Y-%m-%d, %H:%M:%S")])

    return response