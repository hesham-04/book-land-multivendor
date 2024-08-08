from django import forms
from django.forms import ModelForm

from .models import (
    Product, ProductVersion, Version, ProductImage, Post, OtherPlatform
)
from ...accounts.models import User


# forms.py

from django import forms
from django.forms import ModelForm
from .models import Product, ProductVersion, ProductImage, OtherPlatform
from ...accounts.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'thumbnail_image', 'name',
            'book_type', 'categories', 'languages', 'pages',
            'artist', 'author', 'translator', 'illustrator',
            'description', 'is_active'
        ]

    def __init__(self, *args, **kwargs):
        self.seller = kwargs.pop('seller', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.seller:
            product.seller = self.seller
        if commit:
            product.save()
        return product

class ProductVersionForm(forms.ModelForm):
    class Meta:
        model = ProductVersion
        fields = [
            'version', 'isbn', 'price'
        ]

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = [
            'image', 'description'
        ]

class ProductPlatformForm(forms.ModelForm):
    class Meta:
        model = OtherPlatform
        fields = [
            'image', 'url'
        ]

class MyProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'profile_image', 'first_name', 'last_name',
            'phone_number', 'email'
        ]



from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # 'product' is not included here
        widgets = {
            'rating': forms.RadioSelect(),
        }
        labels = {
            'rating': 'Rate this product',
            'comment': 'Your review',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})
