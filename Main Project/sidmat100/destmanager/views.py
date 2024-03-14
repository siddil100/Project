from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

# Create your views here.


@never_cache
@login_required(login_url='accounts:login')
def eventhome(request):
    return render(request, 'destmanager/eventhome.html')


from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from accounts.forms import ChangePasswordForm
class MyPasswordChangeView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'destmanager/change_password.html'  
    success_url = reverse_lazy('destmanager:eventhome')  




# views.py

from django.shortcuts import render
from destpayment.models import *
@never_cache
@login_required(login_url='accounts:login')
def package_booking_list(request):
    # Get the event manager associated with the logged-in user
    current_user = request.user
    try:
        event_manager = EventManager.objects.get(user=current_user)
        location = event_manager.location
        # Filter package bookings based on the location of the event manager
        package_bookings = PackageBooking.objects.filter(package__location=location)
        
        # Check if the user has a valid license
        if License.objects.filter(user=current_user, is_valid=True).exists():
            package_bookings = PackageBooking.objects.filter(package__location=location)
        else:
            # Redirect to upload_license view if is_valid is not true
            return redirect('destmanager:upload_license')
    except EventManager.DoesNotExist:
        # Handle the case where the current user is not associated with any event manager
        package_bookings = []

    return render(request, 'destmanager/package_booking_list.html', {'package_bookings': package_bookings})




from django.shortcuts import render, get_object_or_404
from myadmin.models import *
@never_cache
@login_required(login_url='accounts:login')
def view_package(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    return render(request, 'destmanager/view_package.html', {'package': package})


from myadmin.forms import *



def edit_package(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            return redirect('destmanager:eventhome')  # Redirect to package detail page after editing
    else:
        form = PackageForm(instance=package)
    return render(request, 'destmanager/edit_package.html', {'form': form})





from django.shortcuts import render, redirect
from .forms import FoodOptionForm

def add_food_item(request):
    # Check if the user has a valid license
    if not License.objects.filter(user=request.user, is_valid=True).exists():
        return redirect('destmanager:upload_license')

    if request.method == 'POST':
        form = FoodOptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('destmanager:eventhome')
    else:
        form = FoodOptionForm()
    return render(request, 'destmanager/add_food_item.html', {'form': form})





from .forms import DecorationOptionForm  

def add_decorations(request):
     # Check if the user has a valid license
    if not License.objects.filter(user=request.user, is_valid=True).exists():
        return redirect('destmanager:upload_license')


    if request.method == 'POST':
        form = DecorationOptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('destmanager:eventhome')
    else:
        form = DecorationOptionForm()
    return render(request, 'destmanager/add_decorations.html', {'form': form})





from django.shortcuts import render, redirect
from .models import License
from .forms import LicenseForm
import logging

logger = logging.getLogger(__name__)
def upload_license(request):
    user = request.user
    try:
        existing_license = License.objects.get(user=user)
    except License.DoesNotExist:
        existing_license = None

    if request.method == 'POST':
        form = LicenseForm(request.POST, request.FILES, instance=existing_license)
        if form.is_valid():
            license_instance = form.save(commit=False)
            license_instance.user = user
            license_instance.is_valid = False 
            license_instance.save()
            return redirect('destmanager:eventhome')
        else:
            # Print errors to console
            logger.error(form.errors)
    else:
        form = LicenseForm(instance=existing_license)
    return render(request, 'destmanager/upload_license.html', {'form': form})
