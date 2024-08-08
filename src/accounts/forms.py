from django import forms

class OnboardingForm(forms.Form):
    CHOICES = [
        ('buyer', 'Buyer'),
        ('vendor', 'Seller'),
    ]
    user_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
