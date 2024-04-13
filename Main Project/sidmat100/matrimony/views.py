from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PersonalDetailsForm,Hobby
from .forms import FamilyDetailsForm
from .forms import EducationalDetailsForm
from .forms import EmploymentDetailsForm
from .forms import LocationDetailsForm
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

from .models import PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails


import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail


def check_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        exists = PersonalDetails.objects.filter(phone_number=phone_number).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})



@never_cache
@login_required(login_url='accounts:login')
def personaldetailsview(request):
    user = request.user

    # Get the list of hobbies from the database
    hobbies = Hobby.objects.all()

    # Check if the PersonalDetails form is already filled
    if PersonalDetails.objects.filter(user=user, perso_fill=True).exists():
        # PersonalDetails form is already filled, move to the next form
        return redirect('matrimony:familydetails')

    if request.method == 'POST':
        personal_details_form = PersonalDetailsForm(request.POST, request.FILES)
        if personal_details_form.is_valid():
            print("Selected Hobbies:", personal_details_form.cleaned_data['hobbies'])
            personal_details = personal_details_form.save(commit=False)
            personal_details.user = user
            personal_details.aadhar_valid = True
            personal_details.perso_fill = True
            personal_details.save()

            # Handle hobbies
            selected_hobbies = request.POST.getlist('hobbies')
            personal_details.hobbies.set(Hobby.objects.filter(id__in=selected_hobbies))


            return redirect('matrimony:familydetails')  # Move to the next form
        else:
            # Print form data and errors to the console
            print("Form Data:", request.POST)
            print("Form Errors:", personal_details_form.errors)
    else:
        personal_details_form = PersonalDetailsForm()

    return render(request, 'matrimony/personaldetails.html', {'personal_details_form': personal_details_form, 'hobbies': hobbies})











@never_cache
@login_required(login_url='accounts:login')
def familydetailsview(request):
    user = request.user

    # Check if the FamilyDetails form is already filled
    if FamilyDetails.objects.filter(user=user, famil_fill=True).exists():
        # FamilyDetails form is already filled, move to the next form
        return redirect('matrimony:educationaldetails')

    if request.method == 'POST':
        family_details_form = FamilyDetailsForm(request.POST)
        if family_details_form.is_valid():
            family_details = family_details_form.save(commit=False)
            family_details.user = user
            family_details.famil_fill = True
            family_details.save()
            return redirect('matrimony:educationaldetails')  # Move to the next form

    else:
        family_details_form = FamilyDetailsForm()

    return render(request, 'matrimony/familydetails.html', {'family_details_form': family_details_form})




@never_cache
@login_required(login_url='accounts:login')
def educationaldetailsview(request):
    user = request.user

    # Check if the EducationalDetails form is already filled
    if EducationalDetails.objects.filter(user=user, educ_fill=True).exists():
        # EducationalDetails form is already filled, move to the next form
        return redirect('matrimony:employmentdetails')

    if request.method == 'POST':
        educational_details_form = EducationalDetailsForm(request.POST)
        highest_qualification = request.POST.get('highest_qualification')
        ug_degree = request.POST.get('ug_degree')
        if educational_details_form.is_valid():
            educational_details = educational_details_form.save(commit=False)
            educational_details.user = user
            if highest_qualification == 'undergraduate':
            # Set pg_degree and doctorate_field as None for undergraduate
                educational_details.pg_degree = None
                educational_details.doctorate_field = None
                educational_details.ug_degree = ug_degree
            educational_details.educ_fill = True
            educational_details.save()
            return redirect('matrimony:employmentdetails')  # Move to the next form

    else:
        educational_details_form = EducationalDetailsForm()

    return render(request, 'matrimony/educationaldetails.html', {'educational_details_form': educational_details_form})




@never_cache
@login_required(login_url='accounts:login')
def employmentdetailsview(request):
    user = request.user

    # Check if the EmploymentDetails form is already filled
    if EmploymentDetails.objects.filter(user=user, empl_fill=True).exists():
        # EmploymentDetails form is already filled, move to the next form
        return redirect('matrimony:locationdetails')

    if request.method == 'POST':
        employment_details_form = EmploymentDetailsForm(request.POST)
        if employment_details_form.is_valid():
            employment_details = employment_details_form.save(commit=False)
            employment_details.user = user
            employment_details.empl_fill = True
            employment_details.save()
            return redirect('matrimony:locationdetails')  # Move to the next form

    else:
        employment_details_form = EmploymentDetailsForm()

    return render(request, 'matrimony/employmentdetails.html', {'employment_details_form': employment_details_form})



@never_cache
@login_required(login_url='accounts:login')
def locationdetailsview(request):
    user = request.user

    # Check if the LocationDetails form is already filled
    if LocationDetails.objects.filter(user=user, loca_fill=True).exists():
        # LocationDetails form is already filled

        # Check if the email is verified
        if LocationDetails.objects.filter(user=user, is_email_verified=True).exists():
            return redirect('matrimony:home')  # Email is verified, redirect to the home page
        else:
            return render(request, 'matrimony/regsuccess.html')

    if request.method == 'POST':
        location_details_form = LocationDetailsForm(request.POST, request.FILES)
        if location_details_form.is_valid():
            location_details = location_details_form.save(commit=False)
            location_details.user = user
            location_details.loca_fill = True
            location_details.is_email_verified = False
            location_details.email_verification_token = str(uuid.uuid4())
            location_details.save()

            current_site = get_current_site(request)
            subject = "Activate your Account"
            activation_link = f"http://{current_site}/matrimony/verify_email/{location_details.email_verification_token}/"
            message = f'Click the link to activate your account: {activation_link}'
            send_mail(subject, message, 'matrimony@gmail.com', [user.email])
            return render(request, 'matrimony/regsuccess.html')
            # You may consider showing a message instead of redirecting immediately

    else:
        location_details_form = LocationDetailsForm()

    return render(request, 'matrimony/locationdetails.html', {'location_details_form': location_details_form})

from django.http import HttpResponse
from django.shortcuts import redirect
from .models import LocationDetails
@never_cache
@login_required(login_url='accounts:login')
def verify_email_view(request, token):
    try:
        user_details = LocationDetails.objects.get(email_verification_token=token)
        if user_details:
            # Assuming you want to verify the email for the associated user
            user_details.is_email_verified = True
            user_details.email_verification_token = None
            user_details.save()
            
            # Redirect to the login page or any other desired page
            return redirect('accounts:login')
    except LocationDetails.DoesNotExist:
        # Catch the specific exception when the details are not found
        return HttpResponse("Activation link is invalid!")
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in email verification: {e}")
        return HttpResponse("An error occurred during email verification. Please try again later.")





from django.shortcuts import render, redirect
from .models import PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails

from django.shortcuts import render, redirect
from .models import PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails
from matint.models import NotInterested
from matint.models import UserActivity

@never_cache
@login_required(login_url='accounts:login')
def homeview(request):
    user = request.user
    all_profiles_info = []

    # Check and redirect if any form is not filled
    if not all([
        PersonalDetails.objects.filter(user=user, perso_fill=True).exists(),
        FamilyDetails.objects.filter(user=user, famil_fill=True).exists(),
        EducationalDetails.objects.filter(user=user, educ_fill=True).exists(),
        EmploymentDetails.objects.filter(user=user, empl_fill=True).exists(),
        LocationDetails.objects.filter(user=user, loca_fill=True).exists(),
    ]):
        if not PersonalDetails.objects.filter(user=user, perso_fill=True).exists():
            return redirect('matrimony:personaldetails')
        elif not FamilyDetails.objects.filter(user=user, famil_fill=True).exists():
            return redirect('matrimony:familydetails')
        elif not EducationalDetails.objects.filter(user=user, educ_fill=True).exists():
            return redirect('matrimony:educationaldetails')
        elif not EmploymentDetails.objects.filter(user=user, empl_fill=True).exists():
            return redirect('matrimony:employmentdetails')
        elif not LocationDetails.objects.filter(user=user, loca_fill=True).exists():
            return redirect('matrimony:locationdetails')

    try:
        preferences = Preference.objects.get(user=user)

        personal_details = PersonalDetails.objects.get(user=user)
        profile_image_url = personal_details.profile_image.url
        opposite_gender = 'female' if personal_details.gender == 'male' else 'male'
        blocked_users = BlockedUser.objects.filter(user=user).values_list('blocked_user', flat=True)
        not_interested_users = NotInterested.objects.filter(user=user).values_list('not_interested_user', flat=True)
        
        # Fetch UserActivity data for the logged-in user
        user_activities = UserActivity.objects.filter(user=user)

        # Populating filtered_profiles based on preferences
        filtered_profiles = PersonalDetails.objects.filter(
            perso_fill=True,
            gender=opposite_gender,
            religion=preferences.religion,
        ).exclude(user=user)

        if preferences.occupation:
            filtered_profile_user_ids = EmploymentDetails.objects.filter(occupation=preferences.occupation).values_list('user_id', flat=True)
            filtered_profiles = filtered_profiles.filter(user_id__in=filtered_profile_user_ids)

        if preferences.current_city:
            filtered_profile_user_ids = LocationDetails.objects.filter(current_city=preferences.current_city).values_list('user_id', flat=True)
            filtered_profiles = filtered_profiles.filter(user_id__in=filtered_profile_user_ids)
            filtered_profiles = filtered_profiles.exclude(user__in=blocked_users)
            filtered_profiles = filtered_profiles.exclude(user__in=not_interested_users)

        filtered_employment_details = []
        filtered_location_details = []
        filtered_profiles_info = [] 
        viewed_profile_ids = user_activities.values_list('viewed_user_id', flat=True)

        for profile in filtered_profiles:
            try:
                employment = EmploymentDetails.objects.get(user=profile.user)
                location = LocationDetails.objects.get(user=profile.user)
                filtered_employment_details.append(employment)
                filtered_location_details.append(location)

                # Check if the profile has been viewed by the user
                profile_viewed = profile.user_id in viewed_profile_ids
                filtered_profiles_info.append((profile, employment, location, profile_viewed))
            except (EmploymentDetails.DoesNotExist, LocationDetails.DoesNotExist):
                filtered_employment_details.append(None)
                filtered_location_details.append(None)
                filtered_profiles_info.append((profile, None, None, False))

        # Populating all_profiles_info regardless of preferences
        all_profiles = PersonalDetails.objects.exclude(user=user).filter(gender=opposite_gender, perso_fill=True)
        all_profiles = all_profiles.exclude(user__in=blocked_users)
        all_profiles = all_profiles.exclude(user__in=not_interested_users)

        viewed_profile_ids = user_activities.values_list('viewed_user_id', flat=True)

        for profile in all_profiles.exclude(id__in=filtered_profiles):
            try:
                employment = EmploymentDetails.objects.get(user=profile.user)
                location = LocationDetails.objects.get(user=profile.user)
                profile_viewed = profile.user_id in viewed_profile_ids
                all_profiles_info.append((profile, employment, location, profile_viewed))
            except (EmploymentDetails.DoesNotExist, LocationDetails.DoesNotExist):
                all_profiles_info.append((profile, None, None, False))

        return render(request, 'matrimony/home.html', {
            'profile_image_url': profile_image_url,
            'filtered_profiles_info': filtered_profiles_info,
            'all_profiles_info': all_profiles_info,
            'user_activities': user_activities,
        })

    except Preference.DoesNotExist:
        personal_details = PersonalDetails.objects.get(user=user)
        profile_image_url = personal_details.profile_image.url
        opposite_gender = 'female' if request.user.personaldetails.gender == 'male' else 'male'

        # Fetch UserActivity data for the logged-in user
        user_activities = UserActivity.objects.filter(user=user)
        viewed_profile_ids = user_activities.values_list('viewed_user_id', flat=True)

        opposite_gender_profiles = PersonalDetails.objects.filter(gender=opposite_gender, perso_fill=True).exclude(user=request.user)

        blocked_users = BlockedUser.objects.filter(user=user).values_list('blocked_user', flat=True)
        not_interested_users = NotInterested.objects.filter(user=user).values_list('not_interested_user', flat=True)
        opposite_gender_profiles = opposite_gender_profiles.exclude(user__in=blocked_users)
        opposite_gender_profiles = opposite_gender_profiles.exclude(user__in=not_interested_users)

        all_employment_details = []
        all_location_details = []
        
        
        for profile in opposite_gender_profiles:
            try:
                employment = EmploymentDetails.objects.get(user=profile.user)
                location = LocationDetails.objects.get(user=profile.user)
                profile_viewed = profile.user_id in viewed_profile_ids
                all_employment_details.append(employment)
                all_location_details.append(location)
                all_profiles_info.append((profile, employment, location, profile_viewed))
            except (EmploymentDetails.DoesNotExist, LocationDetails.DoesNotExist):
                all_employment_details.append(None)
                all_location_details.append(None)
                all_profiles_info.append((profile, None, None, False))

        return render(request, 'matrimony/home.html', {
            'profile_image_url': profile_image_url,
            'filtered_profiles_info': None,  # No filtered profiles
            'all_profiles_info': all_profiles_info,
            'user_activities': user_activities,
        })







    


from matpayment import *
from django.shortcuts import render, get_object_or_404
from .models import User, PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails
from matint.models import Interest,UserActivity
from django.db.models import Q
@never_cache
@login_required(login_url='accounts:login')
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    viewed_user = user  # Store the user being viewed

    personal_details = get_object_or_404(PersonalDetails, user=user)

    try:
        family_details = FamilyDetails.objects.get(user=user)
    except FamilyDetails.DoesNotExist:
        family_details = None

    try:
        educational_details = EducationalDetails.objects.get(user=user)
    except EducationalDetails.DoesNotExist:
        educational_details = None

    try:
        employment_details = EmploymentDetails.objects.get(user=user)
    except EmploymentDetails.DoesNotExist:
        employment_details = None

    try:
        location_details = LocationDetails.objects.get(user=user)
    except LocationDetails.DoesNotExist:
        location_details = None

    try:
        interests = Interest.objects.filter(receiver=user)
    except Interest.DoesNotExist:
        interests = None

    # Retrieve images uploaded by the user
    user_images = Image.objects.filter(image_upload__user=user)

    activity_exists = UserActivity.objects.filter(
        Q(user=request.user, viewed_user=viewed_user) |
        Q(user=viewed_user, viewed_user=request.user)
    ).exists()


    interest_status = None

    # Check if the viewed user has sent an interest to the current user
    sent_interest = Interest.objects.filter(sender=user, receiver=request.user, status='accepted').exists()

    # Check if the viewed user has received an interest from the current user
    received_interest = Interest.objects.filter(sender=request.user, receiver=user, status='accepted').exists()

    if sent_interest or received_interest:
        interest_status = 'accepted'


    is_premium = False
    
    current_user = request.user
    try:
        premium_membership = PremiumMembership.objects.get(user=current_user)
        is_premium = premium_membership.is_premium
        print(is_premium)
    except PremiumMembership.DoesNotExist:
        pass
        print("except aane")

    # Render the page with existing context data
    context = {
        'user': user,
        'personal_details': personal_details,
        'family_details': family_details,
        'educational_details': educational_details,
        'employment_details': employment_details,
        'location_details': location_details,
        'hobbies': personal_details.hobbies.all(),
        'user_images': user_images,
        'interests': interests,
        'interest_status': interest_status,
        'is_premium': is_premium,
    }

    # Create UserActivity entry when viewing another user's profile
    if request.user != viewed_user:
    # Use update_or_create to either update existing or create a new UserActivity
        activity, created = UserActivity.objects.update_or_create(
            user=request.user,
            viewed_user=viewed_user,
            defaults={'viewed_details': True}
        )

    # If the activity already exists, update the viewed_details to True
    if not created:
        activity.viewed_details = True
        activity.save()



    return render(request, 'matrimony/user_detail.html', context)





from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails
from matchat.models import *
from matpayment.models import *

@never_cache
@login_required(login_url='accounts:login')
def myprofileview(request):
    user = request.user

    # Retrieve all the user's profile information
    personal_details = PersonalDetails.objects.get(user=user)
    family_details = FamilyDetails.objects.get(user=user)
    educational_details = EducationalDetails.objects.get(user=user)
    employment_details = EmploymentDetails.objects.get(user=user)
    location_details = LocationDetails.objects.get(user=user)
    

    # Retrieve user images
    user_images = Image.objects.filter(image_upload__user=user)

    try:
        # Fetch the user's physical details if available
        physical_details = PhysicalDetails.objects.get(user=user)
    except PhysicalDetails.DoesNotExist:
        physical_details = None


    try:
        premium_membership = PremiumMembership.objects.get(user=user)
    except PremiumMembership.DoesNotExist:
        premium_membership = None


    unread_message_count = Message.objects.filter(receiver=user, is_seen=False).count()

    context = {
        'user': user,
        'personal_details': personal_details,
        'family_details': family_details,
        'educational_details': educational_details,
        'employment_details': employment_details,
        'location_details': location_details,
        'user_images': user_images,
        'physical_details': physical_details,  # Include physical details in the context
        'unread_message_count': unread_message_count,
        'premium_membership': premium_membership,
    }

    return render(request, 'matrimony/my_profile.html', context)





from django.shortcuts import render, redirect


from .forms import PersonalDetailsUpdateForm  # Import the update form

from django.db import IntegrityError  # Import the specific exception if needed
@never_cache
@login_required(login_url='accounts:login')
def update_personaldetails(request):
    personal_details = PersonalDetails.objects.get(user=request.user)
    hobbies = Hobby.objects.all()  # Assuming Hobby is the model for hobbies

    if request.method == 'POST':
        form = PersonalDetailsUpdateForm(request.POST, request.FILES, instance=personal_details)
        if form.is_valid():
            try:
                updated_personal_details = form.save(commit=False)
                updated_personal_details.aadhar_valid = True
                form.save_m2m()
                updated_personal_details.save()

                return redirect('matrimony:myprofile')
            except IntegrityError as e:
                print(f"Error saving form: {e}")
        else:
            print(form.errors)
    else:
        form = PersonalDetailsUpdateForm(instance=personal_details)

    context = {
        'form': form,
        'hobbies': hobbies,
        'personal_details': personal_details,  # Include personal_details in the context
    }

    return render(request, 'matrimony/update_personaldetails.html', context)

from .forms import FamilyDetailsUpdateForm
@never_cache
@login_required(login_url='accounts:login')
def update_familydetails(request):
    family_details = FamilyDetails.objects.get(user=request.user)

    if request.method == 'POST':
        form = FamilyDetailsUpdateForm(request.POST, instance=family_details)  # Use FamilyDetailsUpdateForm
        if form.is_valid():
            try:
                form.save()
                return redirect('matrimony:myprofile')
            except IntegrityError as e:
                print(f"Error saving form: {e}")
        else:
            print(form.errors)

    else:
        form = FamilyDetailsUpdateForm(instance=family_details)  # Use FamilyDetailsUpdateForm

    context = {
        'form': form,
    }

    return render(request, 'matrimony/update_familydetails.html', context)



from django.shortcuts import render, redirect
from .models import EducationalDetails
from .forms import EducationalDetailsUpdateForm
@never_cache
@login_required(login_url='accounts:login')
def update_educationaldetails(request):
    educational_details = EducationalDetails.objects.get(user=request.user)

    if request.method == 'POST':
        form = EducationalDetailsUpdateForm(request.POST, instance=educational_details)
        if form.is_valid():
            try:
                form.save()
                return redirect('matrimony:myprofile')  # Redirect to the user's profile page
            except IntegrityError as e:
                print(f"Error saving form: {e}")
        else:
            print(form.errors)

    else:
        form = EducationalDetailsUpdateForm(instance=educational_details)

    context = {
        'form': form,
    }

    return render(request, 'matrimony/update_educationaldetails.html', context)


from django.shortcuts import render, redirect
from .models import EmploymentDetails
from .forms import EmploymentDetailsUpdateForm
@never_cache
@login_required(login_url='accounts:login')
def update_employmentdetails(request):
    employment_details = EmploymentDetails.objects.get(user=request.user)

    if request.method == 'POST':
        form = EmploymentDetailsUpdateForm(request.POST, instance=employment_details)
        if form.is_valid():
            form.save()
            return redirect('matrimony:myprofile')  # Redirect to the profile page after successful update
    else:
        form = EmploymentDetailsUpdateForm(instance=employment_details)

    context = {
        'form': form,
    }

    return render(request, 'matrimony/update_employmentdetails.html', context)


from django.shortcuts import render, redirect
from .models import LocationDetails
from .forms import LocationDetailsUpdateForm
@never_cache
@login_required(login_url='accounts:login')
def update_locationdetails(request):
    location_details = LocationDetails.objects.get(user=request.user)

    if request.method == 'POST':
        form = LocationDetailsUpdateForm(request.POST, request.FILES, instance=location_details)
        if form.is_valid():
            form.save()
            return redirect('matrimony:myprofile')  # Redirect to the profile page after a successful update
    else:
        form = LocationDetailsUpdateForm(instance=location_details)

    context = {
        'form': form,
    }

    return render(request, 'matrimony/update_locationdetails.html', context)



from django.shortcuts import render, redirect
from .forms import PersonalDetailsAadharForm
from .models import PersonalDetails
from django.conf import settings
@login_required(login_url='accounts:login')
def update_aadhar(request):
    personal_details = PersonalDetails.objects.get(user=request.user)

    if request.method == 'POST':
        form = PersonalDetailsAadharForm(request.POST, request.FILES, instance=personal_details)
        if form.is_valid():
            try:
                updated_personal_details = form.save(commit=False)
                
                updated_personal_details.save()
                send_mail(
                    'Aadhar Update Notification',
                    f'The user {request.user.username} has updated their Aadhar details for re-verification.',
                    settings.DEFAULT_FROM_EMAIL,  # Sender's email
                    ['thunderboltleo10@gmail.com'],  # Replace with the admin's email
                    fail_silently=False,
                )

                return render(request, 'matrimony/aadharsuccess.html')
            except IntegrityError as e:
                print(f"Error saving form: {e}")
        else:
            print(form.errors)
    else:
        form = PersonalDetailsAadharForm(instance=personal_details)

    return render(request, 'matrimony/updateaadhar.html', {'form': form})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm, ImageFormSet
from .models import ImageUpload,Image


from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import ImageUpload, Image
@login_required(login_url='accounts:login')
def upload_images(request):
    if request.method == 'POST':
        image_upload_form = ImageUploadForm(request.POST, request.FILES)
        if image_upload_form.is_valid():
            image = image_upload_form.save(commit=False)
            image.user = request.user
            image.save()

            # Process uploaded files
            for file in request.FILES.getlist('image'):
                # Check if the file is an image before saving
                if file.content_type.startswith('image'):
                    Image.objects.create(image_upload=image, image=file)
                else:
                    # Handle non-image files here (skip or raise an error)
                    pass  # For example, you can skip or log non-image files

            return redirect('matrimony:upload_images')  # Redirect to a success page
    else:
        image_upload_form = ImageUploadForm()

    user_images = ImageUpload.objects.filter(user=request.user)

    return render(request, 'matrimony/upload_images.html', {'image_upload_form': image_upload_form, 'user_images': user_images})




from django.shortcuts import redirect, get_object_or_404
from .models import ImageUpload, Image
from .forms import ImageForm



from django.shortcuts import get_object_or_404
@never_cache
@login_required(login_url='accounts:login')
def delete_image(request, image_upload_id, image_id):
    image_upload = get_object_or_404(ImageUpload, pk=image_upload_id, user=request.user)

    # Get the specific image
    image = get_object_or_404(Image, pk=image_id, image_upload=image_upload)

    # Delete the image
    image.delete()

    # Check if the ImageUpload has no more associated images
    if not image_upload.image_set.exists():
        # If no more images, delete the ImageUpload
        image_upload.delete()

    return redirect('matrimony:upload_images')  # Redirect to a success page or any other appropriate URL


@never_cache
@login_required(login_url='accounts:login')
def edit_image(request, image_upload_id, image_id):
    image_upload = get_object_or_404(ImageUpload, pk=image_upload_id, user=request.user)
    image = get_object_or_404(Image, pk=image_id, image_upload=image_upload)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('matrimony:upload_images')  # Redirect to a success page or any other appropriate URL
    else:
        form = ImageForm(instance=image)

    return redirect('matrimony:upload_images') 




from django.shortcuts import render, redirect
from .models import PhysicalDetails
from .forms import PhysicalDetailsForm
@never_cache
@login_required(login_url='accounts:login')
def physicaldetailsview(request):
    user = request.user
    physical_details_instance = None  # Initialize the variable outside the try block
    
    try:
        # Check if the PhysicalDetails form is already filled for the user
        physical_details_instance = PhysicalDetails.objects.get(user=user)
        form = PhysicalDetailsForm(instance=physical_details_instance)
    except PhysicalDetails.DoesNotExist:
        form = PhysicalDetailsForm()

    if request.method == 'POST':
        form = PhysicalDetailsForm(request.POST, instance=physical_details_instance)
        if form.is_valid():
            physical_details = form.save(commit=False)
            physical_details.user = user
            physical_details.phys_fill = True
            physical_details.save()
            return redirect('matrimony:myprofile')  # Move to the next form or process

    return render(request, 'matrimony/physicaldetails.html', {'physical_details_form': form})




from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import PhysicalDetails
from .forms import PhysicalDetailsUpdateForm
@never_cache
@login_required(login_url='accounts:login')
def update_physicaldetails(request):
    try:
        physical_details = PhysicalDetails.objects.get(user=request.user)
    except PhysicalDetails.DoesNotExist:
        physical_details = None

    if request.method == 'POST':
        form = PhysicalDetailsUpdateForm(request.POST, instance=physical_details)
        if form.is_valid():
            try:
                updated_physical_details = form.save(commit=False)
                updated_physical_details.user = request.user
                updated_physical_details.phys_fill = True
                updated_physical_details.save()
                messages.success(request, 'Physical details updated successfully!')
                return redirect('matrimony:myprofile')
            except IntegrityError as e:
                messages.error(request, f"Error saving form: {e}")
        else:
            print(form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PhysicalDetailsUpdateForm(instance=physical_details)

    context = {
        'form': form,
    }

    return render(request, 'matrimony/update_physicaldetails.html', context)






from django.shortcuts import render, redirect
from .forms import PreferenceForm
from django.contrib.auth.decorators import login_required
from .models import Preference

@never_cache
@login_required(login_url='accounts:login')
def update_preference(request):
    user = request.user
    try:
        preference = Preference.objects.get(user=user)
    except Preference.DoesNotExist:
        preference = None

    if request.method == 'POST':
        preference_form = PreferenceForm(request.POST, instance=preference)
        if preference_form.is_valid():
            preference = preference_form.save(commit=False)
            preference.user = user
            preference.save()
            return redirect('matrimony:myprofile')  # Redirect to a success page
    else:
        preference_form = PreferenceForm(instance=preference)

    return render(request, 'matrimony/update_preference.html', {'preference_form': preference_form})

from .models import BlockedUser

from django.contrib import messages
@never_cache
@login_required(login_url='accounts:login')
def block_user(request, user_id):
    user_to_block = get_object_or_404(User, id=user_id)
    
    # Check if the user is already blocked
    if BlockedUser.objects.filter(user=request.user, blocked_user_id=user_id).exists():
        # If the user is already blocked, display a message
        messages.warning(request, 'This user is already blocked.')
    else:
        blocked_user_details = user_to_block.personaldetails  # Retrieve personal details of the user to block
        BlockedUser.objects.create(user=request.user, blocked_user_details=blocked_user_details, blocked_user_id=user_id)
        # Optionally, perform additional actions after blocking the user

    return redirect('matrimony:blocked_users_list')


@never_cache
@login_required(login_url='accounts:login')
def blocked_users_list(request):
    current_user = request.user
    
    # Retrieve blocked users by the current user
    blocked_users = BlockedUser.objects.filter(user=current_user)
    
    return render(request, 'matrimony/blocked_users_list.html', {'blocked_users': blocked_users})


@never_cache
@login_required(login_url='accounts:login')
def unblock_user(request, user_id):
    user_to_unblock = get_object_or_404(User, id=user_id)
    blocked_user = get_object_or_404(BlockedUser, user=request.user, blocked_user_details__user=user_to_unblock)
    blocked_user.delete()  # Unblock the user by deleting the BlockedUser instance
    # Optionally, perform additional actions after unblocking the user
    return redirect('matrimony:blocked_users_list')