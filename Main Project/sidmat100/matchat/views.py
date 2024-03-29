from django.shortcuts import render

# Create your views here.


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from .models import Message
from django.contrib.auth.models import User
from matrimony.models import*
from matint.models import*
from django.db.models import Q





from django.db.models import Count
@never_cache
@login_required(login_url='accounts:login')
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

    # Retrieve the count of unseen messages for each user in accepted interests
    unseen_messages_counts = {}
    for interest in accepted_interests:
        unseen_count = Message.objects.filter(
            sender=interest.sender,
            receiver=request.user,
            is_seen=False
        ).count()
        unseen_messages_counts[interest.sender.id] = unseen_count

    return render(request, 'matchat/mychats.html', {
        'accepted_interests': accepted_interests,
        'unseen_messages_counts': unseen_messages_counts,
    })









@never_cache
@login_required(login_url='accounts:login')
def chat(request, receiver_id):
    receiver = User.objects.get(pk=receiver_id)
    personal_details = PersonalDetails.objects.get(user=receiver)
    
    # Fetching all messages related to the conversation between users
    messages_sent_by_request_user = Message.objects.filter(sender=request.user, receiver=receiver)
    messages_received_by_request_user = Message.objects.filter(sender=receiver, receiver=request.user)
    messages = messages_sent_by_request_user | messages_received_by_request_user
    messages = messages.order_by('timestamp')
    
    # Determine whether each message is incoming or outgoing
    for message in messages:
        message.is_incoming = message.receiver == request.user

    # Pass receiver ID to the template context
    context = {
        'receiver': receiver,
        'personal_details': personal_details,
        'messages': messages,
        'receiver_id': receiver_id,  # Include receiver_id in the context
    }

    return render(request, 'matchat/chat.html', context)



from django.db.models import BooleanField, Value
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

@never_cache
@login_required(login_url='accounts:login')
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


@never_cache
@login_required(login_url='accounts:login')
def send_message(request, receiver_id):
    if request.method == 'POST':
        receiver = User.objects.get(pk=receiver_id)
        content = request.POST.get('content')

        if content:
            message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
            message.save()

    return redirect('matchat:chat', receiver_id=receiver_id)




@never_cache
@login_required(login_url='accounts:login')
def clear_chat(request, receiver_id):
    receiver = get_object_or_404(User, pk=receiver_id)

    # Fetch all messages between the current user and the receiver
    messages_sent_by_request_user = Message.objects.filter(sender=request.user, receiver=receiver)
    messages_received_by_request_user = Message.objects.filter(sender=receiver, receiver=request.user)

    # Delete all messages (sent and received) between the users
    messages_sent_by_request_user.delete()
    messages_received_by_request_user.delete()

    return redirect('matchat:mychats') 