from django.forms import *
from main.models import ReviewProduct, Checkout

class ReviewForm(ModelForm):
    class Meta:
        model = ReviewProduct
        fields = ["rating", "review"]

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)

class CheckoutForm(forms.Form):
    class Meta:
        model = Checkout
        fields = ['name', 'address', 'payment_method']
