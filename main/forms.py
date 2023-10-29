from django.forms import ModelForm
from main.models import Checkout

class CheckoutForm(ModelForm):
    class Meta:
        model = Checkout
        fields = ['name', 'address', 'payment_method']