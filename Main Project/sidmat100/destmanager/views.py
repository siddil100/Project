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



from django.db.models import Q



def custom_booking_list(request):
    # Get the event manager associated with the logged-in user
    current_user = request.user
    try:
        event_manager = EventManager.objects.get(user=current_user)
        location = event_manager.location

        # Filter custom package bookings based on the location of the event manager
        custom_package_bookings = CustomPackageBooking.objects.filter(Q(location__iexact=location) | Q(location__icontains=location))
        
        # Check if the user has a valid license
        if License.objects.filter(user=current_user, is_valid=True).exists():
            custom_package_bookings = CustomPackageBooking.objects.filter(Q(location__iexact=location) | Q(location__icontains=location))
        else:
            # Redirect to upload_license view if is_valid is not true
            return redirect('destmanager:upload_license')
    except EventManager.DoesNotExist:
        # Handle the case where the current user is not associated with any event manager
        custom_package_bookings = []

    return render(request, 'destmanager/custom_bookinglist.html', {'custom_package_bookings': custom_package_bookings})




from django.shortcuts import render, get_object_or_404
from myadmin.models import *
@never_cache
@login_required(login_url='accounts:login')
def view_package(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    return render(request, 'destmanager/view_package.html', {'package': package})





def view_custom_package(request, pk):
    # Retrieve the custom package booking object
    custom_package = get_object_or_404(CustomPackageBooking, pk=pk)

    return render(request, 'destmanager/view_custom_package.html', {'custom_package': custom_package})


from myadmin.forms import *



@login_required(login_url='accounts:login')
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

@login_required(login_url='accounts:login')
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
            # Print form errors to the console
            print(form.errors)
    else:
        form = FoodOptionForm()
    return render(request, 'destmanager/add_food_item.html', {'form': form})





from .forms import DecorationOptionForm  

@login_required(login_url='accounts:login')
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






from .forms import EventOptionForm  

@login_required(login_url='accounts:login')


def add_events(request):
    # Check if the user has a valid license
    if not License.objects.filter(user=request.user, is_valid=True).exists():
        return redirect('destmanager:upload_license')

    if request.method == 'POST':
        form = EventOptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('destmanager:eventhome')
        else:
            # Print form errors to the console
            print(form.errors)
            
    else:
        form = DecorationOptionForm()
    return render(request, 'destmanager/add_events.html', {'form': form})






from django.shortcuts import render, redirect
from .models import License
from .forms import LicenseForm
import logging

logger = logging.getLogger(__name__)

@login_required(login_url='accounts:login')
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





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def check_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        existing_license = License.objects.filter(phone=phone_number).exists()
        return JsonResponse({'exists': existing_license})
    return JsonResponse({'error': 'Invalid request'}, status=400)






def list_scheduling(request):
    # Check if the user has a valid license
    if not License.objects.filter(user=request.user, is_valid=True).exists():
        return redirect('destmanager:upload_license')  # Redirect to upload license view

    # If the license is valid, proceed with listing schedulings
    schedulings = Scheduling.objects.all()
    return render(request, 'destmanager/list_scheduling.html', {'schedulings': schedulings})




from .models import Scheduling

def update_scheduling(request, scheduling_id):
    scheduling = get_object_or_404(Scheduling, pk=scheduling_id)
    
    if request.method == 'POST':
        scheduling.location = request.POST.get('location')
        scheduling.limit = request.POST.get('limit')
        scheduling.save()
        return redirect('destmanager:eventhome')  # Redirect to wherever you want after update
    
    return render(request, 'destmanager/update_scheduling.html', {'scheduling': scheduling})





from destpayment.models import PackageBooking, CustomPackageBooking
from myadmin.models import EventManager
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Image
from django.http import HttpResponse
from django.utils import timezone
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from reportlab.lib.units import inch
from django.templatetags.static import static
from django.conf import settings








def generate_package_reports(request):
    current_user = request.user
    
    try:
        event_manager = EventManager.objects.get(user=current_user)
        location = event_manager.location
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="package_report.pdf"'

        # Create a PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Add site logo to top left
        image_path = settings.BASE_DIR / 'static' / 'images' / 'logo.jpg'

# Load the image using the absolute file path
        logo = Image(image_path, width=1*inch, height=1*inch)
        elements.append(logo)

        # Header with site name
        header_data = [['DreamWed']]
        header_table = Table(header_data)
        header_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                          ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                          ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                                          ('FONTSIZE', (0, 0), (-1, -1), 16)]))
        elements.append(header_table)
        
        # Add spacing
        elements.append(Spacer(1, 12))

        # Filter package bookings based on the location of the event manager
        package_bookings = PackageBooking.objects.filter(package__location=location)

        # Define table data for package bookings
        package_data = [['Package Name', 'Date', 'Package Type', 'Location', 'Price']]

        for booking in package_bookings:
            package_name = booking.package.package_name
            date = booking.event_date.strftime('%Y-%m-%d %H:%M:%S')
            package_type = "Package"  # Assuming it's a package
            location = booking.package.location  # Assuming Package model has a 'location' field
            price = booking.package.price

            # Append data to the table
            package_data.append([package_name, date, package_type, location, price])

        # Create table for package bookings
        package_table = Table(package_data)
        package_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                           ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                           ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        # Add package bookings table to the PDF document
        elements.append(package_table)

        # Footer with issue date
        footer_data = [[f"Issue Date: {datetime.now().strftime('%Y-%m-%d')}"]]
        footer_table = Table(footer_data)
        footer_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                          ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                          ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                                          ('FONTSIZE', (0, 0), (-1, -1), 10)]))
        elements.append(footer_table)

        # Build the PDF document
        doc.build(elements)
        return response
    
    except EventManager.DoesNotExist:
        # Handle case where the current user is not an event manager
        return HttpResponse("You are not an event manager.")

