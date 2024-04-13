from django.db import models
from django.conf import settings
# Create your models here.

from django.db import models

class FoodOption(models.Model):
    CATEGORY_CHOICES = (
        ('veg', 'Vegetarian'),
        ('non_veg', 'Non-Vegetarian'),
        ('mixed', 'Mixed'),
    )
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='food_images/')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
    
    

    



class DecorationOption(models.Model):
    TYPE_CHOICES = (
        ('floral', 'Floral Decorations'),
        ('candles', 'Candles and Lanterns'),
        ('lighting', 'Lighting'),
        ('signage', 'Custom Signage and Stationery'),
        ('themed', 'Themed Decor'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    subtype = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='decoration_images/')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
    

  



from datetime import date
class License(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_file = models.FileField(upload_to='licenses/')
    is_valid = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)
    dob = models.DateField()  # Default to today's date
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"License for {self.user.username}"
    



from django.utils.html import mark_safe
from django.utils import timezone



class EventOption(models.Model):
    CATEGORY_CHOICES = (
        ('wedding_events', 'Wedding Events'),
        ('pre_wedding_events', 'Pre Wedding Events'),
        ('post_wedding_events', 'Post Wedding Events'),
    )
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    event = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='food_images/')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
    
   




class Scheduling(models.Model):
    location = models.CharField(max_length=100)
    
    limit = models.IntegerField()
    

    def __str__(self):
        return self.location
    



class SchedulingBooking(models.Model):
    location = models.CharField(max_length=100)
    booking_count = models.IntegerField(default=0)
    limit = models.IntegerField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.location

    

   
   