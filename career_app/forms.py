from django import forms
from django.contrib.auth.models import User

class CareerSearchForm(forms.Form):
    skills = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'e.g. Python, Creativity, Communication',
        'class': 'input-field'
    }))
    preferences = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'e.g. Remote jobs, High salary, Design-focused roles',
        'class': 'input-field'
    }))

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)