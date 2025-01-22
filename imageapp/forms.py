from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
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
        labels = {'image': ''}