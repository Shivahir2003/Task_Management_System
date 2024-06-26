import datetime
import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
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
        if self.request.user.is_superuser:
            context['task_list']=TaskManager.objects.all()
            context['users']=User.objects.all()
        else:
            user=User.objects.get(username=self.request.user.username)
            context['task_list']=user.taskmanager_set.all()
            context['task_completed']=user.taskmanager_set.filter(is_completed=True)
            context['task_expired']=user.taskmanager_set.filter(due_date__lte=timezone.now())
        return context


class TaskDetailsView(LoginRequiredMixin,TemplateView):
    """
            Show Task Details for logged in user
            
            Arguments:
                request (HttpRequest)
                task_pk
            
            Returns:
                In Get : render task detail page
    """
    template_name='taskmanager/task_details.html'
    def get_context_data(self,task_pk,**kwargs):
        context = super(TaskDetailsView, self).get_context_data(**kwargs)
        context['task']=TaskManager.objects.get(pk=task_pk)
        return context

class TaskManagerView(LoginRequiredMixin,View):
    """ All Task Manager operations"""

    def dispatch(self,request,*args,**kwargs):
        if request.path == reverse('taskmanager:add_task'):
            return self.add_task_view(request)
        elif '/task/edit/' in request.path:
            return self.edit_task_view(request,**kwargs)
        elif '/task/delete/' in request.path:
            return self.delete_task_view(request,**kwargs)
        elif '/task/complete/' in request.path:
            return self.complete_task(request,**kwargs)
        else:
            return redirect('taskmanager:dashboard')

    def add_task_view(self,request):
        """
            Add Task of logged in user
            
            Arguments:
                request (HttpRequest)
            
            Required Parameters:
                task,due_date
                
            Optional Parameters:
                task_description,star_date
            
            Returns:
                In Get : render add task page
                In Post : Redirect to Dashboard if task add succesfully 
        """
        try:
            user_list=User.objects.all()
            user=User.objects.get(pk=request.user.pk)
            if request.method =="GET":
                addtaskform=TaskForm()
            elif request.method =="POST":
                addtaskform=TaskForm(request.POST)
                if addtaskform.is_valid():
                    start_date=addtaskform.cleaned_data['start_date']
                    due_date=addtaskform.cleaned_data['due_date']
                    if user.is_superuser:
                        user_pk=request.POST.get('user')
                        user=User.objects.get(pk=user_pk)

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
                        messages.success(request,'Task has been added!')
                        return redirect('taskmanager:dashboard')
            context={
                'taskform':addtaskform,
                'user_list':user_list
                }
            return render(request,"taskmanager/add_edit_task.html",context)
        except User.DoesNotExist:
            return render(request,"error_404.html")

    def edit_task_view(self,request,task_pk):
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
                In Get: 
                    render add_edit_task.html with empty form
                In Post:
                    HttpResponseRedirect: dashboard.html with edited form if successful
                    re-render page with validatoin error
        """
        try:
            task= TaskManager.objects.get(pk=task_pk)
            if request.method == "GET":
                edittaskform=TaskForm(instance=task)
            elif request.method == "POST":
                edittaskform=TaskForm(request.POST,instance=task)
                if edittaskform.is_valid():
                    edit_task=edittaskform.save(commit=False)                    
                    edit_task.save()
                    messages.success(request,'Task has been Edited!')
                    return redirect('taskmanager:dashboard')
            context={
                'taskform':edittaskform,
                }
            return render(request,"taskmanager/add_edit_task.html",context)
        except TaskManager.DoesNotExist:
            return render(request,'error_404.html')

    def delete_task_view(self,request,task_pk):
        """
            Delete task form database
            
            Arguments:
                request (HttpRequest),
                task_pk
            
            delete task of given primary key
        """
        try:
            TaskManager.objects.get(pk=task_pk).delete()
            messages.success(request,'Task has been deleted!')
            return redirect('taskmanager:dashboard')
        except TaskManager.DoesNotExist:
            return render(request,'error_404.html')

    def complete_task(self,request,task_pk):
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
def get_all_task_csv(request,**kwargs):
    """
        Genarate CSV of all Tasks of loggedin user
        
        Arguments:
            request (HttpRequest),
            
        Returns:
            Httpresponse: Csv file 
        
    """
    # Create the HttpResponse object with the appropriate CSV header.
    filename=f"all_task_list_{request.user.username}.csv"
    headers={"Content-Disposition": f'attachment; filename={filename}'}
    response = HttpResponse(
        content_type="text/csv",
        headers=headers,
    )
    try:
        if request.user.is_superuser:
            tasks=TaskManager.objects.filter(user=kwargs['user_pk'])
        else:
            tasks=TaskManager.objects.filter(user=request.user)
        writer = csv.writer(response)
        writer.writerow(['Task', 'Task_description','Status' ,'Start_date', 'Due_date', 'Created'])
        for task in tasks:
            if task.is_completed == True:
                status = 'Completed'
            else:
                status = 'Incomplete'
            writer.writerow([task.task, task.task_description,status, task.start_date.strftime("%d/%m/%Y"), task.due_date.strftime("%d/%m/%Y"), task.created.strftime("%d/%m/%Y")])
        return response
    except TaskManager.DoesNotExist:
        return render(request,'error_404.html')
