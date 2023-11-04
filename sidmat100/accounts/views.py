from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('accounts:login')
    else:
        form = UserCreationForm()
    
    return render (request, 'accounts/register.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():

            user = form.get_user()
            login (request, user)
            request.session['suser'] = user.username
            return redirect ('matrimony:profile_list_loghome')
    else:
        form = AuthenticationForm()
    
    return render (request, 'accounts/login.html', {'form':form})

def logout_view(request):
    
    if 'suser' in request.session:
        del request.session['suser']

    logout(request)
    return redirect('accounts:login')