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
from matrimony.models import BlockedUser

@login_required
def received_interests(request):
    # Get received interests for the user with a pending status
    received_interests = Interest.objects.filter(receiver=request.user, status=Interest.PENDING)

    # Get a list of blocked user IDs for the current user
    blocked_user_ids = BlockedUser.objects.filter(user=request.user).values_list('blocked_user_id', flat=True)

    # Exclude blocked users from the received interests queryset
    received_interests = received_interests.exclude(sender_id__in=blocked_user_ids)

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

        # Create a reciprocal interest for the sender with reversed sender and receiver
        reciprocal_interest = Interest(sender=interest.receiver, receiver=interest.sender, status=Interest.ACCEPTED)
        reciprocal_interest.save()

        # Redirect to a success page or another view
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
from .models import Interest

def accepted_interests_view(request):
    blocked_users = BlockedUser.objects.filter(user=request.user).values_list('blocked_user_id', flat=True)
    not_interested_users = NotInterested.objects.filter(user=request.user).values_list('not_interested_user_id', flat=True)

    excluded_users = list(blocked_users) + list(not_interested_users)

    accepted_interests = Interest.objects.filter(
        receiver=request.user,
        status=Interest.ACCEPTED
    ).exclude(
        Q(sender_id__in=excluded_users) | Q(sender=request.user)
    )

    return render(request, 'matint/accepted_interests.html', {
        'accepted_interests': accepted_interests,
    })








########################################################################################

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InterestedProfile  # Import your InterestedProfile model

@login_required
def add_interested(request, user_id):
    user_to_show_interest = get_object_or_404(User, id=user_id)
    
    # Check if the user is trying to express interest in themselves
    if user_to_show_interest == request.user:
        messages.warning(request, 'You cannot express interest in yourself.')
    else:
        # Check if the user has already expressed interest in the profile
        if InterestedProfile.objects.filter(user=request.user, interested_user=user_to_show_interest).exists():
            messages.warning(request, 'You have already added this profile to Interested-Profiles.')
        else:
            interested_user_details = user_to_show_interest.personaldetails  # Retrieve personal details of the user to show interest
            InterestedProfile.objects.create(user=request.user, interested_user=user_to_show_interest, interested_user_details=interested_user_details)
            # Optionally, perform additional actions after expressing interest

    return redirect('matint:interested_profiles_list')





from .models import Interest

def interested_profiles_list(request):
    current_user = request.user

    # Retrieve accepted interests where the logged-in user is the sender
    accepted_interests = Interest.objects.filter(sender=current_user, status='accepted')

    # Retrieve interested profiles of the current user excluding those related to accepted interests
    interested_profiles = InterestedProfile.objects.filter(
        Q(user=current_user) | Q(interested_user=current_user)
    ).exclude(
        interested_user_id__in=[interest.receiver_id for interest in accepted_interests]
    )

    return render(request, 'matint/interested_profiles_list.html', {'interested_profiles': interested_profiles})


from django.shortcuts import get_object_or_404

from .models import InterestedProfile


def remove_interest_profiles(request, user_id):
    interested_profile = get_object_or_404(InterestedProfile, user=request.user, interested_user_id=user_id)
    interested_profile.delete()
    return redirect('matint:interested_profiles_list')











# views.py

from django.shortcuts import render
@login_required
def search_view(request):
    return render(request, 'matint/search_form.html')



# views.py

from django.shortcuts import render
from matrimony.models import *

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
        'max_age': request.GET.get('max_age', ''),
        'min_height': request.GET.get('min_height', ''),  
        'max_height': request.GET.get('max_height', ''),
        'min_weight': request.GET.get('min_weight', ''),  
        'max_weight': request.GET.get('max_weight', ''),
        
        
        
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


    physical_details_qs = PhysicalDetails.objects.all()

    if query['min_height']:
        min_height = float(query['min_height'])
        physical_details_qs = physical_details_qs.filter(height__gte=min_height)
        physical_users = physical_details_qs.values_list('user_id', flat=True)
        personal_details_qs = personal_details_qs.filter(user_id__in=physical_users)

    if query['max_height']:
        max_height = float(query['max_height'])
        physical_details_qs = physical_details_qs.filter(height__lte=max_height)
        physical_users = physical_details_qs.values_list('user_id', flat=True)
        personal_details_qs = personal_details_qs.filter(user_id__in=physical_users)

    if query['min_weight']:
        min_weight = float(query['min_weight'])
        physical_details_qs = physical_details_qs.filter(weight__gte=min_weight)
        physical_users = physical_details_qs.values_list('user_id', flat=True)
        personal_details_qs = personal_details_qs.filter(user_id__in=physical_users)

    if query['max_weight']:
        max_weight = float(query['max_weight'])
        physical_details_qs = physical_details_qs.filter(weight__lte=max_weight)
        physical_users = physical_details_qs.values_list('user_id', flat=True)
        personal_details_qs = personal_details_qs.filter(user_id__in=physical_users)





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
        # Fetching blocked users for the logged_in_user
        blocked_users = BlockedUser.objects.filter(user=logged_in_user).values_list('blocked_user', flat=True)

        # Fetching not interested users for the logged_in_user
        not_interested_users = NotInterested.objects.filter(user=logged_in_user).values_list('not_interested_user', flat=True)

        # Combining blocked users and not interested users
        excluded_users = list(blocked_users) + list(not_interested_users)

        # Exclude both blocked users and not interested users from personal_details_qs
        personal_details_qs = personal_details_qs.exclude(user__in=excluded_users)


    context = {
        'query': query,
        'personal_details': personal_details_qs,
        'location_details': location_details_qs,
        'educational_details': educational_details_qs,
        'employment_details': employment_details_qs,
        'physical_details': physical_details_qs,
        # Add more querysets as needed for other models
    }

    return render(request, 'matint/search_results.html', context)


####   NOT INTERESTED MODEL

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import NotInterested
from matrimony.models import PersonalDetails

def add_notinterested(request, user_id):
    user_not_interested = get_object_or_404(User, id=user_id)
    
    # Check if the user is already marked as not interested
    if NotInterested.objects.filter(user=request.user, not_interested_user_id=user_id).exists():
        # If the user is already marked as not interested, display a message
        messages.warning(request, 'This user is already marked as not interested.')
    else:
        not_interested_user_details = user_not_interested.personaldetails
        NotInterested.objects.create(user=request.user, not_interested_user_details=not_interested_user_details, not_interested_user_id=user_id)
        # Optionally, perform additional actions after marking the user as not interested

    return redirect('matint:notinterested_list')




def notinterested_list(request):
    current_user = request.user
    
    # Retrieve users marked as not interested by the current user
    not_interested_users = NotInterested.objects.filter(user=current_user)
    
    return render(request, 'matint/notinterested_list.html', {'not_interested_users': not_interested_users})




def remove_notinterested(request, user_id):
    user_to_remove = get_object_or_404(User, id=user_id)
    not_interested_user = get_object_or_404(NotInterested, user=request.user, not_interested_user_details__user=user_to_remove)
    not_interested_user.delete()  # Remove the user from the not interested list
    # Optionally, perform additional actions after removing the user from the not interested list
    return redirect('matint:notinterested_list')
