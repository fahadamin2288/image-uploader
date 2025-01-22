from django import forms
from .models import Image
from django import forms
from django.core.exceptions import ValidationError


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Enter your email", max_length=254)

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-3', 
                'placeholder': 'Enter image title',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control mb-3',
                'accept': 'image/*'
            })
        }

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise ValidationError("New password and confirm password do not match.")
        return cleaned_data