from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Assuming you're using Django's built-in User model

class Interest(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_interests')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_interests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Interest from {self.sender.username} to {self.receiver.username} - {self.get_status_display()}"
    

    from django.db import models
from django.contrib.auth.models import User
from matrimony.models import PersonalDetails



# Your code using the PersonalDetails model in the matint app


class InterestedProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expressed_interests')
    interested_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expressed_interest_by')
    interested_user_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE)

    # Add additional fields as needed
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} added in {self.interested_user.username}'s profile to interested profiles'"
    

#NOT INTERESTED PROFILE MODELS

class NotInterested(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='not_interested_users')
    not_interested_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='not_interested_by')
    not_interested_user_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} marked {self.not_interested_user.username} as not interested"

    





