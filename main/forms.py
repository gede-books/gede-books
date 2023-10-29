from django import forms

class CheckoutForm(forms.Form):
    class Meta:
        name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
        payment_method = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))