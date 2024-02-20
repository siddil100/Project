from django import forms
from .models import Package

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['package_name', 'star_rating', 'meal_preference', 'attendees', 'days_count', 'program_count', 'price', 'image','location']
