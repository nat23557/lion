from django import forms
from .models import Comment
from .models import Listing


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'style': 'width: 100%; height: 100px; padding: 10px; margin-bottom: 10px; border: none; border-radius: 4px; background-color: #555; color: #fff;'})
        }
class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'style': 'width: 100%; height: 100px; padding: 10px; margin-bottom: 10px; border: none; border-radius: 4px; background-color: #555; color: #fff;'}),
        }

    image = forms.ImageField(required=False)  # Add the image field to the form



class BidForm(forms.Form):
    bid_amount = forms.DecimalField(label="Bid Amount", max_digits=10, decimal_places=2)
