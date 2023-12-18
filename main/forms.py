from django import forms
from main.models import Checkout, ReviewProduct

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)

class CheckoutForm(forms.Form):
    class Meta:
        model = Checkout
        fields = ['name', 'address', 'payment_method']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewProduct
        fields = ["rating", "review"]