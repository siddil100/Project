from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


from .models import PersonalDetails

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'date_of_birth', 'phone_number', 'profile_image', 'mother_tongue', 'religion', 'sector', 'marital_status']





    
        


















#old

