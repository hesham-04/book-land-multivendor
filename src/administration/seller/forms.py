from django import forms
from .models import SellerProfile

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['store_name', 'store_description', 'profile_image']