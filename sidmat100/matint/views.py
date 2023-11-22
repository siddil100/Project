from django.shortcuts import render, redirect, get_object_or_404
from .forms import InterestForm  # Import your InterestForm from forms.py
from .models import Interest
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.shortcuts import render, redirect, get_object_or_404
from .forms import InterestForm
from .models import Interest
from django.contrib.auth.decorators import login_required

@login_required
def send_interest(request, user_id):
    recipient = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            sender = request.user  # Get the currently logged-in user
            Interest.objects.create(receiver=recipient, message=message, sender=sender)
            return redirect('matrimony:home')  # Replace 'success_page' with your actual success URL name
    else:
        form = InterestForm()

    context = {
        'form': form,
        'recipient': recipient,
    }
    return render(request, 'matint/send_interest.html', context)



from django.shortcuts import render, get_object_or_404
from .models import Interest

@login_required
def received_interests(request):
    received_interests = Interest.objects.filter(receiver=request.user, status=Interest.PENDING)
    context = {
        'received_interests': received_interests,
    }
    return render(request, 'matint/received_interests.html', context)


@login_required
def accept_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    if interest.receiver == request.user and interest.status == Interest.PENDING:
        interest.status = Interest.ACCEPTED
        interest.save()
        # You can redirect to a success page or another view
        return redirect('matint:received_interests')
    # Handle cases where the interest is already accepted or the user doesn't have permission

@login_required
def reject_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    if interest.receiver == request.user and interest.status == Interest.PENDING:
        interest.status = Interest.REJECTED
        interest.save()
        # You can redirect to a success page or another view
        return redirect('matint:received_interests')
    # Handle cases where the interest is already rejected or the user doesn't have permission


