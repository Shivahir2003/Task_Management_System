import datetime
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils import timezone
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
                filtered contex data if get task name,
                all context data if task name not provided
            
        """
        context = super(DashboardView, self).get_context_data(**kwargs)
        user=User.objects.get(username=self.request.user.username)
        # getting task name from search 
        if self.request.GET and self.request.GET['query']:
            task_title = self.request.GET['query']
            context['task_list']=user.taskmanager_set.filter(task__icontains=task_title)
            context['query']=task_title
        else:   
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
                start_date=addtaskform.cleaned_data['start_date']
                due_date=addtaskform.cleaned_data['due_date']
                #  Saving addtaskform
                task=addtaskform.save(commit=False)
                task.user=user
                # adding start Date if start_date is not given
                if start_date is None:
                    start_date=datetime.datetime.now()
                    task.start_date=start_date
                if due_date < timezone.now():
                    addtaskform.add_error('due_date','due date can not to be before today')
                else:
                    task.save()
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
            edittaskform=TaskForm(request.POST,instance=task_obj)
            if edittaskform.is_valid():
                edit_task=edittaskform.save(commit=False)
                edit_task.save()
                return redirect('taskmanager:dashboard')
            return render(request,"taskmanager/add_edit_task.html",{'taskform':edittaskform})
        except TaskManager.DoesNotExist:
            return render(request,'error_404.html')


@login_required()
def delete_task_view(request,task_pk):
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
def complete_task(request,task_pk):
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

@login_required()
def genarate_csv(request):
    """
        Genarate CSV of all Tasks of loggedin user
        
        Arguments:
            request (HttpRequest),
            
        Returns:
            Httpresponse: Csv file 
        
    """
    # Create the HttpResponse object with the appropriate CSV header.
    filename=f"all_task_list_{request.user.username}.csv"
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename={filename}'},
    )
    try:
        tasks=TaskManager.objects.filter(user=request.user)
        writer = csv.writer(response)
        writer.writerow(['task', 'task_description', 'start_date', 'due_date', 'created'])
        for task in tasks:
            writer.writerow([task.task, task.task_description, task.start_date.strftime("%d/%m/%Y, %l:%M:%S %p"), task.due_date.strftime("%d/%m/%Y, %l:%M:%S %p"), task.created.strftime("%d/%m/%Y, %l:%M:%S %p")])
        return response
    except TaskManager.DoesNotExist:
        return render(request,'error_404.html')
