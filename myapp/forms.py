from django import forms
from .models import Device


class DeviceCreateForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'ipAdress']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ipAdress': forms.TextInput(attrs={'class': 'form-control'}),
        }
