from django import forms
from .models import CustomerContact, RetailerContact


class CustomerContactForm(forms.ModelForm):
    class Meta:
        model = CustomerContact
        fields = "__all__"


class RetailerContactForm(forms.ModelForm):
    class Meta:
        model = RetailerContact
        fields = "__all__"
