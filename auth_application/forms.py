from django import forms
from .models import User
"""
i changed the this file by adding attrs as attributes to the widgets to be able to add the class and placeholder to the widgets
this is similar to <input type="text" class="form-control" placeholder="First Name"> in html
😁😁😁
"""
class RegistrationForm(forms.ModelForm):
    email= forms.EmailField(widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
        }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
        }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number',
        }))
    role = forms.ChoiceField(choices=[('patient', 'Patient'), ('doctor', 'Doctor'),('admin','Admin')], widget=forms.Select(attrs={
            'class': 'form-control',
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        }))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'role']
        widgets = {
            'role': forms.Select(choices=[('patient', 'Patient'), ('doctor', 'Doctor')])
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email= forms.EmailField(widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }))