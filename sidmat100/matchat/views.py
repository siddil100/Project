from django.shortcuts import render

# Create your views here.


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message
from django.contrib.auth.models import User
from matrimony.models import*

@login_required
@login_required
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

@login_required
@login_required

def get_messages(request, receiver_id):
    receiver = User.objects.get(pk=receiver_id)
    messages_sent_by_request_user = Message.objects.filter(sender=request.user, receiver=receiver)
    messages_received_by_request_user = Message.objects.filter(sender=receiver, receiver=request.user)

    # Combine messages and add 'is_incoming' flag
    messages = list(messages_sent_by_request_user.values('content', 'timestamp').annotate(is_incoming=Value(False, output_field=BooleanField())))
    messages.extend(list(messages_received_by_request_user.values('content', 'timestamp').annotate(is_incoming=Value(True, output_field=BooleanField()))))

    sorted_messages = sorted(messages, key=lambda x: x['timestamp'])

    return JsonResponse(sorted_messages, safe=False)


@login_required
def send_message(request, receiver_id):
    if request.method == 'POST':
        receiver = User.objects.get(pk=receiver_id)
        content = request.POST.get('content')

        if content:
            message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
            message.save()

    return redirect('matchat:chat', receiver_id=receiver_id)
