from django import forms
from .models import HAConfig

class HAConfigForm(forms.ModelForm):
    class Meta:
        model = HAConfig
        fields = '__all__'
