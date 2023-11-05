from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
fs = FileSystemStorage(location=settings.MEDIA_ROOT)

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class PersonalDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Create a one-to-one relationship with the User model
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15,unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Define the profile image field
    mother_tongue = models.CharField(max_length=100)
    religion = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    perso_fill = models.BooleanField(default=False)
    marital_status = models.CharField(max_length=100)

    # Add any other fields you need for personal details












