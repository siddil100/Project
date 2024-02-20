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

def payment_success(request):
    if request.method == 'POST':
        current_user = request.user
        payment_id = request.POST.get('payment_id')  # Retrieve the payment ID from the form
        package_id = request.POST.get('package_id')  # Retrieve the package ID from the form
        
        # Creating a PackageBooking object for the current user and storing the payment ID
        package_booking = PackageBooking.objects.create(
            user=current_user,
            package_id=package_id,
            payment_id=payment_id,
            subscription_date=timezone.now()
        )

        return render(request, "destpayment/payment_success.html")
    else:
        # Handle GET requests or other cases here
        pass
