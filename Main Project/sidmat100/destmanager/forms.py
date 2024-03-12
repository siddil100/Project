from django import forms
from destmanager.models import FoodOption

class FoodOptionForm(forms.ModelForm):
    class Meta:
        model = FoodOption
        fields = ['category', 'name', 'description', 'image', 'price']
