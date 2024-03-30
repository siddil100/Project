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
    

    


from django import forms
from destpayment.models import CustomPackageBooking

class BookingForm(forms.ModelForm):
    decor_type = forms.MultipleChoiceField(choices=(), widget=forms.CheckboxSelectMultiple)
    event_type = forms.MultipleChoiceField(choices=(), widget=forms.CheckboxSelectMultiple)
    food_type = forms.MultipleChoiceField(choices=(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['decor_type'].choices = self.get_decor_choices()
        self.fields['event_type'].choices = self.get_event_choices()
        self.fields['food_type'].choices = self.get_food_choices()

    def get_decor_choices(self):
        return [(decor.id, f"{decor.name} ({decor.type}, {decor.subtype}, {decor.description}, {decor.price})") for decor in DecorationOption.objects.all()]

    def get_event_choices(self):
        return [(event.id, f"{event.name} ({event.category}, {event.event}, {event.description}, {event.price})") for event in EventOption.objects.all()]

    def get_food_choices(self):
        return [(food.id, f"{food.name} ({food.category}, {food.subcategory}, {food.description}, {food.price})") for food in FoodOption.objects.all()]

    class Meta:
        model = CustomPackageBooking
        fields = ['event_date', 'package_name', 'decor_type', 'event_type', 'food_type', 'price']
