from django.forms import ModelForm
from main.models import ReviewProduct

class ReviewForm(ModelForm):
    class Meta:
        model = ReviewProduct
        fields = ["rating", "review"]