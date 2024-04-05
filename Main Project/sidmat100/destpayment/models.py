from django.db import models
from myadmin.models import Package
from django.contrib.auth.models import User
# Create your models here.


class PackageBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_date = models.DateTimeField(null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)  # Add receipt field
    event_date = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f'{self.user.username} - {self.package.package_name}'
    


from django.utils import timezone
from destmanager.models import *

class CustomPackageBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_date = models.DateTimeField(null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    package_name = models.CharField(max_length=255)
    decor_type = models.ManyToManyField(DecorationOption)
    event_type = models.ManyToManyField(EventOption)
    food_type = models.ManyToManyField(FoodOption)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    attendees = models.IntegerField(default=10)
    location = models.CharField(max_length=100)
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)

    event_datefrom = models.DateTimeField(null=True, blank=True)
    event_dateto = models.DateTimeField(null=True, blank=True)



    def __str__(self):
        return f"{self.user.username}'s Booking - {self.package_name}"
    
    def save(self, *args, **kwargs):
        if not self.subscription_date:
            self.subscription_date = timezone.now()
        super().save(*args, **kwargs)