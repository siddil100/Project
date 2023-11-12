from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
fs = FileSystemStorage(location=settings.MEDIA_ROOT)
from datetime import date
# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Hobby(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class PersonalDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Create a one-to-one relationship with the User model
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    birth_place = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15,unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Define the profile image field
    mother_tongue = models.CharField(max_length=100)
    religion = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    perso_fill = models.BooleanField(default=False)
    marital_status = models.CharField(max_length=100)
    about_you = models.TextField(blank=True)
    aadhar_card = models.FileField(upload_to='aadhar_cards/', blank=True, null=True)
    aadhar_valid = models.BooleanField(default=True)
    hobbies = models.ManyToManyField(Hobby, blank=True,null=True)

   
    def calculate_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age
    
    def update_aadhar_valid(self, value):
        self.aadhar_valid = value
        self.save()
    

    # Now family details

    from django.db import models
from django.contrib.auth.models import User

class FamilyDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Create a foreign key relationship with the User model
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    number_of_siblings = models.PositiveIntegerField()
    father_occupation = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100)
    family_type = models.CharField(max_length=100)
    family_status = models.CharField(max_length=100)
    number_of_family_members = models.PositiveIntegerField()
    famil_fill = models.BooleanField(default=False)

    # Add any other fields you need for family details


class EducationalDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Create a foreign key relationship with the User model
    highest_qualification = models.CharField(max_length=100)
    ug_degree = models.CharField(max_length=100,blank=True)
    pg_degree = models.CharField(max_length=100,blank=True)
    doctorate_field = models.CharField(max_length=100,blank=True)
    grad_year = models.DateField()
    college_institution = models.CharField(max_length=100)
    educ_fill = models.BooleanField(default=False)




class EmploymentDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Create a foreign key relationship with the User model
    employment_status = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100, blank=True)
    employerof = models.CharField(max_length=100, blank=True)
    annual_income = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    job_location = models.CharField(max_length=100, blank=True)
    about_job = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    social_link = models.URLField(blank=True)
    empl_fill = models.BooleanField(default=False)


from django.utils import timezone



class LocationDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_city = models.CharField(max_length=100)
    current_state = models.CharField(max_length=100)
    current_pin_code = models.CharField(max_length=20)
    willing_to_move = models.CharField(max_length=3)
    additional_comments = models.TextField(blank=True)
    location_photos = models.ImageField(upload_to='location_photos/', blank=True, null=True)
    loca_fill = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=200, blank=True, null=True)
    

    def is_token_expired(self):
        expiration_time = self.get_token_expiration_time()
        return timezone.now() > expiration_time

    def get_token_expiration_time(self):
        expiration_time = self.created_at + timezone.timedelta(minutes=5)
        return expiration_time

    














