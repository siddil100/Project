from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


from django import forms
from .models import PersonalDetails

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'date_of_birth', 'phone_number', 'mother_tongue']

    
        


















#old

