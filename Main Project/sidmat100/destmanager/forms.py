from django import forms
from destmanager.models import *

class FoodOptionForm(forms.ModelForm):
    class Meta:
        model = FoodOption
        fields = ['category','subcategory', 'name', 'description', 'image', 'price']




class EventOptionForm(forms.ModelForm):
    class Meta:
        model = EventOption
        fields = ['category','event', 'name', 'description', 'image', 'price']







class DecorationOptionForm(forms.ModelForm):
    class Meta:
        model = DecorationOption
        fields = ['type','subtype', 'name', 'description', 'image', 'price']






from django import forms
from django.core.exceptions import ValidationError
from .models import License

from django import forms
from .models import License

class LicenseForm(forms.ModelForm):
    class Meta:
        model = License
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'dob', 'phone', 'license_file']

    def clean_license_file(self):
        data = self.cleaned_data['license_file']
        # Check if the file extension is PDF
        if not data.name.endswith('.pdf'):
            raise forms.ValidationError('Only PDF files are allowed.')
        return data
    

    


