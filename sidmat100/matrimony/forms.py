from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


from .models import PersonalDetails,Hobby
from .models import FamilyDetails
from .models import EducationalDetails
from .models import EmploymentDetails
from .models import LocationDetails

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'birth_place', 'date_of_birth', 'blood_group', 'phone_number', 'profile_image', 'mother_tongue', 'religion', 'sector', 'marital_status', 'about_you', 'address', 'aadhar_card', 'hobbies']

    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )



class PersonalDetailsUpdateForm(PersonalDetailsForm):
    class Meta:
        model = PersonalDetails
        exclude = ['user', 'date_of_birth', 'gender', 'mother_tongue', 'blood_group', 'phone_number', 'perso_fill']

    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    profile_image = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )






class FamilyDetailsForm(forms.ModelForm):
    class Meta:
        model = FamilyDetails
        exclude = ('user',)


from django import forms
from .models import FamilyDetails

class FamilyDetailsUpdateForm(forms.ModelForm):
    class Meta:
        model = FamilyDetails
        exclude = ['user', 'famil_fill', 'father_name', 'mother_name']



class EducationalDetailsForm(forms.ModelForm):
    class Meta:
        model = EducationalDetails
        exclude = ('user',)

from django import forms
from .models import EducationalDetails

class EducationalDetailsUpdateForm(forms.ModelForm):
    class Meta:
        model = EducationalDetails
        exclude = ['user', 'educ_fill']



class EmploymentDetailsForm(forms.ModelForm):
    class Meta:
        model = EmploymentDetails
        exclude = ('user',)

from django import forms
from .models import EmploymentDetails

class EmploymentDetailsUpdateForm(forms.ModelForm):
    class Meta:
        model = EmploymentDetails
        exclude = ['user', 'empl_fill']




class LocationDetailsForm(forms.ModelForm):
    class Meta:
        model = LocationDetails
        exclude = ('user',)


from django import forms
from .models import LocationDetails

class LocationDetailsUpdateForm(forms.ModelForm):
    class Meta:
        model = LocationDetails
        exclude = ['user', 'loca_fill']

    






    
        


















#old

