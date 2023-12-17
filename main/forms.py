from django import forms
<<<<<<< HEAD
from main.models import Checkout
=======
from django.forms import ModelForm
from main.models import ReviewProduct


class SearchForm(forms.Form):
    class Meta:
        fields = ["query"]

    query = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Cari buku apa?',
               'id': 'search-book'}))
>>>>>>> cb2366c7a62a2fb7e99ca49eabc216a9ed650675

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)

<<<<<<< HEAD
class CheckoutForm(forms.Form):
    class Meta:
        model = Checkout
        fields = ['name', 'address', 'payment_method']
=======
class ReviewForm(ModelForm):
    class Meta:
        model = ReviewProduct
        fields = ["rating", "review"]
>>>>>>> cb2366c7a62a2fb7e99ca49eabc216a9ed650675
