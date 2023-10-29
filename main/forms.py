from django import forms
from django.forms import ModelForm
from main.models import ReviewProduct


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
