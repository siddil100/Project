from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.validators import RegexValidator


from .models import PersonalDetails,Hobby
from .models import FamilyDetails
from .models import EducationalDetails
from .models import EmploymentDetails
from .models import LocationDetails

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'birth_place', 'date_of_birth', 'blood_group', 'phone_number', 'profile_image', 'mother_tongue', 'religion', 'sector', 'marital_status', 'about_you', 'address', 'aadhar_card', 'aadhar_valid', 'hobbies']

    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Please enter a valid 10-digit phone number.",
            )
        ]
    )

    aadhar_card = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    profile_image = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )



class PersonalDetailsUpdateForm(PersonalDetailsForm):
    class Meta:
        model = PersonalDetails
        exclude = ['user', 'date_of_birth', 'gender', 'mother_tongue', 'blood_group', 'perso_fill']

    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    profile_image = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )




class PersonalDetailsAadharForm(forms.ModelForm):
    aadhar_card = forms.FileField(
        required=True,
        label='Upload Aadhar Card (PDF)',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    class Meta:
        model = PersonalDetails
        exclude = ['user','first_name', 'last_name', 'middle_name', 'gender', 'birth_place', 'date_of_birth', 'blood_group', 'phone_number', 'profile_image', 'mother_tongue', 'religion', 'sector', 'marital_status', 'about_you', 'address','perso_fill', 'aadhar_valid', 'hobbies']






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

