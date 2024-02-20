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
    packages = Package.objects.all()
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
            response_message = "Here is the link to view packages: <a href='{}'>View Packages</a>".format(reverse('matdest:view_packages'))
            return JsonResponse({'response_message': response_message})

        # Implement your logic here to determine the redirect URL based on the message
        if message.lower() == 'premium':
            response_message = "Click to get more details of premium: <a href='{}'>Premium</a>".format(reverse('matpayment:view_premium'))
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




