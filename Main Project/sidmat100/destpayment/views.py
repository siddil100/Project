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



@login_required(login_url='accounts:login')
def book_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    amount = package.price

    client = razorpay.Client(
            auth=("rzp_test_GEoDNWPzqie17l", "9PedkHAJFcBloHLpfJqLxTYN"))

    if request.method == "POST":
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        return render(request, 'destpayment/book_package.html', {'package': package, 'payment': payment})
    else:
        return render(request, 'destpayment/book_package.html', {'package': package})







@login_required(login_url='accounts:login')
def process_booking_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        order_id = request.POST.get('order_id')
        package_id = request.POST.get('package_id')  # Assuming you are passing package_id from the frontend
        
        # Initialize Razorpay client with your API keys
        client = razorpay.Client(auth=('rzp_test_GEoDNWPzqie17l', '9PedkHAJFcBloHLpfJqLxTYN'))

        try:
            # Fetch payment details from Razorpay
            payment = client.payment.fetch(payment_id)
            print(f"Payment Details: {payment}")

            # Validate if the payment was successful
            if payment['status'] == 'captured' and payment['order_id'] == order_id:
                # Update the PackageBooking with payment ID
                package_booking = PackageBooking.objects.create(
                    user=request.user,
                    package_id=package_id,
                    payment_id=payment_id,
                    subscription_date=timezone.now()
                )
                print("Package booking created successfully")

                return JsonResponse({'success': True})  # Send a success response after creating the package booking
            else:
                return JsonResponse({'success': False, 'message': 'Payment verification failed.'})
        except Exception as e:
            print(f"Exception occurred: {e}")
            return JsonResponse({'success': False, 'message': str(e)})  # Handle other exceptions generically

    return JsonResponse({'success': False, 'message': 'Invalid request.'})







from django.shortcuts import render, redirect
from django.utils import timezone
from .models import PackageBooking
import datetime



@login_required(login_url='accounts:login')
def payment_success(request):
    if request.method == 'POST':
        current_user = request.user
        payment_id = request.POST.get('payment_id')  # Retrieve the payment ID from the form
        package_id = request.POST.get('package_id')  # Retrieve the package ID from the form
        
        try:
            # Check if a PackageBooking object already exists for the user and the same package ID
            package_booking = PackageBooking.objects.get(user=current_user, package_id=package_id)
            # Update the existing PackageBooking object with the new payment ID and package ID
            package_booking.payment_id = payment_id
            package_booking.subscription_date = timezone.now()
            package_booking.save()
        except PackageBooking.DoesNotExist:
            # Create a new PackageBooking object if none exists for the user with the same package ID
            package_booking = PackageBooking.objects.create(
                user=current_user,
                package_id=package_id,
                payment_id=payment_id,
                subscription_date=timezone.now()
            )

        pdf_response = generate_pdf_receipt(package_booking)

        # Redirect to another view after generating the PDF
        return redirect('destpayment:render_payment_success')
    else:
        # Handle GET requests or other cases here
        pass









    

    from django.shortcuts import render




@login_required(login_url='accounts:login')
def render_payment_success(request):
    return render(request, "destpayment/payment_success.html")






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




















