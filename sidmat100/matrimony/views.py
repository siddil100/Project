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



def check_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        exists = PersonalDetails.objects.filter(phone_number=phone_number).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})



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




@login_required(login_url='accounts:login')
def educationaldetailsview(request):
    user = request.user

    # Check if the EducationalDetails form is already filled
    if EducationalDetails.objects.filter(user=user, educ_fill=True).exists():
        # EducationalDetails form is already filled, move to the next form
        return redirect('matrimony:employmentdetails')

    if request.method == 'POST':
        educational_details_form = EducationalDetailsForm(request.POST)
        if educational_details_form.is_valid():
            educational_details = educational_details_form.save(commit=False)
            educational_details.user = user
            educational_details.educ_fill = True
            educational_details.save()
            return redirect('matrimony:employmentdetails')  # Move to the next form

    else:
        educational_details_form = EducationalDetailsForm()

    return render(request, 'matrimony/educationaldetails.html', {'educational_details_form': educational_details_form})




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



@login_required(login_url='accounts:login')
def locationdetailsview(request):
    user = request.user

    # Check if the LocationDetails form is already filled
    if LocationDetails.objects.filter(user=user, loca_fill=True).exists():
        # LocationDetails form is already filled, redirect to the home page
        return redirect('matrimony:home')

    if request.method == 'POST':
        location_details_form = LocationDetailsForm(request.POST, request.FILES)
        if location_details_form.is_valid():
            location_details = location_details_form.save(commit=False)
            location_details.user = user
            location_details.loca_fill = True
            location_details.save()
            return redirect('matrimony:home')  # All forms are filled, redirect to the home page

    else:
        location_details_form = LocationDetailsForm()

    return render(request, 'matrimony/locationdetails.html', {'location_details_form': location_details_form})







from django.shortcuts import render, redirect
from .models import PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails

from django.shortcuts import render, redirect
from .models import PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails

@login_required(login_url='accounts:login')
def homeview(request):
    user = request.user

    # Check if all forms are filled
    if all([
        PersonalDetails.objects.filter(user=user, perso_fill=True).exists(),
        FamilyDetails.objects.filter(user=user, famil_fill=True).exists(),
        EducationalDetails.objects.filter(user=user, educ_fill=True).exists(),
        EmploymentDetails.objects.filter(user=user, empl_fill=True).exists(),
        LocationDetails.objects.filter(user=user, loca_fill=True).exists(),
    ]):
        personal_details = PersonalDetails.objects.get(user=user)
        profile_image_url = personal_details.profile_image.url

        # Determine the opposite gender
        opposite_gender = 'female' if personal_details.gender == 'male' else 'male'

        # Get a list of user profiles (excluding the currently logged-in user) based on gender
        profiles = PersonalDetails.objects.filter(perso_fill=True, gender=opposite_gender).exclude(user=user)

        # Retrieve the employment details for each profile
        employment_details = []
        location_details = []

        for profile in profiles:
            try:
                employment = EmploymentDetails.objects.get(user=profile.user)
                location = LocationDetails.objects.get(user=profile.user)
                employment_details.append(employment)
                location_details.append(location)
            except (EmploymentDetails.DoesNotExist, LocationDetails.DoesNotExist):
                # Handle the case where a profile doesn't have employment or location details
                employment_details.append(None)
                location_details.append(None)

        # Pair profiles with their employment and location details
        profiles_info = zip(profiles, employment_details, location_details)

        return render(request, 'matrimony/home.html', {
            'profile_image_url': profile_image_url,
            'profiles_info': profiles_info,
        })

    # Redirect to the first unfilled form
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
    



from django.shortcuts import render, get_object_or_404
from .models import User, PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails
@never_cache
@login_required(login_url='accounts:login')
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)

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

    return render(request, 'matrimony/user_detail.html', {
        'user': user,
        'personal_details': personal_details,
        'family_details': family_details,
        'educational_details': educational_details,
        'employment_details': employment_details,
        'location_details': location_details,
        'hobbies': personal_details.hobbies.all(),  # Access the hobbies related to PersonalDetails
    })




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails
@never_cache
@login_required(login_url='accounts:login')
def myprofileview(request):
    # Retrieve all the user's profile information
    user = request.user
    personal_details = PersonalDetails.objects.get(user=user)
    family_details = FamilyDetails.objects.get(user=user)
    educational_details = EducationalDetails.objects.get(user=user)
    employment_details = EmploymentDetails.objects.get(user=user)
    location_details = LocationDetails.objects.get(user=user)

    context = {
        'user': user,
        'personal_details': personal_details,
        'family_details': family_details,
        'educational_details': educational_details,
        'employment_details': employment_details,
        'location_details': location_details,
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















