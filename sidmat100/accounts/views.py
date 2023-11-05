from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from .forms import CreateUserForm
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            m = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for: ' + m)
           
            return redirect ('accounts:login')
        
    else:
        form = CreateUserForm()
    
    return render (request, 'accounts/register.html', {'form':form})

from django.contrib.sessions.models import Session

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['suser'] = user.username  # Store the user's username in the 'suser' session
            return redirect('matrimony:personaldetails')
        else:
            messages.info(request, 'Username or Password is Incorrect')
    
    context = {}
    return render(request, 'accounts/login.html', context)

    

def logout_view(request):
    if 'suser' in request.session:
        del request.session['suser']  # Remove the "suser" session

    logout(request)
    return redirect('accounts:login')
