from django import forms


class SearchForm(forms.Form):
    class Meta:
        fields = ["query"]

    query = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Cari buku apa?',
               'id': 'search-book'}))
