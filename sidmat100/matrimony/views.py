from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PersonalDetailsForm
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
        personal_details_form = PersonalDetailsForm(request.POST)

        if personal_details_form.is_valid():
            personal_details = personal_details_form.save(commit=False)
            personal_details.user = request.user  # Link to the current user
            personal_details.save()
            return redirect('success_url')  # Redirect to a success page

    else:
        personal_details_form = PersonalDetailsForm()

    return render(request, 'matrimony/personaldetails.html', {'personal_details_form': personal_details_form})

