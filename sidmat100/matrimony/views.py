from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PersonalDetailsForm
from .forms import FamilyDetailsForm
from .forms import EducationalDetailsForm
from .forms import EmploymentDetailsForm
from .forms import LocationDetailsForm
from django.http import JsonResponse

from .models import PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails



def check_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        exists = PersonalDetails.objects.filter(phone_number=phone_number).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})


@login_required
def personaldetailsview(request):
    user = request.user

    # Check if the PersonalDetails form is already filled
    if PersonalDetails.objects.filter(user=user, perso_fill=True).exists():
        # PersonalDetails form is already filled, move to the next form
        return redirect('matrimony:familydetails')

    if request.method == 'POST':
        personal_details_form = PersonalDetailsForm(request.POST, request.FILES)
        if personal_details_form.is_valid():
            personal_details = personal_details_form.save(commit=False)
            personal_details.user = user
            personal_details.perso_fill = True
            personal_details.save()
            return redirect('matrimony:familydetails')  # Move to the next form

    else:
        personal_details_form = PersonalDetailsForm()

    return render(request, 'matrimony/personaldetails.html', {'personal_details_form': personal_details_form})












@login_required
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




@login_required
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




@login_required
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



@login_required
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
        if personal_details.gender == 'male':
            opposite_gender = 'female'
        else:
            opposite_gender = 'male'

        # Get a list of user profiles (excluding the currently logged-in user) based on gender
        profiles = PersonalDetails.objects.filter(perso_fill=True, gender=opposite_gender).exclude(user=user)
        
        return render(request, 'matrimony/home.html', {'profile_image_url': profile_image_url, 'profiles': profiles})

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










