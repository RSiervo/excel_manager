from django import forms
from django.contrib.auth.models import User
# accounts/apps.py
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals  # Import the signals to initialize


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    profile_picture = forms.ImageField(required=False)  # Add an ImageField for the profile picture

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_confirmation', 'profile_picture']  # Include the profile picture in the fields

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        # Check if passwords match
        if password and password_confirmation and password != password_confirmation:
            self.add_error("password_confirmation", "Passwords do not match.")

        # Check if username is unique
        username = cleaned_data.get("username")
        if username and User.objects.filter(username=username).exists():
            self.add_error("username", "Username is already taken.")

        # Check if email is unique
        email = cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            self.add_error("email", "Email is already in use.")

        return cleaned_data
