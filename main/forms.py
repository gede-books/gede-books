from django import forms
from main.models import Checkout

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)

class CheckoutForm(forms.Form):
    class Meta:
        model = Checkout
        fields = ['name', 'address', 'payment_method']