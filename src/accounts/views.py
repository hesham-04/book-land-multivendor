from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View, UpdateView
from django.contrib.auth import logout
from .forms import OnboardingForm
from src.accounts.models import Address


@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('account_login')


@method_decorator(login_required, name='dispatch')
class CrossAuthView(View):

    def get(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return redirect("admins:dashboard")
        else:
            return redirect('client:dashboard')




from .forms import OnboardingForm

@login_required
def onboarding_view(request):
    if request.method == 'POST':
        form = OnboardingForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            if user_type == 'vendor':
                request.user.is_seller = True
                request.user.is_client = False
                request.user.save()
                return redirect('seller:profile_setup_form')
            else:
                request.user.is_seller = False
                request.user.is_client = True
                request.user.save()
                return redirect('website:home')
    else:
        form = OnboardingForm()
    return render(request, 'accounts/onboarding.html', {'form': form})
