from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PremiumMembership
from datetime import datetime, timedelta
import razorpay
from django.views.decorators.csrf import csrf_exempt

@login_required
def upgrade_to_premium(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 50000

        client = razorpay.Client(
            auth=("rzp_test_GEoDNWPzqie17l", "9PedkHAJFcBloHLpfJqLxTYN"))

        payment = client.order.create({'amount': amount, 'currency': 'INR','payment_capture': '1'})
    return render(request, 'matpayment/upgrade_membership.html')







from datetime import datetime, timedelta
from django.shortcuts import render
from .models import PremiumMembership

from datetime import datetime, timedelta
from django.shortcuts import render
from .models import PremiumMembership

def paymentsuccess(request):
    if request.method == 'POST':
        current_user = request.user
        payment_id = request.POST.get('payment_id')  # Retrieve the payment ID from the form
        
        # Creating a PremiumMembership object for the current user and storing the payment ID
        premium_membership = PremiumMembership.objects.create(
            user=current_user,
            is_premium=True,
            subscription_date=datetime.now(),
            expiry_date=datetime.now() + timedelta(days=30),
            payment_id=payment_id
        )

        return render(request, "matpayment/paymentsuccess.html")
    else:
        # Handle GET requests or other cases here
        pass









import razorpay
from django.http import JsonResponse
from .models import PremiumMembership
from datetime import datetime, timedelta

from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import PremiumMembership
import razorpay

def process_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        order_id = request.POST.get('order_id')
        
        # Initialize Razorpay client with your API keys
        client = razorpay.Client(auth=('rzp_test_GEoDNWPzqie17l', '9PedkHAJFcBloHLpfJqLxTYN'))

        try:
            # Fetch payment details from Razorpay
            payment = client.payment.fetch(payment_id)
            print(f"Payment Details: {payment}")

            # Validate if the payment was successful
            if payment['status'] == 'captured' and payment['order_id'] == order_id:
                # Update the user's membership status
                user_membership, created = PremiumMembership.objects.get_or_create(user=request.user)
                print(f"User Membership: {user_membership}")

                if not user_membership.is_premium:
                    print("User is not premium, updating membership...")
                    user_membership.is_premium = True
                    user_membership.subscription_date = datetime.now()
                    user_membership.expiry_date = datetime.now() + timedelta(days=30)
                    user_membership.save()
                    print("Membership updated successfully")

                return JsonResponse({'success': True})  # Send a success response after updating membership status
            else:
                return JsonResponse({'success': False, 'message': 'Payment verification failed.'})
        except Exception as e:
            print(f"Exception occurred: {e}")
            return JsonResponse({'success': False, 'message': str(e)})  # Handle other exceptions generically

    return JsonResponse({'success': False, 'message': 'Invalid request.'})




def view_premium(request):
    try:
        # Retrieve the PremiumMembership instance for the current user
        premium_membership = PremiumMembership.objects.get(user=request.user)
    except PremiumMembership.DoesNotExist:
        premium_membership = None

    context = {
        'premium_membership': premium_membership,
    }

    return render(request, 'matpayment/view_premium.html', context)


