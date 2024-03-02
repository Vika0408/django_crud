from django.shortcuts import render, redirect
from .froms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

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
            # return redirect('')
    context = {'form' : form}
    return render(request, 'crud/register.html', context=context)
