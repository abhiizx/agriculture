from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


# reset password
from django.contrib.auth.forms import PasswordResetForm
from django import forms
from django.contrib.auth.models import User

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email_or_username_or_phone = self.cleaned_data.get('email')

        # Custom logic to check if input is email, phone, or username
        try:
            user = User.objects.get(email=email_or_username_or_phone)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=email_or_username_or_phone)
            except User.DoesNotExist:
                user = None

        if not user:
            raise forms.ValidationError("No user found with this information.")
        return email_or_username_or_phone
