from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PersonalDetailsForm
from .forms import FamilyDetailsForm
from .forms import EducationalDetailsForm
from .forms import EmploymentDetailsForm
from .forms import LocationDetailsForm
from django.http import JsonResponse
from .models import PersonalDetails


def check_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        exists = PersonalDetails.objects.filter(phone_number=phone_number).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})


@login_required
def personaldetailsview(request):
    if request.method == 'POST':
        personal_details_form = PersonalDetailsForm(request.POST, request.FILES)

        if personal_details_form.is_valid():
            personal_details = personal_details_form.save(commit=False)
            personal_details.user = request.user  # Link to the current user
            personal_details.perso_fill = True
            personal_details.save()
            return redirect('matrimony:familydetails')  # Redirect to a success page

    else:
        personal_details_form = PersonalDetailsForm()
        print(personal_details_form.errors)

    return render(request, 'matrimony/personaldetails.html', {'personal_details_form': personal_details_form})












@login_required  # Use the login_required decorator to ensure the user is logged in
def familydetailsview(request):
    form_errors = None  # Initialize the form_errors variable

    if request.method == 'POST':
        family_details_form = FamilyDetailsForm(request.POST)
        if family_details_form.is_valid():
            family_details = family_details_form.save(commit=False)

            # You can directly set the user field to the current user
            family_details.user = request.user

            family_details.famil_fill = True
            family_details.save()
            return redirect('matrimony:educationaldetails')  # Redirect to a success page
        else:
            print(family_details_form.errors)  # Get form errors

    else:
        family_details_form = FamilyDetailsForm()

    return render(request, 'matrimony/familydetails.html', {'family_details_form': family_details_form, 'form_errors': form_errors})




def educationaldetailsview(request):
    form_errors = None  

    if request.method == 'POST':
        educational_details_form = EducationalDetailsForm(request.POST)
        if educational_details_form.is_valid():
            educational_details = educational_details_form.save(commit=False)

            
            educational_details.user = request.user

            educational_details.educ_fill = True
            educational_details.save()
            return redirect('matrimony:employmentdetails')  
        else:
            print(educational_details_form.errors)  

    else:
        educational_details_form = EducationalDetailsForm()

    return render(request, 'matrimony/educationaldetails.html', {'educational_details_form': educational_details_form, 'form_errors': form_errors})




def employmentdetailsview(request):
    form_errors = None

    if request.method == 'POST':
        employment_details_form = EmploymentDetailsForm(request.POST)
        if employment_details_form.is_valid():
            employment_details = employment_details_form.save(commit=False)

            employment_details.user = request.user

            employment_details.empl_fill = True
            employment_details.save()
            return redirect('matrimony:locationdetails')
        else:
            print(employment_details_form.errors)

    else:
        employment_details_form = EmploymentDetailsForm()

    return render(request, 'matrimony/employmentdetails.html', {'employment_details_form': employment_details_form, 'form_errors': form_errors})




def locationdetailsview(request):
    form_errors = None

    if request.method == 'POST':
        location_details_form = LocationDetailsForm(request.POST, request.FILES)  # Note the use of request.FILES for file upload
        if location_details_form.is_valid():
            location_details = location_details_form.save(commit=False)

            location_details.user = request.user

            location_details.loca_fill = True
            location_details.save()
            return redirect('matrimony:success_page')
        else:
            print(location_details_form.errors)
            form_errors = location_details_form.errors  # Store the form errors

    else:
        location_details_form = LocationDetailsForm()

    return render(request, 'matrimony/locationdetails.html', {'location_details_form': location_details_form, 'form_errors': form_errors})








