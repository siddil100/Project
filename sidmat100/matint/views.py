from django.shortcuts import render, redirect, get_object_or_404
from .forms import InterestForm  # Import your InterestForm from forms.py
from .models import Interest
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.shortcuts import render, redirect, get_object_or_404
from .forms import InterestForm
from .models import Interest
from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404, render, redirect
from .models import Interest
from .forms import InterestForm

def send_interest(request, user_id):
    recipient = get_object_or_404(User, id=user_id)
    already_sent = False
    already_accepted = False
    pending = False  # Initialize pending variable

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            sender = request.user
            existing_interest = Interest.objects.filter(sender=sender, receiver=recipient, status='pending').exists()
            if not existing_interest:
                Interest.objects.create(receiver=recipient, message=message, sender=sender)
                return redirect('matrimony:home')
            else:
                already_sent = True

    else:
        form = InterestForm()

    accepted_interest = Interest.objects.filter(sender=request.user, receiver=recipient, status='accepted').exists()
    if accepted_interest:
        already_accepted = True

    pending_interest = Interest.objects.filter(sender=request.user, receiver=recipient, status='pending').exists()
    if pending_interest:
        pending = True  # Set pending to True if there's a pending interest

    context = {
        'form': form,
        'recipient': recipient,
        'already_sent': already_sent,
        'already_accepted': already_accepted,
        'pending': pending,  # Pass pending to the template
    }
    return render(request, 'matint/send_interest.html', context)




from django.shortcuts import render, get_object_or_404
from .models import Interest

@login_required
def received_interests(request):
    received_interests = Interest.objects.filter(receiver=request.user, status=Interest.PENDING)
    context = {
        'received_interests': received_interests,
    }
    return render(request, 'matint/received_interests.html', context)


@login_required
def accept_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    if interest.receiver == request.user and interest.status == Interest.PENDING:
        interest.status = Interest.ACCEPTED
        interest.save()
        # You can redirect to a success page or another view
        return redirect('matint:received_interests')
    # Handle cases where the interest is already accepted or the user doesn't have permission

@login_required
def reject_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    if interest.receiver == request.user and interest.status == Interest.PENDING:
        interest.status = Interest.REJECTED
        interest.save()
        # You can redirect to a success page or another view
        return redirect('matint:received_interests')
    # Handle cases where the interest is already rejected or the user doesn't have permission










# views.py

from django.shortcuts import render
@login_required
def search_view(request):
    return render(request, 'matint/search_form.html')



# views.py

from django.shortcuts import render
from matrimony.models import PersonalDetails, LocationDetails, EducationalDetails, EmploymentDetails,BlockedUser

from django.contrib.auth.models import User

from django.db.models import Q
from datetime import timedelta,date

def global_search(request):
    query = {
        'first_name': request.GET.get('first_name', ''),
        'last_name': request.GET.get('last_name', ''),
        'religion': request.GET.get('religion', ''),
        'current_city': request.GET.get('current_city', ''),
        'current_state': request.GET.get('current_state', ''),
        'highest_qualification': request.GET.get('highest_qualification', ''),
        'occupation': request.GET.get('occupation', ''),
        'min_age': request.GET.get('min_age', ''),  # Add min_age field to query dictionary
        'max_age': request.GET.get('max_age', ''),  # Add max_age field to query dictionary
        'exact_age': request.GET.get('exact_age', ''),
        
        # Add more fields from the form as needed
    }
    

# Filter PersonalDetails based on age criteria
    
    # Filtering PersonalDetails
    personal_details_qs = PersonalDetails.objects.all()
    if query['first_name']:
        personal_details_qs = personal_details_qs.filter(first_name__icontains=query['first_name'])
    if query['last_name']:
        personal_details_qs = personal_details_qs.filter(last_name__icontains=query['last_name'])
    if query['religion']:
        personal_details_qs = personal_details_qs.filter(religion__icontains=query['religion'])


    if query['min_age']:
        min_age = int(query['min_age'])
        min_birth_year = date.today().year - min_age
        min_birth_date = date(min_birth_year, date.today().month, date.today().day)
        personal_details_qs = personal_details_qs.filter(date_of_birth__lte=min_birth_date)

    if query['max_age']:
        max_age = int(query['max_age'])
        max_birth_year = date.today().year - max_age - 1
        max_birth_date = date(max_birth_year, date.today().month, date.today().day)
        personal_details_qs = personal_details_qs.filter(date_of_birth__gte=max_birth_date)

    if query['exact_age']:
        exact_age = int(query['exact_age'])
        exact_birth_year = date.today().year - exact_age
        exact_birth_date_start = date(exact_birth_year, date.today().month, date.today().day)
        exact_birth_date_end = exact_birth_date_start.replace(year=exact_birth_date_start.year + 1)
        personal_details_qs = personal_details_qs.filter(
            date_of_birth__gte=exact_birth_date_start,
            date_of_birth__lt=exact_birth_date_end
        )




    # Filtering LocationDetails and linking back to PersonalDetails
    location_details_qs = LocationDetails.objects.all()
    if query['current_city']:
        location_details_qs = location_details_qs.filter(current_city__iexact=query['current_city'])
        # Link filtered LocationDetails back to corresponding PersonalDetails
    if query['current_state']:
        location_details_qs = location_details_qs.filter(current_state__iexact=query['current_state'])
        location_users = location_details_qs.values_list('user', flat=True)
        personal_details_qs = personal_details_qs.filter(user__in=location_users)

    # Filtering EducationalDetails and linking back to PersonalDetails
    educational_details_qs = EducationalDetails.objects.all()
    if query['highest_qualification']:
        educational_details_qs = educational_details_qs.filter(highest_qualification__icontains=query['highest_qualification'])
        # Link filtered EducationalDetails back to corresponding PersonalDetails
        educational_users = educational_details_qs.values_list('user', flat=True)
        personal_details_qs = personal_details_qs.filter(user__in=educational_users)

    # Filtering EmploymentDetails and linking back to PersonalDetails
    employment_details_qs = EmploymentDetails.objects.all()
    if query['occupation']:
        employment_details_qs = employment_details_qs.filter(occupation__icontains=query['occupation'])
        # Link filtered EmploymentDetails back to corresponding PersonalDetails
        employment_users = employment_details_qs.values_list('user', flat=True)
        personal_details_qs = personal_details_qs.filter(user__in=employment_users)

    # Additional conditions, exclusions, etc. (if needed)

    user_gender = None
    if request.user.is_authenticated:
        user = request.user
        try:
            personal_details = PersonalDetails.objects.get(user=user)
            user_gender = personal_details.gender
        except PersonalDetails.DoesNotExist:
            pass

    if user_gender:
        # Exclude profiles of the logged-in user's gender
        personal_details_qs = personal_details_qs.exclude(gender=user_gender)

    logged_in_user = request.user if request.user.is_authenticated else None

    # Exclude blocked users from the search results
    if logged_in_user:
        blocked_users = BlockedUser.objects.filter(user=logged_in_user).values_list('blocked_user', flat=True)
        personal_details_qs = personal_details_qs.exclude(user__in=blocked_users)

    context = {
        'query': query,
        'personal_details': personal_details_qs,
        'location_details': location_details_qs,
        'educational_details': educational_details_qs,
        'employment_details': employment_details_qs,
        # Add more querysets as needed for other models
    }

    return render(request, 'matint/search_results.html', context)




