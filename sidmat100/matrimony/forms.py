from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


from .models import PersonalDetails
from .models import FamilyDetails
from .models import EducationalDetails
from .models import EmploymentDetails
from .models import LocationDetails

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'birth_place', 'date_of_birth', 'blood_group', 'phone_number', 'profile_image', 'mother_tongue', 'religion', 'sector', 'marital_status']





class FamilyDetailsForm(forms.ModelForm):
    class Meta:
        model = FamilyDetails
        exclude = ('user',)



class EducationalDetailsForm(forms.ModelForm):
    class Meta:
        model = EducationalDetails
        exclude = ('user',)


class EmploymentDetailsForm(forms.ModelForm):
    class Meta:
        model = EmploymentDetails
        exclude = ('user',)



class LocationDetailsForm(forms.ModelForm):
    class Meta:
        model = LocationDetails
        exclude = ('user',)

    






    
        


















#old

