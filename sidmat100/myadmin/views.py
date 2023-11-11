from django.shortcuts import render
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.contrib.auth.models import User

from django.core.mail import send_mail

from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@never_cache
@login_required(login_url='accounts:login')
def myadminview(request):
    # Get the filter criteria
    # Get the filter criteria
    filter_name = request.GET.get('name', 'all')  # Default to 'all'
    filter_status = request.GET.get('status', 'all')  # Default to 'all'
    filter_gender = request.GET.get('gender', 'all')  # Default to 'all'

    # Get all users
    users = User.objects.filter(is_superuser=False)

    # Apply filters based on the criteria
    if filter_name != 'all':
        users = users.filter(username__istartswith=filter_name)  # Filter by name

    if filter_status == 'active':
        users = users.filter(is_active=True)  # Filter by active status
    elif filter_status == 'inactive':
        users = users.filter(is_active=False)  # Filter by inactive status

    if filter_gender == 'male':
        users = users.filter(personaldetails__gender='male')  # Filter by male gender
    elif filter_gender == 'female':
        users = users.filter(personaldetails__gender='female')  # Filter by female gender

    # Define the number of users to display per page
    per_page = 10
    paginator = Paginator(users, per_page)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        suspension_reason = request.POST.get('suspension_reason')  # Get the selected suspension reason

        if user_id:
            try:
                user = User.objects.get(id=user_id)

                if user.is_active:
                    # If the user is active, suspend them and save the suspension reason
                    user.is_active = False
                    user.suspension_reason = suspension_reason
                    user.save()

                    # Send an email with the suspension reason
                    subject = 'Your Account is Suspended'
                    message = f'Hello {user.username}, your account has been suspended by the admin due to the following reason: {suspension_reason}. If you feel there is something wrong, please contact us at dreamwedofficials@gmail.com.'
                    from_email = 'dreamwedofficials@gmail.com'  # Replace with your admin email
                    recipient_list = [user.email]

                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                else:
                    # Handle unsuspension if needed
                    user.is_active = True
                    user.suspension_reason = ""
                    user.save()
            except User.DoesNotExist:
                # Handle the case where the user is not found
                pass
            

    return render(request, 'myadmin/myadmin.html', {'users': page})






