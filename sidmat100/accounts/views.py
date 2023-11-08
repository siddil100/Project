from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from .forms import CreateUserForm
from django.contrib import messages
from matrimony.models import PersonalDetails
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
            if user.is_superuser:
                login(request, user)
                request.session['suser'] = user.username  # Store the user's username in the 'suser' session

                # Retrieve the PersonalDetails instance for the superuser
                try:
                    personal_details = PersonalDetails.objects.get(user=user)
                    if personal_details.profile_image:
                        request.session['profile_image_url'] = personal_details.profile_image.url  # Store the profile image URL in the session
                except PersonalDetails.DoesNotExist:
                    request.session['profile_image_url'] = ''  # No PersonalDetails for the superuser
                
                return redirect('myadmin:myadmin')  # Redirect superuser to custom admin panel
            else:
                login(request, user)
                request.session['suser'] = user.username  # Store the user's username in the 'suser' session
                
                # Retrieve the PersonalDetails instance for the user
                try:
                    personal_details = PersonalDetails.objects.get(user=user)
                    if personal_details.profile_image:
                        request.session['profile_image_url'] = personal_details.profile_image.url  # Store the profile image URL in the session
                except PersonalDetails.DoesNotExist:
                    request.session['profile_image_url'] = ''  # No PersonalDetails for the user

                return redirect('matrimony:personaldetails')  # Redirect non-superusers to personaldetails
        else:
            messages.info(request, 'Username or Password is Incorrect')
    
    context = {}
    return render(request, 'accounts/login.html', context)

    

def logout_view(request):
    if 'suser' in request.session:
        del request.session['suser']  # Remove the "suser" session

    logout(request)
    return redirect('accounts:login')
