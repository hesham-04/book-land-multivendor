from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SellerProfileForm

class SellerProfileCreateView(LoginRequiredMixin, FormView):
    template_name = 'seller/seller_profile_form.html'
    form_class = SellerProfileForm
    success_url = reverse_lazy('admins:dashboard')

    def form_valid(self, form):
        seller_profile = form.save(commit=False)
        seller_profile.user = self.request.user
        seller_profile.save()
        return super().form_valid(form)


