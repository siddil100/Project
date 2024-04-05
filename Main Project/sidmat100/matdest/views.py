from django.shortcuts import redirect, render

# matdest/views.py

from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required



@never_cache
@login_required(login_url='accounts:login')
def desthome(request):
    return render(request, 'matdest/desthome.html')



from django.shortcuts import render
from myadmin.models import Package


@never_cache
@login_required(login_url='accounts:login')
def view_packages(request):
    # Retrieve all packages initially
    packages = Package.objects.filter(pack_status=True)

    # Handle filters if provided in the request
    location = request.GET.get('location')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if location:
        packages = packages.filter(location__icontains=location)
    if min_price:
        packages = packages.filter(price__gte=min_price)
    if max_price:
        packages = packages.filter(price__lte=max_price)

    return render(request, 'matdest/view_packages.html', {'packages': packages})



from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse

from django.http import JsonResponse
from django.urls import reverse

from django.http import JsonResponse
from django.urls import reverse

from django.http import JsonResponse
from django.urls import reverse

@never_cache
@login_required(login_url='accounts:login')
def chatbot_redirect(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        # Check if the message is a greeting
        if message.lower() in ['hello', 'hai', 'hi', 'hola']:
            response_message = "How can I help you?"
            return JsonResponse({'response_message': response_message})

        # Check if the message contains the word 'packages' or 'package'
        if 'packages' in message.lower() or 'package' in message.lower():
            # If 'packages' is found in the message, construct the response with a link to view packages
            view_packages_link = reverse('matdest:view_packages')
            booked_packages_link = reverse('matdest:my_packages')

            response_message = "Here are some matching links:<br>"
            response_message += f"<a href='{view_packages_link}'>View Packages</a><br>"
            response_message += f"<a href='{booked_packages_link}'>Show Booked Packages</a>"
            return JsonResponse({'response_message': response_message})

        # Implement your logic here to determine the redirect URL based on the message
        if message.lower() == 'premium':
            response_message = "Click to get more details of premium: <a href='{}'>Premium</a>".format(reverse('matpayment:view_premium'))
            return JsonResponse({'response_message': response_message})
        
        if message.lower() == 'booking':
            response_message = "Click to get more details of booked packages: <a href='{}'>My Bookings</a>".format(reverse('matdest:my_packages'))
            return JsonResponse({'response_message': response_message})
        
        if 'chat' in message.lower() or 'chats' in message.lower() or 'message' in message.lower():
            response_message = "Click to get mychats: <a href='{}'>Chats</a>".format(reverse('matchat:mychats'))
            return JsonResponse({'response_message': response_message})
        else:
            redirect_url = '/path/to/default/view/'  # Replace with the default URL

        # If the message doesn't match any predefined responses, construct a default response
        default_response = "Sorry, your query didn't match any of our options."
        return JsonResponse({'response_message': default_response})
    else:
        # If the request method is not POST, return an error response
        return JsonResponse({'error': 'Invalid request method'}, status=400)







from django.shortcuts import render
from destpayment.models import PackageBooking


@never_cache
@login_required(login_url='accounts:login')
def view_my_packages(request):
    user_packages = PackageBooking.objects.filter(user=request.user)
    return render(request, 'matdest/my_packages.html', {'user_packages': user_packages})




from django.shortcuts import render, get_object_or_404
@never_cache
@login_required(login_url='accounts:login')
def view_package_details(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    return render(request, 'matdest/view_package_details.html', {'package': package})


