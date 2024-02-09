from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    


from django.contrib.auth.forms import PasswordChangeForm

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        # Modify form fields' attributes if needed
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})






    
