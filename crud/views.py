from django.shortcuts import render, redirect
from .froms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Record
from django.contrib import messages


# Create your views here.

def home(request):
    # return HttpResponse('Hello world!')
    return render(request, 'crud/index.html')


# Register a user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("my-login")
    context = {'form': form}
    return render(request, 'crud/register.html', context=context)


def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, "You have logged in!")
                return redirect("dashboard")

    context = {'form': form}
    return render(request, 'crud/my-login.html', context=context)


# - Dashboard
@login_required(login_url='my-login')
def dashboard(request):
    my_records = Record.objects.all()
    context = {'records': my_records}
    return render(request, 'crud/dashboard.html', context=context)


# - Create a record

@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record created successfully!")
            return redirect("dashboard")

    context = {'form': form}
    return render(request, 'crud/create-record.html', context=context)


@login_required(login_url='my-login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully!")
            return redirect("dashboard")

    context = {'form': form}
    return render(request, 'crud/update-record.html', context=context)


# - view a record

@login_required(login_url='my-login')
def singular_record(request, pk):
    all_records = Record.objects.get(id=pk)
    context = {'record': all_records}
    return render(request, 'crud/view-record.html', context=context)


# - delete a record

@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "Record deleted!")
    return redirect("dashboard")


def user_logout(request):
    auth.logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("my-login")
