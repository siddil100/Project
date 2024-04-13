from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import PackageBooking, Package
import razorpay

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Package
import razorpay

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import PackageBooking
from datetime import datetime, timedelta
import razorpay
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Package
import razorpay

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Package
import razorpay


from django.http import JsonResponse
from django.utils import timezone
from .models import PackageBooking
import razorpay


from django.http import HttpResponseBadRequest
@login_required(login_url='accounts:login')
def book_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    amount = package.price

    client = razorpay.Client(auth=("rzp_test_GEoDNWPzqie17l", "9PedkHAJFcBloHLpfJqLxTYN"))

    event_date = request.GET.get('date')
    if event_date:
        print("date is$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",event_date)  # Debugging print statement

    if request.method == "POST":
        # Validate and sanitize event_date if necessary
        if not event_date:
            return HttpResponseBadRequest('Event date is missing')

        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        return render(request, 'destpayment/book_package.html', {'package': package, 'event_date': event_date, 'payment': payment})
    else:
        return render(request, 'destpayment/book_package.html', {'package': package,'event_date': event_date,})
    





from django.shortcuts import render
from destmanager.models import FoodOption, DecorationOption, EventOption
from destmanager.forms import BookingForm  # Assuming you have a BookingForm defined in forms.py




def proceed_tocustom(request):
    return render(request, 'destpayment/proceed_tocustom.html')

from django.db.models import Max
# views.py

def custom_package(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Set the user ID
            
            # Generate a unique package name starting with "custom"
            latest_package = CustomPackageBooking.objects.aggregate(Max('id'))['id__max']
            latest_id = 1 if latest_package is None else latest_package + 1
            package_name = f"custom{latest_id}"
            booking.package_name = package_name
            
            booking.save()
            form.save_m2m()
            
            # Redirect to custom_bookpackage view with the package ID
            return redirect('destpayment:custom_bookpackage', package_id=booking.id)
        else:
            print("Form errors:", form.errors)  # Print form errors to console
    else:
        form = BookingForm()

    # Fetch choices with images for rendering the form
    decor_choices_with_images = [(choice.id, f"{choice.name} ({choice.type},  {choice.description}, INR ₹ {choice.price} Per Sq Ft)", choice.image.url) for choice in DecorationOption.objects.all()]
    event_choices_with_images = [(choice.id, f"{choice.name} ({choice.category},  {choice.description}, INR ₹ {choice.price} Per event )", choice.image.url) for choice in EventOption.objects.all()]
    food_choices_with_images = [(choice.id, f"{choice.name} ({choice.category},  {choice.description}, INR ₹ {choice.price} Per Plate)", choice.image.url) for choice in FoodOption.objects.all()]

    return render(request, 'destpayment/custom_package.html', {
        'form': form,
        'decor_choices': decor_choices_with_images,
        'event_choices': event_choices_with_images,
        'food_choices': food_choices_with_images
    })









def get_decor_price(request):
    decor_id = request.GET.get('id')
    decor = DecorationOption.objects.get(id=decor_id)
    return JsonResponse({'price': decor.price})

def get_event_price(request):
    event_id = request.GET.get('id')
    event = EventOption.objects.get(id=event_id)
    return JsonResponse({'price': event.price})

def get_food_price(request):
    food_id = request.GET.get('id')
    food = FoodOption.objects.get(id=food_id)
    return JsonResponse({'price': food.price})






  






from django.shortcuts import render, redirect
from django.utils import timezone
from .models import PackageBooking
from destmanager.models import *
import datetime
from django.db.models import F



@login_required(login_url='accounts:login')
def payment_success(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        current_user = request.user
        payment_id = request.POST.get('payment_id')  # Retrieve the payment ID from the form
        package_id = request.POST.get('package_id')  # Retrieve the package ID from the form
        event_date = request.POST.get('event_date')  # Retrieve the event date from the form
        print("Event Date received in view:", event_date) 
        
        try:
            # Check if a PackageBooking object already exists for the user and the same package ID
            package_booking = PackageBooking.objects.get(user=current_user, package_id=package_id)
            # Update the existing PackageBooking object with the new payment ID, package ID, and event date
            package_booking.payment_id = payment_id
            package_booking.subscription_date = timezone.now()
            package_booking.event_date = event_date  # Set the event date
            package_booking.save()



            try:
                scheduling = Scheduling.objects.get(location=package_booking.package.location)
                scheduling_booking = SchedulingBooking.objects.get(location=scheduling, date=event_date)
                
                scheduling_booking.booking_count = F('booking_count') + 1
                scheduling_booking.limit = scheduling.limit
                scheduling_booking.save()
            except Scheduling.DoesNotExist:
    # If there is no corresponding Scheduling for the location, handle it accordingly
                pass
                
                # Create a new SchedulingBooking instance if none exists for the location and date
            except SchedulingBooking.DoesNotExist:
    # Create a new SchedulingBooking instance if none exists for the location and date
                scheduling_booking = SchedulingBooking.objects.create(
                    location=package_booking.package.location,
                    booking_count=1,  # Initial booking count is 1
                    limit=scheduling.limit,  # Set limit based on Scheduling
                    date=event_date  # Set the event date
                )
        except PackageBooking.DoesNotExist:
            # Create a new PackageBooking object if none exists for the user with the same package ID
            package_booking = PackageBooking.objects.create(
                user=current_user,
                package_id=package_id,
                payment_id=payment_id,
                subscription_date=timezone.now(),
                event_date=event_date  # Set the event date
            )
            
            # Update the corresponding SchedulingBooking instance
            try:
                scheduling = Scheduling.objects.get(location=package_booking.package.location)
                scheduling_booking = SchedulingBooking.objects.get(location=scheduling, date=event_date)
                
                scheduling_booking.booking_count = F('booking_count') + 1
                scheduling_booking.limit = scheduling.limit
                scheduling_booking.save()
            except Scheduling.DoesNotExist:
    # If there is no corresponding Scheduling for the location, handle it accordingly
                pass
                
                # Create a new SchedulingBooking instance if none exists for the location and date
            except SchedulingBooking.DoesNotExist:
    # Create a new SchedulingBooking instance if none exists for the location and date
                scheduling_booking = SchedulingBooking.objects.create(
                    location=package_booking.package.location,
                    booking_count=1,  # Initial booking count is 1
                    limit=scheduling.limit,  # Set limit based on Scheduling
                    date=event_date  # Set the event date
                )


        pdf_response = generate_pdf_receipt(package_booking)

        # Redirect to another view after generating the PDF
        return redirect('destpayment:render_payment_success')
    else:
        # Handle GET requests or other cases here
        pass





from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomPackageBooking


import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
import base64



def custompayment_success(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        current_user = request.user
        payment_id = request.POST.get('payment_id')  # Retrieve the payment ID from the form
        package_id = request.POST.get('package_id')  # Retrieve the package ID from the form

        # Retrieve the CustomPackageBooking object based on the package_id and current_user
        booking = CustomPackageBooking.objects.filter(user=current_user, id=package_id).first()

        if booking:
            booking.payment_id = payment_id
            booking.save()

            # Generate PDF receipt
            pdf_data = generate_custom_receipt(booking)

            # Save PDF receipt to the model
            filename = f"receipt_{booking.id}.pdf"  # Unique filename for each receipt
            booking.receipt.save(filename, ContentFile(pdf_data))



            subscription_date_formatted = booking.subscription_date.strftime("%d-%m-%Y")
            event_date_formatted = booking.event_date.strftime("%d-%m-%Y")
            event_date_from_formatted = booking.event_datefrom.strftime("%d-%m-%Y")
            event_date_to_formatted = booking.event_dateto.strftime("%d-%m-%Y")
            # Generate QR code with booked package details
            package_details = f"Package ID: {booking.id}, UserName: {current_user.username}, Subscription Date: {subscription_date_formatted}, Event Date: {event_date_formatted}, Payment ID: {booking.payment_id}, Package Name: {booking.package_name}, Decor Type: {', '.join([str(decor) for decor in booking.decor_type.all()])}, Event Type: {', '.join([str(event) for event in booking.event_type.all()])}, Food Type: {', '.join([str(food) for food in booking.food_type.all()])}, Price: {booking.price}, Attendees: {booking.attendees}, Location: {booking.location}, Event Date From: {event_date_from_formatted}, Event Date To: {event_date_to_formatted}"
            qr = qrcode.make(package_details)

            # Convert QR code image to bytes
            buffer = BytesIO()
            
            qr.save(buffer, format='PNG')
            qr_image_data = buffer.getvalue()
            qr_image_base64 = base64.b64encode(qr_image_data).decode()

            # Render template with QR code image data
            context = {
                'qr_code': qr_image_base64,
            }
            html_content = render_to_string('destpayment/custompayment_success.html', context)

            return HttpResponse(html_content)
        else:
            messages.error(request, 'Booking not found or does not belong to the current user.')
            return redirect('destpayment:error_page')  # Redirect to error_page in destpayment app
    else:
        # Handle GET requests or other cases here
        pass










    

    from django.shortcuts import render




@login_required(login_url='accounts:login')
def render_payment_success(request):
    return render(request, "destpayment/payment_success.html")


def render_custompayment_success(request):
    return render(request, "destpayment/custompayment_success.html")






from django.http import HttpResponse
from .models import PackageBooking
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
import io
from django.core.files.base import ContentFile


@login_required(login_url='accounts:login')
def generate_pdf_receipt(package_booking):
    buffer = io.BytesIO()  # Create a buffer to store the PDF content

    # Create PDF document
    p = canvas.Canvas(buffer, pagesize=letter)

    # Add bold heading at center on top of the PDF
    heading_style = ParagraphStyle(name='Heading', fontSize=16, alignment=1, fontName='Helvetica-Bold')
    heading = Paragraph("<br/><br/><br/><br/><b>DreamWed Receipt</b>", heading_style)
    heading.wrapOn(p, 500, 100)
    heading.drawOn(p, 50, 750)

    # Draw a border around the content
    p.rect(50, 590, 500, 150)  # Adjust coordinates and dimensions as needed

    # Write package details to PDF
    p.drawString(100, 700, f'Package Name: {package_booking.package.package_name}')
    p.drawString(100, 680, f'Package Price: {package_booking.package.price}')  # Include package price
    p.drawString(100, 660, f'Payment ID: {package_booking.payment_id}')
    p.drawString(100, 640, f'Subscription Date: {package_booking.subscription_date}')

    p.showPage()
    p.save()

    # Save the PDF content to the package_booking's receipt field
    package_booking.receipt.save('receipt.pdf', ContentFile(buffer.getvalue()))

    return HttpResponse(buffer.getvalue(), content_type='application/pdf')





@login_required(login_url='accounts:login')
def download_pdf(request):
    # Retrieve the last stored PackageBooking object associated with the current user
    current_user = request.user
    try:
        package_booking = PackageBooking.objects.filter(user=current_user).latest('id')
    except PackageBooking.DoesNotExist:
        # Handle the case where no package booking exists for the user
        return HttpResponse("No package booking found for this user.")

    # Generate PDF content based on the package booking details
    pdf_response = generate_pdf_receipt(package_booking)

    return pdf_response





def download_custompdf(request):
    # Retrieve the last stored PackageBooking object associated with the current user
    current_user = request.user
    try:
        package_booking = CustomPackageBooking.objects.filter(user=current_user).latest('id')
    except CustomPackageBooking.DoesNotExist:
        # Handle the case where no package booking exists for the user
        return HttpResponse("No package booking found for this user.")

    # Generate PDF content based on the package booking details
    pdf_data = generate_custom_receipt(package_booking)

    # Create a FileResponse and return the PDF data
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="custom_receipt.pdf"'
    return response





import io
from reportlab.pdfgen import canvas
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_custom_receipt(package_booking):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Set font and size
    bold_font = "Helvetica-Bold"
    regular_font = "Helvetica"
    font_size = 12
    p.setFont(bold_font, font_size)

    # Add background color
    p.setFillColorRGB(0.9, 0.9, 0.9)  # Light gray
    p.rect(0, 0, 700, 850, fill=1)

    # Add border around the page
    p.setStrokeColor(colors.black)
    p.rect(10, 10, 580, 800)

    # Add heading to the receipt
    p.setFillColor(colors.black)  # Set font color to black
    p.drawCentredString(300, 750, "DreamWed - Receipt for Package Booking")


    user_first_name = package_booking.user.personaldetails.first_name
    user_last_name = package_booking.user.personaldetails.last_name
    user_full_name = f"{user_first_name} {user_last_name}"

    # Add user and payment information
    user_info = f"User: {user_full_name}"
    payment_id = f"Payment ID: {package_booking.payment_id}"
    p.setFont(regular_font, font_size)
    p.setFillColor(colors.black)  # Set font color to black
    p.drawString(100, 700, user_info)
    p.drawString(100, 680, payment_id)

    # Format event date as day-month-year
    event_date = package_booking.event_date.strftime("%d-%b-%Y")

    # Add event date information
    p.drawString(100, 660, f"Event Date: {event_date}")

    # Fetch related objects directly
    event_option_names = [event.name for event in package_booking.event_type.all()]
    decor_option_names = [decor.name for decor in package_booking.decor_type.all()]
    food_option_names = [food.name for food in package_booking.food_type.all()]

    # Prepare data for the table
    data = [
        ["Event Type", ", ".join(event_option_names)],
        ["Decoration Type", ", ".join(decor_option_names)],
        ["Food Type", ", ".join(food_option_names)],
    ]

    # Create table and set style
    table = Table(data, colWidths=[150, 350])
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), regular_font),
        ('FONTSIZE', (0, 0), (-1, -1), font_size),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),  # Table background color
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),  # Table inner grid
        ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Table border
    ]))

    # Draw the table on the canvas
    table.wrapOn(p, 400, 300)
    table.drawOn(p, 50, 480)

    # Calculate total price based on attendees
    attendees = package_booking.attendees
    event_price = sum(event.price for event in package_booking.event_type.all())
    decor_price = sum(decor.price for decor in package_booking.decor_type.all())
    food_price = sum(food.price for food in package_booking.food_type.all())
    total_price = (event_price + decor_price + food_price) * attendees

    # Draw total price information
    p.setFillColor(colors.black)  # Set font color to black
    p.drawString(100, 450, f"Price per attendee: INR {total_price / attendees:.2f}")
    p.drawString(100, 430, f"Total Price for {attendees} attendees: INR {total_price:.2f}")

    # Draw current date at the bottom
    today_date = datetime.now().strftime("%d-%b-%Y")
    p.setFont(regular_font, 10)
    p.setFillColor(colors.black)  # Set font color to black
    p.drawRightString(550, 20, f"Issue Date: {today_date}")

    # Save and return PDF data
    p.showPage()
    p.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data













from .models import CustomPackageBooking

def custom_bookpackage(request, package_id):
    
    
    # Get the CustomPackageBooking object based on its ID
    package = get_object_or_404(CustomPackageBooking, id=package_id)
    
    amount = package.price
    print(f"Amount from booking ID {package_id}: {amount}")

    client = razorpay.Client(auth=("rzp_test_GEoDNWPzqie17l", "9PedkHAJFcBloHLpfJqLxTYN"))

    if request.method == "POST":
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        return render(request, 'destpayment/custom_bookpackage.html', {'package': package, 'payment': payment})
    else:
        return render(request, 'destpayment/custom_bookpackage.html', {'package': package})















