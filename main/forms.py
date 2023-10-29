from django.forms import ModelForm
from main.models import ReviewProduct
from main.models import Checkout

class CheckoutForm(ModelForm):
    class Meta:
        model = Checkout
        fields = ['name', 'address', 'payment_method']

class SearchForm(forms.Form):
    class Meta:
        fields = ["query"]

    query = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Cari buku apa?',
               'id': 'search-book'}))

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)

class ReviewForm(ModelForm):
    class Meta:
        model = ReviewProduct
        fields = ["rating", "review"]