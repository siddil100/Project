from django.db import models
from django.conf import settings
# Create your models here.

class FoodOption(models.Model):
    CATEGORY_CHOICES = (
        ('veg', 'Vegetarian'),
        ('non_veg', 'Non-Vegetarian'),
        ('mixed', 'Mixed'),
    )
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
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
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='decoration_images/')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
    




class License(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_file = models.FileField(upload_to='licenses/')
    is_valid = models.BooleanField(default=False)  # Add the is_valid field

    def __str__(self):
        return f"License for {self.user.username}"