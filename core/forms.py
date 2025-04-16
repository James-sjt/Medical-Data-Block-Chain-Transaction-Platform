from django import forms
from .models import DataFile
from django.contrib.auth.models import User

class UploadForm(forms.ModelForm):
    class Meta:
        model = DataFile
        fields = ['title', 'description', 'file', 'is_for_sale', 'price']

class TransferForm(forms.Form):
    new_owner = forms.ModelChoiceField(queryset=User.objects.all())