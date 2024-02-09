from django import forms
from .models import Interest

class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['message']  # Fields to be included in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form labels or widgets if needed
        self.fields['message'].widget = forms.Textarea(attrs={'rows': 4})  # Customize textarea widget, if desired
        self.fields['message'].label = 'Your Message'  # Change label text, if desired
        self.fields['message'].widget.attrs['placeholder'] = 'Type your message here'
        default_message = 'Hey, I found your profile impressive!'
        self.fields['message'].initial = default_message

