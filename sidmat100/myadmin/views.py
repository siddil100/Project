from django.shortcuts import render
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.contrib.auth.models import User

from django.core.mail import send_mail

def myadminview(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                # Check the current status and toggle it
                user.is_active = not user.is_active
                user.save()

                # Send an email when the account is suspended
                if not user.is_active:
                    subject = 'Your Account is Suspended'
                    message = f'Hello {user.username}, your account has been suspended by the admin.'
                    from_email = 'dreamwedofficials@gmail.com'  # Replace with your admin email
                    recipient_list = [user.email]
                    
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            except User.DoesNotExist:
                # Handle the case where the user is not found
                pass

    users = User.objects.filter(is_superuser=False)
    return render(request, 'myadmin/myadmin.html', {'users': users})


