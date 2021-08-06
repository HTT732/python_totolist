from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import CreateUserForm, TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'task.html')

def login_form(request):
    if request.user.is_authenticated:
        return redirect('task')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task')
            else:
                messages.info(request, "Username or password is incorrect!")
    return render(request, 'login/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')
    
def register_form(request):
    if request.user.is_authenticated:
        return redirect('task')
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for \"" + user + "\"") 
                return redirect('login')

    context = {'form':form}
    return render(request, 'login/register.html', context)

@login_required(login_url='login')
def task_page(request):
    tasks = Task.objects.filter(user_id=request.user.id)
    status = Status.objects.all()
    context = {'tasks':tasks, 'status':status}

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "1 task was created!")
            return redirect('task')
        context['form'] = form
    
    return render(request, 'task.html', context)

@login_required(login_url='login')
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    status = Status.objects.all()
    context = {'task':task, 'status':status}
    
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task.title = request.POST.get('title')
            task.start_day = request.POST.get('start_day')
            task.end_day = request.POST.get('end_day')
            task.status_id = request.POST.get('status')
            context['form'] = form
            task.save()
            
            messages.info(request, "\"" + task.title + "\" was updated!")
            return redirect('task')
    return render(request, 'edit.html', context)

@login_required(login_url='login')
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.info(request, "\"" + task.title + "\" was deleted!")
    return redirect('task')
    
@login_required(login_url='login')
def calendar_page(request):
    tasks = Task.objects.filter(user_id=request.user.id)
    return render(request, 'calendar.html', {'tasks':tasks})
