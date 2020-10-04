from django import forms
from .models import *
from django.core.exceptions import ValidationError


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['number', 'mark', 'model', 'year', 'user_name', 'user_number']

        widgets = {
            'number': forms.TextInput(attrs={'class': 'validate', 'id': 'input_car', 'style': 'margin:0; padding:0; text-transform: uppercase;'}),
            'mark': forms.TextInput(attrs={'class': 'validate', 'id': 'input_car', 'style': 'margin:0; padding:0;'}),
            'model': forms.TextInput(attrs={'class': 'validate', 'id': 'input_car', 'style': 'margin:0; padding:0;'}),
            'year': forms.NumberInput(attrs={'class': 'validate', 'id': 'input_car', 'style': 'margin:0; padding:0;'}),
            'user_name': forms.TextInput(attrs={'class': 'validate', 'id': 'input_car', 'style': 'margin:0; padding:0;'}),
            'user_number': forms.TextInput(attrs={'class': 'validate', 'id': 'input_car', 'style': 'margin:0; padding:0;', 'data-inputmask': "'mask': '+38(099) 999-9999'"})
        }

    def clean_number(self):
        new_number = self.cleaned_data['number']
        new_number = new_number.upper()
        if Car.objects.filter(number__iexact=new_number).count():
            raise ValidationError(f"Номер: {new_number} вже існує в базі даних")

        return new_number


class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ['type', 'description', 'price', 'date']

        widgets = {
            'type': forms.TextInput(attrs={'class': 'validate', 'id': 'input_repair', 'style': 'margin:0; padding:0;'}),
            'description': forms.Textarea(attrs={'class': 'validate', 'id': 'textarea_repair', 'style': 'margin:0; padding:0; height:100px;'}),
            'price': forms.NumberInput(attrs={'class': 'validate', 'id': 'input_repair', 'style': 'margin:0; padding:0;'}),
            'date': forms.DateTimeInput(attrs={'class': 'validate', 'id': 'input_repair', 'style': 'margin:0; padding:0;'})
        }