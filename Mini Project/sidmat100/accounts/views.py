from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from .forms import CreateUserForm
from django.contrib import messages
from matrimony.models import PersonalDetails
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            m = form.cleaned_data.get('username')
            mymail = form.cleaned_data.get('email')
            subject = 'Registration Confirmation'
            message = f'Welcome to DreamWed - Your Journey of Love Begins Here! 🎉 Congratulations on Registering with Us, {m}! Explore a World of Love, Hope, and New Beginnings. ❤️🥂'

            from_email = 'your-email@example.com'  # Replace with your email
            recipient_list = [mymail]  # Use the user's email
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
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
                 
                
                return redirect('myadmin:myadmin')  # Redirect superuser to custom admin panel
            else:
                login(request, user)
                request.session['suser'] = user.username  # Store the user's username in the 'suser' session
                
                # Retrieve the PersonalDetails instance for the user
                try:
                    personal_details = PersonalDetails.objects.get(user=user)
                    if personal_details.aadhar_valid:
                        # If aadhar_valid is True, redirect to personal details
                        if personal_details.profile_image:
                            request.session['profile_image_url'] = personal_details.profile_image.url  # Store the profile image URL in the session
                        return redirect('matrimony:personaldetails')  # Redirect non-superusers to personaldetails
                    else:
                        # If aadhar_valid is False, redirect to Aadhar update page
                        return redirect('matrimony:update_aadhar')  # Adjust this to your actual Aadhar update page URL
                except PersonalDetails.DoesNotExist:
                    request.session['profile_image_url'] = ''  # No PersonalDetails for the user

                return redirect('matrimony:personaldetails')  # Default redirect to personal details
        else:
            messages.info(request, 'Username or Password is Incorrect')
    
    context = {}
    return render(request, 'accounts/login.html', context)

    
@login_required(login_url='accounts:login')
def logout_view(request):
    if 'suser' in request.session:
        del request.session['suser']  # Remove the "suser" session

    logout(request)
    return redirect('accounts:login')




from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from accounts.forms import ChangePasswordForm
class MyPasswordChangeView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'accounts/change_password.html'  # Replace with your desired template name
    success_url = reverse_lazy('matrimony:home')  # Replace with your desired success URL
