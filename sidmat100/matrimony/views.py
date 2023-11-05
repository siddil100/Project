from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PersonalDetailsForm
from .forms import FamilyDetailsForm
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






from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required  # Import the login_required decorator

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
            return redirect('matrimony:personaldetails')  # Redirect to a success page
        else:
            print(family_details_form.errors)  # Get form errors

    else:
        family_details_form = FamilyDetailsForm()

    return render(request, 'matrimony/familydetails.html', {'family_details_form': family_details_form, 'form_errors': form_errors})







