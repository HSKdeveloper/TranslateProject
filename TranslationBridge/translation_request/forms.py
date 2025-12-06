from django import forms
from .models import TranslationRequest



class TranslationRequestForm(forms.ModelForm):
    class Meta:
        model = TranslationRequest
        fields = [
            'company_name',
            'company_type',
            'request_type',
            'description',
            'cost',
            'location',
            'language',
            'specialty',
            'file',
            'duration_days',
            'start_date',
            'city',
            'status'
   
        ]

        widgets = {
            "company_name": forms.TextInput(attrs={
                "class": "form-control mt-2",
                "placeholder": "Enter Company Name..."
            }),
            "company_type": forms.Select(attrs={
                "class": "form-control"
            }),
            "request_type": forms.HiddenInput(),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }



