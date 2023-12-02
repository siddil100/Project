from django.shortcuts import render

# Create your views here.


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message
from django.contrib.auth.models import User
from matrimony.models import*
from matint.models import*
from django.db.models import Q





def mychats(request):
    blocked_users = BlockedUser.objects.filter(user=request.user).values_list('blocked_user_id', flat=True)
    not_interested_users = NotInterested.objects.filter(user=request.user).values_list('not_interested_user_id', flat=True)

    excluded_users = list(blocked_users) + list(not_interested_users)

    accepted_interests = Interest.objects.filter(
        receiver=request.user,
        status=Interest.ACCEPTED
    ).exclude(
        Q(sender_id__in=excluded_users) | Q(sender=request.user)
    )

    return render(request, 'matchat/mychats.html', {
        'accepted_interests': accepted_interests,
    })








@login_required
def chat(request, receiver_id):
    receiver = User.objects.get(pk=receiver_id)
    personal_details = PersonalDetails.objects.get(user=receiver)
    
    # Fetching all messages related to the conversation between users
    messages_sent_by_request_user = Message.objects.filter(sender=request.user, receiver=receiver)
    messages_received_by_request_user = Message.objects.filter(sender=receiver, receiver=request.user)
    messages = messages_sent_by_request_user | messages_received_by_request_user
    messages = messages.order_by('timestamp')
    

    for message in messages:
        message.is_incoming = message.receiver == request.user

    return render(request, 'matchat/chat.html', {'receiver': receiver, 'personal_details': personal_details, 'messages': messages})



from django.db.models import BooleanField, Value
from django.shortcuts import get_object_or_404

@login_required
@login_required

def get_messages(request, receiver_id):
    receiver = get_object_or_404(User, pk=receiver_id)
    
    # Retrieve all messages received by the current user from the sender
    messages_received_by_request_user = Message.objects.filter(sender=receiver, receiver=request.user, is_seen=False)
    
    # Mark messages as seen when fetched
    for message in messages_received_by_request_user:
        message.is_seen = True
        message.save()

    # Fetch all messages related to the conversation between users
    messages_sent_by_request_user = Message.objects.filter(sender=request.user, receiver=receiver)
    messages_received_by_request_user = Message.objects.filter(sender=receiver, receiver=request.user)
    messages = messages_sent_by_request_user | messages_received_by_request_user
    messages = messages.order_by('timestamp')

    # Prepare the messages to be returned as JSON
    formatted_messages = []
    for message in messages:
        formatted_messages.append({
            'content': message.content,
            'timestamp': message.timestamp,
            'is_incoming': message.receiver == request.user,
            'is_seen': message.is_seen  # Include the is_seen field in JSON response
        })

    return JsonResponse(formatted_messages, safe=False)


@login_required
def send_message(request, receiver_id):
    if request.method == 'POST':
        receiver = User.objects.get(pk=receiver_id)
        content = request.POST.get('content')

        if content:
            message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
            message.save()

    return redirect('matchat:chat', receiver_id=receiver_id)
